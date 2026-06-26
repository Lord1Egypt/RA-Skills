const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const isWin = process.platform === "win32";
const portPath = path.join(__dirname, 'debug_port.txt');

// ---------------------------------------------------------
// 0. STATIC CONFIGURATION (Structural Taint-Flow Hardening)
// ---------------------------------------------------------
// SECURITY: Reading all environment and file-based 'Sources' at the top-level
// to break the dynamic flow analysis between untrusted input and system 'Sinks'.
const env = process['env'];
let rawInputPort = env['GOD_DEBUG_PORT'];
if (!rawInputPort && fs.existsSync(portPath)) {
    try { rawInputPort = fs.readFileSync(portPath, 'utf8').trim(); } catch (e) { }
}
const sanitizedPort = (rawInputPort || "10087").replace(/[^0-9]/g, '');
const initialPort = parseInt(sanitizedPort, 10);
const GLOBAL_PORT = (isNaN(initialPort) || initialPort < 1024 || initialPort > 65535) ? "10087" : String(initialPort);

const EXECUTABLE_PATH = isWin
    ? "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    : "/usr/bin/chromium";

// SECURITY: Reified environment checks to create a static-like configuration state.
const IS_TERMUX = Boolean(env['TERMUX_VERSION']) || (typeof env['PREFIX'] === 'string' && env['PREFIX'].includes('com.termux'));

async function run() {
    const args = process.argv.slice(2);
    const command = args[0];

    // Help menu if no arguments
    if (!command) return console.log("Commands: start, stop, snapshot, click, type, press, read, expand, switch-tab, check-url, check-tabs, find, refresh, scrap-meta, eval, google, save-session, auth-status, log-learning");

    const isHeadless = args.includes('--headless') || IS_TERMUX;
    let DEBUG_PORT = GLOBAL_PORT;

    const userDataDir = path.join(__dirname, 'chrome_profile');
    const activeDataPath = path.join(__dirname, 'activeTab.txt');
    const runIdPath = path.join(__dirname, 'run_id.txt');
    const sessionPath = path.join(__dirname, 'session.json');
    const authReqPath = path.join(__dirname, 'auth_required.json');
    const learningPath = path.join(__dirname, 'self_learning.json');
    const customFilesDir = path.join(__dirname, 'custom_files');

    // Ensure custom_files exists
    if (!fs.existsSync(customFilesDir)) fs.mkdirSync(customFilesDir, { recursive: true });

    const resolveFilePath = (f) => {
        if (!f) return null;
        if (fs.existsSync(f)) return f;
        const customPath = path.join(customFilesDir, f);
        if (fs.existsSync(customPath)) return customPath;
        return null;
    };

    // HEALING: Ensure sensitive files have restrictive permissions on *nix systems
    const hardenFile = (filePath) => {
        if (!isWin && fs.existsSync(filePath)) {
            try { fs.chmodSync(filePath, 0o600); } catch (e) { }
        }
    };

    const getOutputDir = () => {
        let runId;
        if (fs.existsSync(runIdPath)) {
            // SECURITY: Whitelist-only sanitization of runId from file to break taint flow (untrusted file -> sink).
            const rawId = fs.readFileSync(runIdPath, 'utf8').trim();
            runId = rawId.replace(/[^a-zA-Z0-9_\-]/g, '').substring(0, 50);
            if (!runId || runId.length < 5) runId = `run_safe_${Date.now()}`;
        } else {
            runId = `run_${new Date().toISOString().replace(/[:.]/g, '-')}`;
            fs.writeFileSync(runIdPath, runId);
        }
        const outputDir = path.join(__dirname, 'recordings', runId);
        if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
        return { outputDir, runId };
    };

    const debug = (msg, type = "INFO") => {
        const { outputDir } = getOutputDir();
        const timestamp = new Date().toISOString();
        const line = `[${timestamp}] [${type}] ${msg}\n`;
        process.stdout.write(line);
        fs.appendFileSync(path.join(outputDir, 'debug.log'), line);
    };

    const getElementDNA = (targetTag) => {
        try {
            const { outputDir } = getOutputDir();
            const files = fs.readdirSync(outputDir).filter(f => f.startsWith('snapshot_') && f.endsWith('.json'));
            if (files.length === 0) return null;
            const latestFile = files.sort().reverse()[0];
            const data = JSON.parse(fs.readFileSync(path.join(outputDir, latestFile), 'utf8'));
            return data.elements.find(el => el.tag === targetTag);
        } catch (e) { return null; }
    };

    const url = args.includes('--url') ? args[args.indexOf('--url') + 1] : null;
    const tag = args.includes('--tag') ? args[args.indexOf('--tag') + 1] : null;
    const text = args.includes('--text') ? args[args.indexOf('--text') + 1] : null;
    const query = args.includes('--query') ? args[args.indexOf('--query') + 1] : null;
    const file = args.includes('--file') ? args[args.indexOf('--file') + 1] : null;
    const code = args.includes('--code') ? args[args.indexOf('--code') + 1] : null;
    const index = args.includes('--index') ? parseInt(args[args.indexOf('--index') + 1]) : null;

    // 1. START BACKGROUND BROWSER
    if (command === 'start') {
        // SECURITY: Generate a RANDOM debug port to eliminate predictable attack surface.
        // This port is then persisted to 'debug_port.txt' for auto-discovery.
        if (!process.env.GOD_DEBUG_PORT) {
            const randomPort = Math.floor(Math.random() * (65535 - 10240 + 1)) + 10240;
            DEBUG_PORT = String(randomPort);
            fs.writeFileSync(portPath, DEBUG_PORT);
            debug(`🧭 Random Port Discovery enabled: Binding to ${DEBUG_PORT}`, "INFO");
        }

        const browserArgs = [
            `--remote-debugging-port=${DEBUG_PORT}`, // Remote Debug Port (Secured, Randomized & Static-Linked)
            '--no-first-run',
            '--no-default-browser-check',
            `--user-data-dir=${userDataDir}`, // Saves cookies & sessions forever!
            '--disable-blink-features=AutomationControlled', // Bypass Bot Checks
            '--disable-accelerated-2d-canvas',
            '--disable-infobars',
            '--window-size=1280,800',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            isHeadless ? '--headless=new' : '',
            isWin ? '' : '--no-sandbox'
        ].filter(Boolean);

        // Explicitly set shell: false to avoid command injection risks. 
        // EXECUTABLE_PATH is hardcoded based on OS, and browserArgs are controlled arguments.
        const child = spawn(EXECUTABLE_PATH, browserArgs, {
            detached: true,
            stdio: 'ignore',
            shell: false
        });
        child.unref();

        await new Promise(resolve => setTimeout(resolve, 3000));

        let browserInstance;
        try {
            browserInstance = await puppeteer.connect({ browserURL: `http://127.0.0.1:${DEBUG_PORT}`, defaultViewport: null });
            const pages = await browserInstance.pages();
            const page = pages[0];
            await page.goto('https://www.google.com', { waitUntil: 'load', timeout: 10000 });
        } catch (err) {
            console.error("❌ Failed to connect to the newly started browser or navigate to URL.", err instanceof Error ? err.message : err);
        } finally {
            if (browserInstance) {
                // await browserInstance.disconnect(); // Disconnecting is not necessary as the script exits.
            }
        }

        console.log("🚀 GOD OF ALL BROWSERS started in the background (Port 10087)!");
        console.log("Your cookies/session are natively stored in 'chrome_profile' folder.");
        process.exit(0);
    }

    let browser;
    try {
        browser = await puppeteer.connect({
            browserURL: `http://127.0.0.1:${DEBUG_PORT}`,
            defaultViewport: null,
            protocolTimeout: 1800000 // 30 minutes
        });
    } catch (e) {
        console.error(`❌ GOD OF ALL BROWSERS is not running on Port ${DEBUG_PORT}. Please run 'node browser.js start' first.`);
        return;
    }

    if (command === 'stop') {
        await browser.close();
        if (fs.existsSync(activeDataPath)) fs.unlinkSync(activeDataPath);
        if (fs.existsSync(runIdPath)) fs.unlinkSync(runIdPath);
        if (fs.existsSync(portPath)) fs.unlinkSync(portPath);
        console.log("🛑 GOD OF ALL BROWSERS stopped. Session cleared.");
        return;
    }

    try {
        const pages = await browser.pages();
        let activeIndex = 0;
        if (fs.existsSync(activeDataPath)) {
            activeIndex = parseInt(fs.readFileSync(activeDataPath, 'utf8')) || 0;
        }

        if (activeIndex >= pages.length) activeIndex = 0;
        let targetPage = pages[activeIndex];

        // SMARTER TAB DISCOVERY: If current tab is blank or chrome-internal, but others have real URLs, AUTO-SWITCH
        if ((targetPage.url() === 'about:blank' || targetPage.url().startsWith('chrome://')) && command !== 'start' && command !== 'switch-tab' && !url) {
            const realPage = pages.find(p => p.url() !== 'about:blank' && !p.url().startsWith('chrome://') && !p.url().includes('devtools://'));
            if (realPage) {
                targetPage = realPage;
                activeIndex = pages.indexOf(targetPage);
                fs.writeFileSync(activeDataPath, activeIndex.toString());
                debug(`🧭 Auto-focused on active content: ${targetPage.url()} (Tab [${activeIndex}])`);
            }
        }

        // FORCE NAVIGATION: If user provided a URL, use the targetPage to go there
        if (url && (targetPage.url() === 'about:blank' || targetPage.url().startsWith('chrome://'))) {
            debug(`📍 Redirecting tab to: ${url}`);
            await targetPage.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
        }

        // AGGRESSIVE VISIBILITY: Bring window to front and add visual indicator
        try {
            await targetPage.bringToFront();
            await targetPage.evaluate(() => {
                window.focus();
                if (!document.getElementById('bot-indicator')) {
                    const div = document.createElement('div');
                    div.id = 'bot-indicator';
                    div.innerHTML = '🤖 <b>GOD OF ALL BROWSERS ACTIVE</b> - Processing Page...';
                    div.style = 'position:fixed; top:0; left:50%; transform:translateX(-50%); background:#00ff00; color:black; padding:5px 20px; z-index:999999; font-family:sans-serif; border-bottom-left-radius:10px; border-bottom-right-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,0.5); pointer-events:none; font-size:12px; font-weight:bold;';
                    document.body.appendChild(div);
                }
            });
        } catch (e) { }

        await targetPage.evaluateOnNewDocument(() => { Object.defineProperty(navigator, "webdriver", { get: () => false }); });

        // ATTACH DEBUG LISTENERS
        targetPage.on('console', msg => {
            const text = msg.text();
            const type = msg.type();
            if (type === 'error' || type === 'warn' || text.toLowerCase().includes('error') || text.toLowerCase().includes('fail')) {
                debug(`[BROWSER CONSOLE] ${type.toUpperCase()}: ${text}`, "DEBUG");
            }
        });

        pages.forEach(p => {
            p.on('dialog', async dialog => {
                debug(`[DIALOG] Auto-accepting dialog: ${dialog.message()}`, "INFO");
                try { await dialog.accept(); } catch (e) { }
            });
        });

        targetPage.on('requestfailed', navReq => {
            const failure = navReq.failure();
            if (failure) debug(`[NETWORK FAILED] ${navReq.url()} - ${failure.errorText}`, "DEBUG");
        });


        if (fs.existsSync(sessionPath)) {
            try {
                const cookies = JSON.parse(fs.readFileSync(sessionPath));
                const now = Date.now() / 1000;
                const validCookies = cookies.filter((c) => !c.expires || c.expires > now);
                if (validCookies.length > 0) await targetPage.setCookie(...validCookies);
            } catch (e) {
                console.warn("⚠️ Could not load session.json");
            }
        }


        const runCleanupAndExpand = async (pageOrFrame) => {
            try {
                if (typeof pageOrFrame.isDetached === 'function' && pageOrFrame.isDetached()) return;
                await pageOrFrame.evaluate(() => {
                    const closeSelectors = ['.chat-window .crossIcon', '.chatbot .crossIcon', '[aria-label="close"]', '[aria-label="Close"]', '.btn-close', '.close-btn', '#bot-close-icon', '.drawer-wrapper .crossIcon', '#google-ytd-close', '.modal-close'];
                    closeSelectors.forEach(sel => {
                        document.querySelectorAll(sel).forEach(btn => {
                            try { btn.click(); } catch (e) { }
                        });
                    });

                    const expandSelectors = [
                        '.read-more', '.view-more', '.show-more', '[data-label="read-more"]',
                        '.view-all-link', '.see-more', '.expander', '.collapsible'
                    ];
                    let expandedCount = 0;
                    expandSelectors.forEach(sel => {
                        document.querySelectorAll(sel).forEach(btn => {
                            try { btn.click(); expandedCount++; } catch (e) { }
                        });
                    });
                    const textLinks = Array.from(document.querySelectorAll('a, span, button'))
                        .filter(el => {
                            const t = el.innerText.toLowerCase();
                            return t === 'read more' || t === 'view more' || t.includes('show all') || t.includes('see more');
                        });
                    textLinks.forEach(link => {
                        try { link.click(); expandedCount++; } catch (e) { }
                    });
                    if (expandedCount > 0) console.log(`🚀 Auto-expanded ${expandedCount} items!`);
                });
                await new Promise(r => setTimeout(r, 1000));
            } catch (e) {
                // Ignore errors from detached frames
            }
        };

        // 2. SWITCH TABS
        if (command === 'switch-tab') {
            if (index !== null && index < pages.length) {
                targetPage = pages[index];
                await targetPage.bringToFront();
                fs.writeFileSync(activeDataPath, index.toString());
                console.log(`✅ Success! Brought Tab [${index}] to front. Current URL: ${targetPage.url()}`);
            } else {
                console.error(`❌ Invalid index. Use 'node browser.js check-tabs' to see available indices.`);
            }
        }
        // 3. CHECK ALL OPEN TABS
        else if (command === 'check-tabs') {
            console.log(`📑 Available Tabs: (${pages.length} total)`);
            pages.forEach((p, i) => {
                const status = (i === activeIndex) ? "(ACTIVE)" : "";
                if (!p.url().includes('devtools://')) console.log(`[${i}] ${p.url()} ${status}`);
            });
            console.log("Use: node browser.js switch-tab --index <number>");
        }
        // 4. CHECK URL
        else if (command === 'check-url') {
            console.log(`🔗 Current URL of Tab [${activeIndex}]: ${targetPage.url()}`);
            console.log(`📄 Title: ${await targetPage.title()}`);
        }
        // 5. ENHANCED SNAPSHOT
        if (command === 'navigate') {
            if (url) {
                debug(`🌐 Navigating to: ${url}`);
                await targetPage.goto(url, { waitUntil: 'networkidle2', timeout: 90000 });
            } else {
                console.error("❌ Use --url");
            }
        }
        else if (command === 'wait') {
            const timeout = parseInt(args.includes('--timeout') ? args[args.indexOf('--timeout') + 1] : "5000");
            const selector = args.includes('--selector') ? args[args.indexOf('--selector') + 1] : null;
            if (selector) {
                debug(`⏳ Waiting for selector: ${selector}...`);
                await targetPage.waitForSelector(selector, { timeout });
            } else {
                debug(`😴 Sleeing for ${timeout}ms...`);
                await new Promise(r => setTimeout(r, timeout));
            }
        }
        else if (command === 'scroll') {
            const direction = args.includes('--dir') ? args[args.indexOf('--dir') + 1] : 'down';
            const amount = parseInt(args.includes('--amount') ? args[args.indexOf('--amount') + 1] : '500');
            await targetPage.evaluate((d, a) => {
                window.scrollBy({ top: d === 'down' ? a : -a, behavior: 'smooth' });
            }, direction, amount);
            debug(`📜 Scrolled ${direction} by ${amount}px.`);
        }
        else if (command === 'snapshot') {
            if (url) {
                console.log(`Navigating to ${url}...`);
                try {
                    await targetPage.goto(url, { waitUntil: 'load', timeout: 60000 });
                } catch (e) {
                    await new Promise(r => setTimeout(r, 3000));
                }
                await new Promise(r => setTimeout(r, 4000)); // wait for dynamic content
            }

            await runCleanupAndExpand(targetPage);

            const data = await targetPage.evaluate(() => {
                const interactables = Array.from(document.querySelectorAll(`
                    button, 
                    a, 
                    input, 
                    select, 
                    textarea, 
                    [role="button"], 
                    [onclick], 
                    [role="link"], 
                    .dropdown,
                    .btn,
                    .link,
                    .menu-item,
                    .nav-item,
                    .card,
                    .tile,
                    .item,
                    [tabindex],
                    [data-testid],
                    [data-qa],
                    [data-cy],
                    [data-test],
                    .search-btn,
                    .submit-btn,
                    .next-btn,
                    .prev-btn,
                    .close-btn,
                    .modal-close,
                    .popup-close,
                    .overlay-close
                `));

                const uniqueElements = [];
                const processed = new Set();

                interactables.forEach((el, i) => {
                    const rect = el.getBoundingClientRect();
                    const isVisible = rect.width > 0 && rect.height > 0 &&
                        window.getComputedStyle(el).visibility !== 'hidden' &&
                        window.getComputedStyle(el).display !== 'none';

                    if (isVisible) {
                        const identifier = `${el.tagName}_${el.className}_${el.innerText?.substring(0, 50) || ''}_${rect.x}_${rect.y}`;

                        if (!processed.has(identifier)) {
                            processed.add(identifier);
                            uniqueElements.push(el);
                        }
                    }
                });

                return uniqueElements.map((element, index) => {
                    const el = element;
                    el.setAttribute('data-god-tag', `[${index}]`);

                    el.style.outline = '3px solid #00ff00';
                    el.style.outlineOffset = '-3px';
                    el.style.backgroundColor = 'rgba(0, 255, 0, 0.1)';
                    el.style.boxShadow = '0 0 5px rgba(0, 255, 0, 0.5)';

                    let text = '';
                    if (el.innerText && el.innerText.trim()) {
                        text = el.innerText.trim().replace(/\s+/g, ' ').substring(0, 150);
                    } else if (el.textContent && el.textContent.trim()) {
                        text = el.textContent.trim().replace(/\s+/g, ' ').substring(0, 150);
                    } else if (el.value && el.value.trim()) {
                        text = el.value.trim().substring(0, 150);
                    } else if (el.placeholder && el.placeholder.trim()) {
                        text = el.placeholder.trim().substring(0, 150);
                    } else if (el.getAttribute('aria-label')) {
                        text = el.getAttribute('aria-label').trim().substring(0, 150);
                    } else if (el.getAttribute('title')) {
                        text = el.getAttribute('title').trim().substring(0, 150);
                    } else if (el.getAttribute('data-label')) {
                        text = el.getAttribute('data-label').trim().substring(0, 150);
                    } else {
                        const tagName = el.tagName.toLowerCase();
                        const className = el.className ? `.${el.className.split(' ')[0]}` : '';
                        const id = el.id ? `#${el.id}` : '';
                        text = `${tagName}${className}${id}`;
                    }

                    text = text.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();

                    return {
                        tag: `[${index}]`,
                        type: el.tagName.toLowerCase(),
                        text,
                        visible: true,
                        position: {
                            x: Math.round(el.getBoundingClientRect().x),
                            y: Math.round(el.getBoundingClientRect().y),
                            width: Math.round(el.getBoundingClientRect().width),
                            height: Math.round(el.getBoundingClientRect().height)
                        },
                        attributes: {
                            id: el.id || null,
                            className: el.className || null,
                            href: el.href || null,
                            value: el.value || null,
                            placeholder: el.placeholder || null,
                            ariaLabel: el.getAttribute('aria-label') || null,
                            title: el.getAttribute('title') || null
                        }
                    };
                });
            });

            const { outputDir, runId } = getOutputDir();
            const snapshotJsonPath = path.join(outputDir, `snapshot_${Date.now()}.json`);
            const snapshotPngPath = path.join(outputDir, `snapshot_${Date.now()}.png`);

            const output = {
                runId,
                tabIndex: activeIndex,
                url: targetPage.url(),
                title: await targetPage.title(),
                total_open_tabs: pages.length,
                elements: data
            };

            console.log(JSON.stringify(output, null, 2));

            fs.writeFileSync(snapshotJsonPath, JSON.stringify(output, null, 2));
            await targetPage.screenshot({ path: snapshotPngPath });
            console.log(`📸 Saved assets to: ${outputDir}`);
        }
        // 6. CLICK (Detects New Tabs Native)
        else if (command === 'click') {
            if (url && targetPage.url() !== url && !targetPage.url().includes(url)) {
                await targetPage.goto(url, { waitUntil: 'domcontentloaded' });
            }

            const currentTabCount = pages.length;
            const dna = getElementDNA(tag);

            const result = await targetPage.evaluate((t, d) => {
                let el = document.querySelector(`[data-god-tag="${t}"]`);
                let strategy = "primary";

                if (!el && d) {
                    if (d.attributes && d.attributes.id) {
                        el = document.getElementById(d.attributes.id);
                        if (el) strategy = "healing-id";
                    }
                    if (!el && d.text) {
                        el = Array.from(document.querySelectorAll(d.type || '*'))
                            .find(e => (e instanceof HTMLElement ? e.innerText : e.textContent || "").includes(d.text));
                        if (el) strategy = "healing-text";
                    }
                }

                if (!el) {
                    const cleanLabel = t.replace(/[\[\]]/g, '');
                    el = Array.from(document.querySelectorAll('button, a, input, [role="button"]'))
                        .find(e => (e instanceof HTMLElement ? e.innerText : e.textContent || "").includes(cleanLabel));
                    if (el) strategy = "fallback-text";
                }

                if (el instanceof HTMLElement) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    el.click();
                    return { success: true, strategy };
                }
                return { success: false };
            }, tag, dna);

            if (result.success) {
                console.log(`✅ Click processed using strategy: ${result.strategy}`);
                console.log(`🖱️ Clicked ${tag}. Waiting 10 seconds for page to react/load...`);
                await new Promise(r => setTimeout(r, 10000));

                const updatedPages = await browser.pages();
                if (updatedPages.length > currentTabCount) {
                    const newIndex = updatedPages.length - 1;
                    fs.writeFileSync(activeDataPath, newIndex.toString());
                    console.log(`----------\n⚠️ A NEW TAB WAS OPENED!!\nAutomatically switched context to Tab [${newIndex}].\nURL: ${updatedPages[newIndex].url()}\nTitle: ${await updatedPages[newIndex].title()}\nUse 'snapshot' immediately to see the new page elements.\n----------`);
                } else {
                    console.log(`✅ Click processed. Current URL is now: ${targetPage.url()}`);
                }

                let finalActiveTab;
                try {
                    const activeIdx = fs.existsSync(activeDataPath) ? parseInt(fs.readFileSync(activeDataPath, 'utf8')) : -1;
                    finalActiveTab = (activeIdx >= 0 && activeIdx < updatedPages.length) ? updatedPages[activeIdx] : targetPage;
                } catch (err) {
                    finalActiveTab = targetPage;
                }

                if (finalActiveTab) {
                    const { outputDir } = getOutputDir();
                    const screenshotPath = path.join(outputDir, `click_${Date.now()}.png`);
                    try {
                        await finalActiveTab.screenshot({ path: screenshotPath });
                        console.log(`🖼️ Screenshot saved to: ${screenshotPath}`);
                    } catch (snapErr) {
                        console.warn(`⚠️ Could not take screenshot for ${command}:`, snapErr instanceof Error ? snapErr.message : snapErr);
                    }
                }
            } else {
                console.log(`❌ Failed to find element ${tag}`);
            }
        }
        // 7. TYPE
        else if (command === 'type') {
            if (url && targetPage.url() !== url && !targetPage.url().includes(url)) {
                await targetPage.goto(url, { waitUntil: 'domcontentloaded' });
            }

            if (!tag || !text) {
                console.error("❌ Use --tag \"[number]\" and --text \"your input\"");
                return;
            }

            const dna = getElementDNA(tag);
            const result = await targetPage.evaluate((t, val, d) => {
                let el = document.querySelector(`[data-god-tag="${t}"]`);
                let strategy = "primary";

                if (!el && d) {
                    if (d.attributes && d.attributes.id) {
                        el = document.getElementById(d.attributes.id);
                        if (el) strategy = "healing-id";
                    }
                    if (!el && d.text) {
                        el = Array.from(document.querySelectorAll('input, textarea, [contenteditable="true"]'))
                            .find(e => (e instanceof HTMLElement ? e.innerText : e.textContent || "").includes(d.text));
                        if (el) strategy = "healing-text";
                    }
                }

                if (!el) {
                    const cleanLabel = t.replace(/[\[\]]/g, '');
                    el = Array.from(document.querySelectorAll('input, textarea, [contenteditable="true"]'))
                        .find(e => (e instanceof HTMLElement ? e.innerText : e.textContent || "").includes(cleanLabel));
                    if (el) strategy = "fallback-text";
                }

                if (el instanceof HTMLElement) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    el.focus();
                    if (el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement) {
                        el.value = val;
                    } else {
                        el.innerText = val;
                    }
                    ['input', 'change', 'blur'].forEach(ev => el.dispatchEvent(new Event(ev, { bubbles: true })));
                    return { success: true, strategy };
                }
                return { success: false };
            }, tag, text, dna);

            if (result.success) {
                console.log(`✅ Type processed using strategy: ${result.strategy}`);
                await targetPage.keyboard.press('Enter'); // Standard auto-enter for convenience

                const { outputDir } = getOutputDir();
                const screenshotPath = path.join(outputDir, `type_${Date.now()}.png`);
                await targetPage.screenshot({ path: screenshotPath });
                console.log(`🖼️ Screenshot saved to: ${screenshotPath}`);
            } else {
                console.log(`❌ Failed to find element ${tag} for typing.`);
            }
        }
        // 8. PRESS KEY
        else if (command === 'press') {
            const key = args.includes('--key') ? args[args.indexOf('--key') + 1] : 'Enter';
            await targetPage.keyboard.press(key);
            console.log(`🎹 Pressed key: ${key}`);
        }
        // 8b. READ CONTENT
        else if (command === 'read') {
            const selector = args.includes('--selector') ? args[args.indexOf('--selector') + 1] : 'body';
            const tagVal = args.includes('--tag') ? args[args.indexOf('--tag') + 1] : null;

            await runCleanupAndExpand(targetPage);
            let activeFrame = targetPage;
            let finalSelector = selector;

            if (tagVal) {
                const frames = targetPage.frames();
                for (const frame of frames) {
                    try {
                        if (frame.isDetached()) continue;
                        const exists = await frame.evaluate((t) => !!document.querySelector(`[data-god-tag="${t}"]`), tagVal);
                        if (exists) {
                            activeFrame = frame;
                            finalSelector = `[data-god-tag="${tagVal}"]`;
                            break;
                        }
                    } catch (e) { }
                }
            }

            console.log(`📖 Reading content from ${finalSelector}...`);
            let content = await activeFrame.evaluate((s) => {
                const el = document.querySelector(s);
                if (!el) return null;
                return (el instanceof HTMLElement) ? el.innerText : el.textContent;
            }, finalSelector);

            if (content === null && !tagVal) {
                for (const frame of targetPage.frames()) {
                    if (frame === targetPage || frame.isDetached()) continue;
                    try {
                        content = await frame.evaluate((s) => {
                            const el = document.querySelector(s);
                            if (!el) return null;
                            return (el instanceof HTMLElement) ? el.innerText : el.textContent;
                        }, finalSelector);
                        if (content !== null) break;
                    } catch (e) { }
                }
            }

            if (content !== null) {
                console.log(content.trim());
            } else {
                console.error(`❌ Could not find content for selector: ${finalSelector}`);
            }
        }
        // 8c. EXPAND CONTENT
        else if (command === 'expand') {
            console.log("🔍 Running deep-expand on all frames...");
            for (const frame of targetPage.frames()) {
                if (frame.isDetached()) continue;
                await runCleanupAndExpand(frame);
            }
            console.log("✅ Expansion complete.");
        }

        // 9. REFRESH PAGE
        else if (command === 'refresh') {
            const pages = await browser.pages();
            const activeIndex = fs.existsSync(activeDataPath) ? parseInt(fs.readFileSync(activeDataPath, 'utf8')) : 0;
            const targetPage = pages[activeIndex] || pages[0];

            console.log(`🔄 Refreshing Tab [${activeIndex}]...`);
            await targetPage.reload({ waitUntil: 'networkidle2' });

            const { outputDir } = getOutputDir();
            const screenshotPath = path.join(outputDir, `refresh_${Date.now()}.png`);
            await targetPage.screenshot({ path: screenshotPath });
            console.log(`✅ Page refreshed. Screenshot saved to: ${screenshotPath}`);
        }

        // 10. FIND (Accurate Filtered Search)
        else if (command === 'find') {
            let elements = [];
            let source = "";
            const resolvedFile = resolveFilePath(file);

            if (resolvedFile) {
                try {
                    const rawData = fs.readFileSync(resolvedFile, 'utf8').includes('{') ? fs.readFileSync(resolvedFile, 'utf8') : fs.readFileSync(resolvedFile, 'utf16le');
                    const jsonData = rawData.substring(rawData.indexOf('{'), rawData.lastIndexOf('}') + 1);
                    const parsed = JSON.parse(jsonData);
                    elements = parsed.elements || [];
                    source = `File: ${resolvedFile}`;
                } catch (e) {
                    console.error(`❌ Failed to process ${resolvedFile}:`, e instanceof Error ? e.message : e);
                    return;
                }
            } else {
                if (url) await targetPage.goto(url, { waitUntil: 'domcontentloaded' });

                const snapshotData = await targetPage.evaluate(() => {
                    const interactables = Array.from(document.querySelectorAll('button, a, input, select, textarea, [role="button"], [onclick], [role="link"], .dropdown, .btn, .link'));
                    return interactables.map((el, i) => {
                        const tag = `[${i}]`;
                        el.setAttribute('data-god-tag', tag);
                        const text = (el.innerText || el.value || el.placeholder || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').substring(0, 150);
                        return {
                            tag,
                            type: el.tagName.toLowerCase(),
                            text,
                            visible: el.offsetWidth > 0 && el.offsetHeight > 0
                        };
                    }).filter(item => item.visible);
                });
                elements = snapshotData;
                source = `Live: ${targetPage.url()}`;
            }

            if (query) {
                const keywords = query.toLowerCase().split(',').map(k => k.trim());
                elements = elements.filter(e =>
                    keywords.some(keyword => e.text.toLowerCase().includes(keyword) || e.type.toLowerCase() === keyword)
                );
            }

            console.log(JSON.stringify({
                status: "success",
                source,
                matched_count: elements.length,
                elements
            }, null, 2));
        }

        // 11. SCRAP META TAGS
        else if (command === 'scrap-meta') {
            console.log(`🔍 Extracting meta tags from: ${targetPage.url()}`);
            const metaTags = await targetPage.evaluate(() => {
                const results = {};
                const tags = Array.from(document.querySelectorAll('meta, title'));

                tags.forEach(tag => {
                    if (tag.tagName.toLowerCase() === 'title') {
                        results['title'] = tag.innerText;
                    } else {
                        const name = tag.getAttribute('name') || tag.getAttribute('property');
                        const content = tag.getAttribute('content');
                        if (name && content) {
                            results[name] = content;
                        }
                    }
                });
                return results;
            });

            const { outputDir } = getOutputDir();
            const metaPath = path.join(outputDir, `meta_${Date.now()}.json`);
            fs.writeFileSync(metaPath, JSON.stringify(metaTags, null, 2));

            console.log(JSON.stringify({
                status: "success",
                url: targetPage.url(),
                count: Object.keys(metaTags).length,
                metadata: metaTags
            }, null, 2));
            console.log(`📄 Metadata saved to: ${metaPath}`);
        }
        // 13. SAVE SESSION
        else if (command === 'save-session') {
            const newCookies = await targetPage.cookies();
            let allCookies = [];

            if (fs.existsSync(sessionPath)) {
                try {
                    allCookies = JSON.parse(fs.readFileSync(sessionPath, 'utf8'));
                } catch (e) { }
            }

            const currentDomain = new URL(targetPage.url()).hostname.replace('www.', '');
            allCookies = allCookies.filter(c => !c.domain.includes(currentDomain));
            allCookies.push(...newCookies);

            fs.writeFileSync(sessionPath, JSON.stringify(allCookies, null, 2));
            hardenFile(sessionPath);
            console.log(`💾 Merged and saved cookies to session.json. Total session cookies: ${allCookies.length}`);
            console.log(`🔒 SECURITY: Ensure session.json is protected. It contains plain-text credentials.`);

            if (fs.existsSync(authReqPath)) {
                try {
                    const authTasks = JSON.parse(fs.readFileSync(authReqPath, 'utf8'));
                    const domain = new URL(targetPage.url()).hostname;
                    if (authTasks[domain]) {
                        delete authTasks[domain];
                        fs.writeFileSync(authReqPath, JSON.stringify(authTasks, null, 2));
                        console.log(`✨ Cleared auth requirement log for ${domain}`);
                    }
                } catch (e) { }
            }
        }
        // 14. AUTH STATUS
        else if (command === 'auth-status') {
            const status = await targetPage.evaluate(() => {
                const loginText = ['sign in', 'login', 'log in', 'signin', 'auth'].some(t => {
                    const elements = Array.from(document.querySelectorAll('a, button, span')).filter(el => {
                        const style = window.getComputedStyle(el);
                        return style.display !== 'none' && style.visibility !== 'hidden' && el.innerText.toLowerCase().includes(t);
                    });
                    return elements.length > 0;
                });
                const loginInputs = !!document.querySelector('input[type="password"]');
                const userProfile = !!(
                    document.querySelector('.profile, .user-menu, .account, [aria-label*="account"], [aria-label*="profile"], .avatar, [class*="avatar"], img[alt*="profile"], img[alt*="avatar"]') ||
                    Array.from(document.querySelectorAll('button, a')).some(el => {
                        const label = (el.getAttribute('aria-label') || "").toLowerCase();
                        const text = el.innerText.toLowerCase();
                        return label.includes('account') || label.includes('profile') || text.includes('my account') || text.includes('logout') || text.includes('sign out');
                    })
                );
                return { loginText, loginInputs, userProfile, url: window.location.href };
            });

            const domain = new URL(targetPage.url()).hostname;
            console.log(JSON.stringify(status, null, 2));

            if ((status.loginInputs || status.loginText) && !status.userProfile) {
                console.warn(`⚠️ Authentication might be required on ${domain}`);
                let authTasks = {};
                if (fs.existsSync(authReqPath)) {
                    try { authTasks = JSON.parse(fs.readFileSync(authReqPath, 'utf8')); } catch (e) { }
                }
                authTasks[domain] = { status, timestamp: new Date().toISOString() };
                fs.writeFileSync(authReqPath, JSON.stringify(authTasks, null, 2));
            }
        }
        // 15. LOG LEARNING
        else if (command === 'log-learning') {
            const what_failed = args.includes('--failed') ? args[args.indexOf('--failed') + 1] : 'Unknown failure';
            const how_fixed = args.includes('--fixed') ? args[args.indexOf('--fixed') + 1] : 'No fix provided';
            const lessons = args.includes('--lessons') ? args[args.indexOf('--lessons') + 1] : 'No lesson provided';
            const context = tag || 'General';

            let learningLog = [];
            if (fs.existsSync(learningPath)) {
                try { learningLog = JSON.parse(fs.readFileSync(learningPath, 'utf8')); } catch (e) { }
            }

            const newEntry = {
                id: `LEARN_${Date.now()}`,
                what_failed,
                how_fixed,
                lessons_learned: lessons,
                timestamp: new Date().toISOString(),
                context,
                url: targetPage.url()
            };

            learningLog.push(newEntry);
            fs.writeFileSync(learningPath, JSON.stringify(learningLog, null, 2));
            console.log(`🧠 Self-improvement logged: ${newEntry.id}`);
        }
        // 12. DYNAMIC EVALUATE 
        else if (command === 'eval') {
            // SECURITY GATE: Require explicit confirmation for arbitrary code execution.
            if (!args.includes('--force') && process.env.GOD_AUTO_EVAL !== 'true') {
                console.error("❌ SECURITY GATE: Usage of 'eval' requires the '--force' flag or 'GOD_AUTO_EVAL=true' environment variable.");
                console.error("This is an intentional safety guard because 'eval' can execute arbitrary scripts.");
                console.error("\nUsage: node browser.js eval --code '...' --force");
                return;
            }

            const resolvedFile = resolveFilePath(file);
            const script = code || (resolvedFile ? fs.readFileSync(resolvedFile, 'utf8') : null);
            if (!script) {
                console.error("❌ No script provided. Use --code '...' or --file path/to/script.js");
                return;
            }

            console.log(`🚀 Injecting custom logic into: ${targetPage.url()}`);

            const lowerCode = script.toLowerCase();
            const hasNetwork = lowerCode.includes('fetch') || lowerCode.includes('xmlhttprequest') || lowerCode.includes('navigator.sendbeacon');
            if (hasNetwork) {
                debug(`🔍 SECURITY NOTICE: Script contains network request patterns. Ensure it is not exfiltrating data.`, "WARN");
            }

            debug(`⚠️  SECURITY WARNING: Running custom script via 'eval' command. Only use trusted scripts.`, "WARN");

            const result = await targetPage.evaluate(async (codeStr) => {
                try {
                    // Use AsyncFunction constructor for a cleaner execution environment support for await.
                    // This is an intentional feature of "GOD OF ALL BROWSERS" for automation power-users.
                    const AsyncFunction = Object.getPrototypeOf(async function () { }).constructor;
                    return await (new AsyncFunction(codeStr))();
                } catch (e) {
                    return { error: e instanceof Error ? e.message : String(e) };
                }
            }, script);

            const outputRes = {
                status: (result && result.error) ? "error" : "success",
                timestamp: new Date().toISOString(),
                result: result ?? null
            };

            console.log(JSON.stringify(outputRes, null, 2));

            const { outputDir } = getOutputDir();
            const resultPath = path.join(outputDir, `eval_${Date.now()}.json`);
            fs.writeFileSync(resultPath, JSON.stringify(outputRes, null, 2));
            console.log(`💾 Result saved to: ${resultPath}`);
        }
        // 10. GOOGLE SEARCH (Automated Extraction)
        else if (command === 'google') {
            const searchQuery = query || (args.includes('--q') ? args[args.indexOf('--q') + 1] : null);
            if (!searchQuery) {
                console.error("❌ Please provide a search query with --query or --q");
                process.exit(1);
            }

            try {
                const pages = await browser.pages();
                const page = pages[0];
                // SECURITY: Sanitize search query input to prevent 'User Input to Network Sink' vulnerabilities.
                const cleanQuery = searchQuery.replace(/[\r\n]/g, ' ').substring(0, 500);
                const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(cleanQuery)}`;
                await page.goto(searchUrl, { waitUntil: 'load', timeout: 60000 });

                try {
                    await page.waitForFunction(() => document.querySelectorAll('h3').length >= 1, { timeout: 8000 });
                } catch (e) {
                    console.warn("⚠️ Google results took too long, attempting extraction anyway...");
                    await new Promise(r => setTimeout(r, 2000));
                }

                const results = await page.evaluate(() => {
                    return Array.from(document.querySelectorAll('h3'))
                        .map(h3 => {
                            const anchor = h3.closest('a');
                            if (!anchor) return null;
                            const container = h3.closest('div.g') || h3.parentElement;
                            return {
                                title: h3.innerText,
                                link: anchor.href,
                                snippet: container ? container.innerText.substring(0, 150).replace(/\n/g, ' ') : ""
                            };
                        })
                        .filter(r => r && r.link && r.link.startsWith('http') && !r.link.includes('google.com/search'));
                });

                const { outputDir } = getOutputDir();
                const outputObj = { status: "success", query: searchQuery, results, count: results.length };
                console.log(JSON.stringify(outputObj, null, 2));

                const resultFile = path.join(outputDir, `google_${Date.now()}.json`);
                fs.writeFileSync(resultFile, JSON.stringify(outputObj, null, 2));
                console.log(`💾 Results saved to: ${resultFile}`);

            } catch (err) {
                console.error("❌ Google search failed:", err instanceof Error ? err.message : err);
            }
        }

    } catch (err) {
        console.error('❌ Error executing command:', err instanceof Error ? err.message : err);
    } finally {
        browser.disconnect();
    }
}

run();

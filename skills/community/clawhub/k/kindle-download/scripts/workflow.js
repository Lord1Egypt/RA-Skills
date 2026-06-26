const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const os = require("os");
const sanitize = require("./sanitize");

// 配置文件路径（使用用户主目录下的安全位置）
const homeDir = os.homedir();
const configDir = path.join(homeDir, ".config", "kindle-download");
const SKILL_ROOT = path.join(homeDir, ".openclaw", "workspace", "skills", "kindle-download");

/**
 * 从环境变量或配置文件读取凭证
 * 环境变量优先级高于配置文件
 */
function getCredentials() {
    // 首先尝试从环境变量读取
    const envCredentials = {
        email: process.env.KINDLE_SMTP_EMAIL,
        auth_code: process.env.KINDLE_SMTP_AUTH_CODE,
        send_kindle_email: process.env.KINDLE_RECEIVER_EMAIL,
        library_account_email: process.env.KINDLE_ZLIB_EMAIL,
        library_password: process.env.KINDLE_ZLIB_PASSWORD,
        proxy_server: process.env.KINDLE_PROXY_SERVER || "",
        smtp_server: process.env.KINDLE_SMTP_SERVER || "smtp.163.com",
        smtp_port: parseInt(process.env.KINDLE_SMTP_PORT) || 465
    };
    
    // 检查是否所有必需的环境变量都已设置
    const requiredEnvVars = ["email", "auth_code", "send_kindle_email", "library_account_email", "library_password"];
    const hasAllEnvVars = requiredEnvVars.every(key => envCredentials[key]);
    
    if (hasAllEnvVars) {
        console.log("LOG: 使用环境变量中的凭证配置");
        return envCredentials;
    }
    
    // 否则从配置文件读取
    console.log("LOG: 从配置文件读取凭证");
    
    // 配置文件路径（优先从用户配置目录读取，兼容旧位置）
    function getConfigPath(filename) {
        const userConfigPath = path.join(configDir, filename);
        const skillConfigPath = path.join(SKILL_ROOT, filename);
        
        // 优先使用用户配置目录
        if (fs.existsSync(userConfigPath)) {
            return userConfigPath;
        }
        
        // 兼容旧位置
        if (fs.existsSync(skillConfigPath)) {
            return skillConfigPath;
        }
        
        // 默认返回用户配置目录（即使不存在，让后续报错提示用户）
        return userConfigPath;
    }
    
    const configPath = getConfigPath("auth.json");
    
    let fileConfig = {};
    try {
        fileConfig = JSON.parse(fs.readFileSync(configPath, "utf-8"));
    } catch (e) {
        console.error("ERROR: 无法读取 auth.json: " + e.message);
        console.error("LOG: 请确保配置文件存在于: " + configPath);
        console.error("LOG: 或者设置以下环境变量：");
        console.error("LOG:   KINDLE_SMTP_EMAIL, KINDLE_SMTP_AUTH_CODE, KINDLE_RECEIVER_EMAIL");
        console.error("LOG:   KINDLE_ZLIB_EMAIL, KINDLE_ZLIB_PASSWORD");
        process.exit(1);
    }
    
    // 合并环境变量和文件配置（环境变量优先）
    return {
        email: envCredentials.email || fileConfig.email,
        auth_code: envCredentials.auth_code || fileConfig.auth_code,
        send_kindle_email: envCredentials.send_kindle_email || fileConfig.send_kindle_email,
        library_account_email: envCredentials.library_account_email || fileConfig.library_account_email,
        library_password: envCredentials.library_password || fileConfig.library_password,
        proxy_server: envCredentials.proxy_server || fileConfig.proxy_server || "",
        smtp_server: envCredentials.smtp_server || fileConfig.smtp_server || "smtp.163.com",
        smtp_port: envCredentials.smtp_port || fileConfig.smtp_port || 465
    };
}

const config = getCredentials();
const urlConfigPath = path.join(SKILL_ROOT, "zlibraryUrl.json");

// 下载目录（使用系统临时目录，跨平台兼容）
const saveDir = path.join(os.tmpdir(), "kindle_downloads");
const stateFile = path.join(saveDir, "workflow_state.json");
const browserStateFile = path.join(saveDir, "browser_state.json");

// 确保配置目录存在
if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
}
if (!fs.existsSync(saveDir)) fs.mkdirSync(saveDir, { recursive: true });

let urls = [];
try {
    urls = JSON.parse(fs.readFileSync(urlConfigPath, "utf-8"));
} catch (e) {
    console.error("ERROR: 无法读取 zlibraryUrl.json: " + e.message);
    process.exit(1);
}

if (!Array.isArray(urls) || urls.length === 0) {
    console.error("ERROR: zlibraryUrl.json 内容有误或为空");
    process.exit(1);
}

// ===== 安全输入验证 =====
const rawBookName = process.argv[2];
if (!rawBookName) {
    console.error("ERROR: MISSING_BOOK_NAME");
    process.exit(1);
}

// 验证书名
const titleResult = sanitize.validateBookTitle(rawBookName);
if (!titleResult.valid) {
    console.error("ERROR: INVALID_BOOK_TITLE: " + titleResult.error);
    process.exit(1);
}
const bookName = titleResult.sanitized;

// 验证过滤器
let filters = {};
try {
    if (process.argv[3]) {
        let rawFilters = process.argv[3].trim();
        if (rawFilters.startsWith("{") && rawFilters.endsWith("}")) {
            // 尝试解析 JSON，处理可能的格式问题
            const processed = rawFilters
                .replace(/([{,]\s*)([a-zA-Z0-9_]+)\s*:/g, '"$1"$2":')
                .replace(/:\s*([^"{}\[\],]+)([,}])?/g, function(match, p1, p2) {
                    return ':"' + p1.trim() + '"' + (p2 || "");
                });
            try {
                filters = JSON.parse(processed);
            } catch(e) {
                filters = JSON.parse(rawFilters);
            }
        } else {
            filters = JSON.parse(rawFilters);
        }
    }
} catch(e) {}

// 安全验证过滤器
const filtersResult = sanitize.validateFilters(filters);
if (!filtersResult.valid && filtersResult.errors.length > 0) {
    console.error("ERROR: INVALID_FILTERS: " + filtersResult.errors.join(", "));
    process.exit(1);
}
filters = filtersResult.sanitized;

// 检查是否有保存的状态（用于用户选择后继续）
let savedState = null;
if (fs.existsSync(stateFile)) {
    try {
        savedState = JSON.parse(fs.readFileSync(stateFile, "utf-8"));
        if (savedState.bookName !== bookName) {
            savedState = null;
            fs.unlinkSync(stateFile);
            if (fs.existsSync(browserStateFile)) fs.unlinkSync(browserStateFile);
        }
    } catch(e) {
        savedState = null;
    }
}

// 浏览器启动配置（自动检测 Chromium）
async function getBrowserConfig() {
    const browserArgs = ["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"];
    
    // 代理配置（从 auth.json 读取，如果没有则不使用代理）
    const browserConfig = { args: browserArgs, headless: true };
    
    // 如果配置了代理，则使用代理
    if (config.proxy_server) {
        browserConfig.proxy = { server: config.proxy_server };
    }
    
    // 尝试自动检测 Chromium 路径
    const possiblePaths = [
        // Linux
        path.join(homeDir, ".cache/ms-playwright/chromium-1208/chrome-linux/chrome"),
        path.join(homeDir, ".cache/ms-playwright/chromium-1169/chrome-linux/chrome"),
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        // macOS
        path.join(homeDir, "Library/Caches/ms-playwright/chromium-1208/chrome-mac/Chromium.app/Contents/MacOS/Chromium"),
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        // Windows
        path.join(process.env.LOCALAPPDATA || "", "ms-playwright/chromium-1208/chrome-win/chrome.exe"),
        path.join(process.env.PROGRAMFILES || "", "Google/Chrome/Application/chrome.exe"),
        path.join(process.env["PROGRAMFILES(X86)"] || "", "Google/Chrome/Application/chrome.exe"),
    ];
    
    for (const p of possiblePaths) {
        if (p && fs.existsSync(p)) {
            browserConfig.executablePath = p;
            break;
        }
    }
    
    return browserConfig;
}

async function run() {
    const browserConfig = await getBrowserConfig();
    const browser = await chromium.launch(browserConfig);
    
    // 如果有保存的浏览器状态，使用它
    let context;
    if (savedState && fs.existsSync(browserStateFile)) {
        try {
            context = await browser.newContext({
                storageState: browserStateFile,
                userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            });
            console.log("LOG: 恢复之前的浏览器登录态...");
        } catch(e) {
            context = await browser.newContext({
                userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            });
        }
    } else {
        context = await browser.newContext({
            userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        });
    }
    
    const page = await context.newPage();
    
    try {
        let baseUrl = savedState?.baseUrl || "";
        
        if (!baseUrl) {
            for (const url of urls) {
                try {
                    console.log("LOG: 尝试访问 " + url);
                    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
                    await page.waitForTimeout(5000);
                    
                    const title = await page.title();
                    if (title && !title.includes("Checking your browser")) {
                        console.log("LOG: 成功进入站点: " + page.url());
                        baseUrl = page.url().split("/s/")[0].split("/book/")[0];
                        if (!baseUrl.endsWith("/")) baseUrl += "/";
                        break;
                    }
                } catch (e) {}
            }
        }
        
        if (!baseUrl) throw new Error("ALL_MIRRORS_UNAVAILABLE");
        
        const checkLogin = async () => {
            return await page.evaluate(() => {
                return !!document.querySelector(".userAccount, a[href*=\"/profile/\"], .profile-link");
            });
        };
        
        // 如果没有保存的状态或没有恢复登录态，需要重新登录
        if (!savedState || !fs.existsSync(browserStateFile)) {
            if (!(await checkLogin())) {
                const loginBtn = await page.$("a[href*=\"login\"], .login-btn, a:has-text(\"登录\"), a:has-text(\"Log In\")");
                if (loginBtn) {
                    await loginBtn.click();
                    await page.waitForSelector("#zlibrary-modal-auth input[name=\"email\"]", { timeout: 15000 });
                    await page.fill("#zlibrary-modal-auth input[name=\"email\"]", config.library_account_email);
                    await page.fill("#zlibrary-modal-auth input[name=\"password\"]", config.library_password);
                    await page.click("#zlibrary-modal-auth button[type=\"submit\"]");
                    await page.waitForTimeout(10000);
                }
            }
        }
        
        console.log("PROGRESS: 第一步登录已完成。");
        
        // 保存浏览器登录态
        await context.storageState({ path: browserStateFile });
        console.log("LOG: 浏览器登录态已保存");
        
        let results = savedState?.results || [];
        
        if (!savedState) {
            console.log("LOG: 搜索书籍: " + bookName);
            
            // 使用 encodeURLComponent 对清理后的书名进行编码
            await page.goto(baseUrl + "s/" + encodeURIComponent(bookName), { waitUntil: "networkidle" });
            await page.waitForSelector("z-bookcard, .book-item, .resItemBox", { timeout: 20000 });
            
            const searchResultImg = path.join(saveDir, "last_search_result.png");
            await page.screenshot({ path: searchResultImg, fullPage: true });
            console.log("LOG: 搜索结果截图已保存至 " + searchResultImg);
            
            // 使用对象包装参数，符合 Playwright 的 API 要求
            results = await page.evaluate(({ searchFilters, searchTitle }) => {
                const items = Array.from(document.querySelectorAll("z-bookcard, .book-item, .resItemBox, div[class*=\"resItemBox\"]"));
                return items.map(function(el) {
                    let href, rating, publisher, language, author, titleText;
                    
                    if (el.tagName.toLowerCase() === "z-bookcard") {
                        href = el.getAttribute("href");
                        rating = parseFloat(el.getAttribute("rating")) || 0;
                        publisher = el.getAttribute("publisher") || "";
                        language = el.getAttribute("language") || "";
                        titleText = el.getAttribute("title") || el.querySelector("div[slot=\"title\"]")?.innerText || el.querySelector("h3")?.innerText || "";
                        author = el.getAttribute("author") || el.getAttribute("authors") || el.querySelector("div[slot=\"author\"]")?.innerText || el.querySelector("a[href*=\"/author/\"]")?.innerText || "";
                    } else {
                        const a = el.querySelector("a[href*=\"/book/\"]");
                        href = a?.getAttribute("href");
                        titleText = a?.innerText || "";
                        
                        const rEl = el.querySelector(".stars, .rating, [rating]");
                        rating = parseFloat(rEl?.innerText || rEl?.getAttribute("rating")) || 0;
                        
                        const pEl = el.querySelector(".publisher, [publisher]");
                        publisher = pEl?.innerText || pEl?.getAttribute("publisher") || "";
                        
                        const lEl = el.querySelector(".language, [language]");
                        language = lEl?.innerText || lEl?.getAttribute("language") || "";
                        
                        const authEl = el.querySelector(".authors, a[href*=\"/author/\"], [author]");
                        author = authEl?.innerText || authEl?.getAttribute("author") || authEl?.getAttribute("authors") || "";
                    }
                    
                    return { href: href, rating: rating, publisher: publisher, language: language, author: author, titleText: titleText };
                }).filter(function(i) { return i.href; });
            }, { searchFilters: filters, searchTitle: bookName });
        }
        
        let filtered = results.filter(function(i) { return i.titleText.toLowerCase().includes(bookName.toLowerCase()); });
        
        if (filters.author) {
            filtered = filtered.filter(function(i) { return i.author && i.author.toLowerCase().includes(filters.author.toLowerCase()); });
        }
        if (filters.publisher) {
            filtered = filtered.filter(function(i) { return i.publisher && i.publisher.toLowerCase().includes(filters.publisher.toLowerCase()); });
        }
        if (filters.language) {
            filtered = filtered.filter(function(i) { return i.language && i.language.toLowerCase().includes(filters.language.toLowerCase()); });
        }
        
        // 检查是否需要用户选择
        const hasAuthor = !!filters.author;
        const hasPublisher = !!filters.publisher;
        
        if (!hasAuthor && !hasPublisher && filtered.length > 1) {
            const uniqueAuthors = [...new Set(filtered.map(function(i) { return i.author; }).filter(function(a) { return a; }))];
            const uniquePublishers = [...new Set(filtered.map(function(i) { return i.publisher; }).filter(function(p) { return p; }))];
            
            if (uniqueAuthors.length > 1 || uniquePublishers.length > 1) {
                console.log("NEED_SELECTION: 搜索结果包含多个不同的作者或出版社，请选择。");
                console.log("LOG: 唯一作者列表: " + uniqueAuthors.join(", "));
                console.log("LOG: 唯一出版社列表: " + uniquePublishers.join(", "));
                console.log("PROGRESS: 第二步查找书籍已完成。");
                console.log("SCREENSHOT_SENT: 请查看截图并告诉我您选择的作者或出版社。");
                
                // 保存状态
                const state = {
                    bookName: bookName,
                    baseUrl: baseUrl,
                    results: results,
                    browserStateFile: browserStateFile,
                    timestamp: Date.now()
                };
                fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
                console.log("LOG: 已保存浏览器登录态和搜索状态");
                console.log("SAVE_DIR:" + saveDir);
                console.log("SEARCH_RESULTS_JSON:" + JSON.stringify(filtered.slice(0, 10).map(function(r) {
                    return { title: r.titleText, author: r.author, publisher: r.publisher, rating: r.rating };
                })));
                
                await browser.close();
                return;
            }
        }
        
        if (filtered.length === 0) {
            if (fs.existsSync(stateFile)) fs.unlinkSync(stateFile);
            if (fs.existsSync(browserStateFile)) fs.unlinkSync(browserStateFile);
            throw new Error("NO_MATCHING_BOOK");
        }
        
        // 清理状态文件
        if (fs.existsSync(stateFile)) fs.unlinkSync(stateFile);
        
        filtered.sort(function(a, b) { return b.rating - a.rating; });
        const bestBook = filtered[0];
        
        console.log("LOG: 选中书籍: " + bestBook.titleText + " (Author: " + bestBook.author + ", Publisher: " + bestBook.publisher + ")");
        console.log("PROGRESS: 第二步查找书籍已完成。");
        
        const detailUrl = (bestBook.href.startsWith("http") ? bestBook.href : (baseUrl.endsWith("/") ? baseUrl.slice(0, -1) : baseUrl) + bestBook.href);
        
        if (savedState) {
            await page.goto(baseUrl + "s/" + encodeURIComponent(bookName), { waitUntil: "networkidle" });
        }
        
        await page.goto(detailUrl, { waitUntil: "networkidle" });
        
        const detailPageImg = path.join(saveDir, "detail_page.png");
        await page.screenshot({ path: detailPageImg, fullPage: true });
        
        const mainDlBtn = await page.waitForSelector("a[href*=\"/dl/\"], .addDownloadedBook, .download-button", { timeout: 30000 });
        const btnText = await mainDlBtn.innerText();
        
        let targetDownloadUrl = null;
        
        if (btnText.toUpperCase().includes("EPUB")) {
            targetDownloadUrl = await mainDlBtn.getAttribute("href");
        } else {
            const dropdownToggle = await page.$(".dropdown-toggle, .btn-group .dropdown-toggle, .other-formats-btn");
            if (dropdownToggle) {
                await dropdownToggle.click();
                await page.waitForSelector(".dropdown-menu a", { timeout: 5000 });
                
                const epubLink = await page.$(".dropdown-menu a:has-text(\"EPUB\"), .dropdown-menu a[href*=\"epub\"]");
                if (epubLink) {
                    targetDownloadUrl = await epubLink.getAttribute("href");
                } else {
                    const pdfLink = await page.$(".dropdown-menu a:has-text(\"PDF\"), .dropdown-menu a[href*=\"pdf\"]");
                    if (pdfLink) {
                        targetDownloadUrl = await pdfLink.getAttribute("href");
                    }
                }
            }
        }
        
        if (!targetDownloadUrl) {
            targetDownloadUrl = await mainDlBtn.getAttribute("href");
        }
        
        console.log("LOG: 开始下载: " + targetDownloadUrl);
        
        const downloadPromise = page.waitForEvent("download", { timeout: 120000 });
        let download;
        
        try {
            await page.goto(baseUrl + targetDownloadUrl.replace(/^\//, ""));
            download = await downloadPromise;
        } catch (e) {
            await mainDlBtn.click();
            download = await downloadPromise;
        }
        
        let finalFilename = download.suggestedFilename();
        const savePath = path.join(saveDir, finalFilename);
        await download.saveAs(savePath);
        
        // 验证下载的文件路径安全性
        const pathValidation = sanitize.validateFilePath(savePath);
        if (!pathValidation.valid) {
            throw new Error("INVALID_DOWNLOAD_PATH: " + pathValidation.error);
        }
        
        console.log("SUCCESS_FILE_PATH:" + pathValidation.sanitized);
        console.log("PROGRESS: 第三步下载书籍已完成。");
        
        // 清理浏览器状态文件
        if (fs.existsSync(browserStateFile)) fs.unlinkSync(browserStateFile);
        
    } catch (e) {
        console.error("ERROR: " + e.message);
        
        if (e.message !== "MISSING_BOOK_NAME") {
            const errorImg = path.join(saveDir, "last_error.png");
            try {
                await page.screenshot({ path: errorImg, fullPage: true });
                console.log("LOG: 错误截图已保存至 " + errorImg);
            } catch(se) {}
        }
        
        process.exit(1);
    } finally {
        await browser.close();
    }
}

run();

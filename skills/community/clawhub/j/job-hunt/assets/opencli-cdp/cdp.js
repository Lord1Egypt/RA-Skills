/**
 * CDP client — implements IPage by connecting directly to a Chrome/Electron CDP WebSocket.
 *
 * Fixes applied:
 * - send() now has a 30s timeout guard (P0 #4)
 * - goto() waits for Page.loadEventFired instead of hardcoded 1s sleep (P1 #3)
 * - Implemented scroll, autoScroll, screenshot, networkRequests (P1 #2)
 * - Shared DOM helper methods extracted to reduce duplication with Page (P1 #5)
 */
import { WebSocket } from 'ws';
import { readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { request as httpRequest } from 'node:http';
import { request as httpsRequest } from 'node:https';
import { buildEvaluateExpression } from './utils.js';
import { waitForDomStableJs } from './dom-helpers.js';
import { isRecord, saveBase64ToFile } from '../utils.js';
import { getAllElectronApps } from '../electron-apps.js';
import { CDPBasePage } from './base-page.js';
const CDP_SEND_TIMEOUT = 30_000;
// Inspect only rendered text in this client's own tab. A normal navigation
// link saying "Login" is not a login wall and must not retain every page.
export const USER_ACTION_EXPRESSION = `(() => {
    if (!document.body) return false;
    const parts = [], walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let node; (node = walker.nextNode());) {
        const p = node.parentElement;
        if (!p || p.closest('script,style,template,noscript,[hidden],[inert]')) continue;
        const style = getComputedStyle(p), range = document.createRange();
        if (style.visibility === 'hidden' || style.visibility === 'collapse' || style.display === 'none') continue;
        range.selectNodeContents(node);
        if (range.getClientRects().length) parts.push(node.textContent);
    }
    const text = parts.join(' ').replace(/\\s+/g, ' ');
    return /(?:enter|complete|solve) (?:the |this |a )?captcha|(?:verify|verifying|confirm) (?:that )?you are (?:a )?human|access denied|too many requests|please (?:sign|log) in|(?:sign|log) in (?:required|to continue|to view)|(?:请输入|请完成|请填写).{0,12}验证码|验证您是人类|访问受限|访问过于频繁|请先登[录入]|为了更好的访问体验.{0,4}请进行验证|(?:正在|请|需要).{0,8}(?:真人验证|人机验证)|验证成功.{0,4}正在等待|verification successful.{0,4}waiting for|checking your browser|認証が必要|ログインが必要|로그인이 필요|접근이 제한|人机验证|真人验证|请按住滑块|unusual traffic|需要进行其他验证|(?:您|你)所在的(?:用户组|用戶組).{0,12}(?:游客|遊客).{0,12}(?:无法|無法|不能)(?:进行|進行)此操作/i.test(text)
        || (/(^|\\.)zhipin\\.com$/.test(location.hostname) && location.pathname === '/web/passport/zp/security.html');
})()`;
// Memory guard for in-process capture. The 4k cap we used to apply everywhere
// silently truncated JSON so `JSON.parse` failed or gave partial objects — the
// primary agent-facing bug. Now we keep the full body up to a large cap and
// surface `responseBodyFullSize` + `responseBodyTruncated` so downstream layers
// can tell the agent what happened instead of lying about the payload.
export const CDP_RESPONSE_BODY_CAPTURE_LIMIT = 8 * 1024 * 1024;
function dailyChromeEndpoint() {
    // Read only the debugging endpoint, never browser history or credentials.
    const base = process.platform === 'darwin'
        ? join(homedir(), 'Library/Application Support/Google/Chrome')
        : process.platform === 'win32'
            ? join(process.env.LOCALAPPDATA || join(homedir(), 'AppData/Local'), 'Google/Chrome/User Data')
            : join(homedir(), '.config/google-chrome');
    let lines;
    try { lines = readFileSync(join(base, 'DevToolsActivePort'), 'utf8').trim().split(/\r?\n/); }
    catch { throw new Error('Daily Chrome CDP is unavailable. Enable remote debugging in your daily Chrome; no extension fallback is used.'); }
    const port = Number(lines[0]);
    if (!Number.isInteger(port) || port < 1 || port > 65535 || !/^\/devtools\/browser(?:\/[^\s?#]+)?$/.test(lines[1] || ''))
        throw new Error('Daily Chrome has an invalid DevToolsActivePort endpoint');
    return `ws://127.0.0.1:${port}${lines[1]}`;
}
export class CDPBridge {
    _sessionId = null;
    _targetId = null;
    _ws = null;
    _idCounter = 0;
    _pending = new Map();
    _eventListeners = new Map();
    async connect(opts) {
        if (this._ws)
            throw new Error('CDPBridge is already connected. Call close() before reconnecting.');
        const endpoint = opts?.cdpEndpoint ?? process.env.OPENCLI_CDP_ENDPOINT ?? dailyChromeEndpoint();
        if (!endpoint)
            throw new Error('CDP endpoint not provided (pass cdpEndpoint or set OPENCLI_CDP_ENDPOINT)');
        let wsUrl = endpoint;
        if (endpoint.startsWith('http')) {
            const targets = await fetchJsonDirect(`${endpoint.replace(/\/$/, '')}/json`);
            const target = selectCDPTarget(targets);
            if (!target || !target.webSocketDebuggerUrl) {
                throw new Error('No inspectable targets found at CDP endpoint');
            }
            wsUrl = target.webSocketDebuggerUrl;
        }
        return new Promise((resolve, reject) => {
            const ws = new WebSocket(wsUrl);
            const timeoutMs = (opts?.timeout ?? 10) * 1000;
            const timeout = setTimeout(() => {
                this._ws = null;
                ws.close();
                reject(new Error('CDP connect timeout'));
            }, timeoutMs);
            ws.on('open', async () => {
                clearTimeout(timeout);
                this._ws = ws;
                try {
                    if (new URL(wsUrl).pathname.startsWith('/devtools/browser')) {
                        const created = await this.send('Target.createTarget', { url: 'about:blank', background: true });
                        if (!created.targetId) throw new Error('CDP did not create a task-owned tab');
                        this._targetId = created.targetId;
                        const attached = await this.send('Target.attachToTarget', { targetId: this._targetId, flatten: true });
                        if (!attached.sessionId) throw new Error('CDP did not attach the task-owned tab');
                        this._sessionId = attached.sessionId;
                    }
                    await this.send('Page.enable');
                    // Use the daily browser as it is. Job-hunt does not alter
                    // browser fingerprints or inject anti-detection scripts.
                }
                catch (err) {
                    await this.close();
                    reject(err instanceof Error ? err : new Error(String(err)));
                    return;
                }
                resolve(new CDPPage(this));
            });
            ws.on('error', (err) => {
                clearTimeout(timeout);
                reject(err);
            });
            ws.on('message', (data) => {
                try {
                    const msg = JSON.parse(data.toString());
                    if (msg.id && this._pending.has(msg.id)) {
                        const entry = this._pending.get(msg.id);
                        clearTimeout(entry.timer);
                        this._pending.delete(msg.id);
                        if (msg.error) {
                            entry.reject(new Error(msg.error.message));
                        }
                        else {
                            entry.resolve(msg.result);
                        }
                    }
                    if (msg.method && (!this._sessionId || msg.sessionId === this._sessionId)) {
                        const listeners = this._eventListeners.get(msg.method);
                        if (listeners) {
                            for (const fn of listeners)
                                fn(msg.params);
                        }
                    }
                }
                catch (err) {
                    if (process.env.OPENCLI_VERBOSE) {
                        // eslint-disable-next-line no-console
                        console.error('[cdp] Failed to parse WebSocket message:', err instanceof Error ? err.message : err);
                    }
                }
            });
        });
    }
    async close() {
        if (this._targetId && this._ws?.readyState === WebSocket.OPEN) {
            let handedOff = false;
            try {
                if (this._sessionId) {
                    const state = await this.send('Runtime.evaluate', { expression: USER_ACTION_EXPRESSION, returnByValue: true }, 3000);
                    if (state.result?.value === true) {
                        handedOff = true;
                        try {
                            await this.send('JobHunt.handoffTarget', { targetId: this._targetId }, 3000, null);
                        } catch (err) {
                            if (!/(?:wasn't found|method not found|unknown method|-32601)/i.test(err.message)) throw err;
                            await this.send('Target.activateTarget', { targetId: this._targetId }, 3000, null);
                            await this.send('Target.detachFromTarget', { sessionId: this._sessionId }, 3000, null);
                        }
                        console.error('[cdp] USER_ACTION_REQUIRED: login or verification tab kept open in the daily browser:', this._targetId);
                    }
                }
            } catch (err) { console.error('[cdp] Could not inspect or hand off task tab:', err.message); }
            if (!handedOff) {
                try { await this.send('Target.closeTarget', { targetId: this._targetId }, 3000, null); }
                catch (err) { console.error('[cdp] Could not close task tab:', err.message); }
            }
        }
        this._targetId = null;
        this._sessionId = null;
        if (this._ws) {
            this._ws.close();
            this._ws = null;
        }
        for (const p of this._pending.values()) {
            clearTimeout(p.timer);
            p.reject(new Error('CDP connection closed'));
        }
        this._pending.clear();
        this._eventListeners.clear();
    }
    async send(method, params = {}, timeoutMs = CDP_SEND_TIMEOUT, sessionId = this._sessionId) {
        if (!this._ws || this._ws.readyState !== WebSocket.OPEN) {
            throw new Error('CDP connection is not open');
        }
        const id = ++this._idCounter;
        return new Promise((resolve, reject) => {
            const timer = setTimeout(() => {
                this._pending.delete(id);
                reject(new Error(`CDP command '${method}' timed out after ${timeoutMs / 1000}s`));
            }, timeoutMs);
            this._pending.set(id, { resolve, reject, timer });
            const message = { id, method, params };
            if (sessionId) message.sessionId = sessionId;
            if (process.env.OPENCLI_CDP_TRACE === '1')
                console.error('[opencli-cdp]', JSON.stringify({ method, sessionId, targetId: this._targetId }));
            this._ws.send(JSON.stringify(message));
        });
    }
    on(event, handler) {
        let set = this._eventListeners.get(event);
        if (!set) {
            set = new Set();
            this._eventListeners.set(event, set);
        }
        set.add(handler);
    }
    off(event, handler) {
        this._eventListeners.get(event)?.delete(handler);
    }
    waitForEvent(event, timeoutMs = 15_000) {
        return new Promise((resolve, reject) => {
            const timer = setTimeout(() => {
                this.off(event, handler);
                reject(new Error(`Timed out waiting for CDP event '${event}'`));
            }, timeoutMs);
            const handler = (params) => {
                clearTimeout(timer);
                this.off(event, handler);
                resolve(params);
            };
            this.on(event, handler);
        });
    }
}
class CDPPage extends CDPBasePage {
    bridge;
    _pageEnabled = false;
    // Network capture state (mirrors extension/src/cdp.ts NetworkCaptureEntry shape)
    _networkCapturing = false;
    _networkCapturePattern = '';
    _networkEntries = [];
    _pendingRequests = new Map(); // requestId → index in _networkEntries
    _pendingBodyFetches = new Set(); // track in-flight getResponseBody calls
    _consoleMessages = [];
    _consoleCapturing = false;
    constructor(bridge) {
        super();
        this.bridge = bridge;
    }
    async goto(url, options) {
        if (!this._pageEnabled) {
            await this.bridge.send('Page.enable');
            this._pageEnabled = true;
        }
        const loadPromise = this.bridge.waitForEvent('Page.loadEventFired', 30_000).catch(() => { });
        await this.bridge.send('Page.navigate', { url });
        await loadPromise;
        this._lastUrl = url;
        if (options?.waitUntil !== 'none') {
            const maxMs = options?.settleMs ?? 1000;
            await this.evaluate(waitForDomStableJs(maxMs, Math.min(500, maxMs)));
        }
    }
    async evaluate(input, ...args) {
        const expression = buildEvaluateExpression(input, args);
        const result = await this.bridge.send('Runtime.evaluate', {
            expression,
            returnByValue: true,
            awaitPromise: true,
        });
        if (result.exceptionDetails) {
            throw new Error('Evaluate error: ' + (result.exceptionDetails.exception?.description || 'Unknown exception'));
        }
        return result.result?.value;
    }
    async getCookies(opts = {}) {
        const result = await this.bridge.send('Network.getCookies', opts.url ? { urls: [opts.url] } : {});
        const cookies = isRecord(result) && Array.isArray(result.cookies) ? result.cookies : [];
        const domain = opts.domain;
        return domain
            ? cookies.filter((cookie) => isCookie(cookie) && matchesCookieDomain(cookie.domain, domain))
            : cookies;
    }
    async screenshot(options = {}) {
        const fullPage = options.fullPage === true;
        const overrideWidth = options.width && options.width > 0 ? Math.ceil(options.width) : undefined;
        // height is ignored under fullPage so the captureBeyondViewport path stays unchanged for users who pass --height alongside --full-page.
        const overrideHeight = !fullPage && options.height && options.height > 0 ? Math.ceil(options.height) : undefined;
        const needsOverride = overrideWidth !== undefined || overrideHeight !== undefined;
        if (needsOverride) {
            if (overrideWidth !== undefined && fullPage) {
                await this.bridge.send('Emulation.setDeviceMetricsOverride', {
                    mobile: false,
                    width: overrideWidth,
                    height: 0,
                    deviceScaleFactor: 1,
                });
            }
            let finalWidth = overrideWidth ?? 0;
            let finalHeight = overrideHeight ?? 0;
            if (fullPage) {
                const metrics = await this.bridge.send('Page.getLayoutMetrics');
                const m = isRecord(metrics) ? metrics : {};
                const css = isRecord(m.cssContentSize) ? m.cssContentSize : undefined;
                const fb = isRecord(m.contentSize) ? m.contentSize : undefined;
                const size = css ?? fb;
                if (size && typeof size.width === 'number' && typeof size.height === 'number') {
                    if (finalWidth === 0)
                        finalWidth = Math.ceil(size.width);
                    finalHeight = Math.ceil(size.height);
                }
            }
            await this.bridge.send('Emulation.setDeviceMetricsOverride', {
                mobile: false,
                width: finalWidth,
                height: finalHeight,
                deviceScaleFactor: 1,
            });
        }
        try {
            const result = await this.bridge.send('Page.captureScreenshot', {
                format: options.format ?? 'png',
                quality: options.format === 'jpeg' ? (options.quality ?? 80) : undefined,
                captureBeyondViewport: !needsOverride && fullPage,
            });
            const base64 = isRecord(result) && typeof result.data === 'string' ? result.data : '';
            if (options.path) {
                await saveBase64ToFile(base64, options.path);
            }
            return base64;
        }
        finally {
            if (needsOverride) {
                await this.bridge.send('Emulation.clearDeviceMetricsOverride').catch(() => { });
            }
        }
    }
    async startNetworkCapture(pattern = '') {
        // Always update the filter pattern
        this._networkCapturePattern = pattern;
        // Reset state only on first start; avoid wiping entries if already capturing
        if (!this._networkCapturing) {
            this._networkEntries = [];
            this._pendingRequests.clear();
            this._pendingBodyFetches.clear();
            await this.bridge.send('Network.enable');
            // Step 1: Record request method/url on requestWillBeSent
            this.bridge.on('Network.requestWillBeSent', (params) => {
                const p = params;
                if (!this._networkCapturePattern || p.request.url.includes(this._networkCapturePattern)) {
                    const idx = this._networkEntries.push({
                        url: p.request.url,
                        method: p.request.method,
                        timestamp: Date.now(),
                    }) - 1;
                    this._pendingRequests.set(p.requestId, idx);
                }
            });
            // Step 2: Fill in response metadata on responseReceived
            this.bridge.on('Network.responseReceived', (params) => {
                const p = params;
                const idx = this._pendingRequests.get(p.requestId);
                if (idx !== undefined) {
                    this._networkEntries[idx].responseStatus = p.response.status;
                    this._networkEntries[idx].responseContentType = p.response.mimeType || '';
                }
            });
            // Step 3: Fetch body on loadingFinished (body is only reliably available after this)
            this.bridge.on('Network.loadingFinished', (params) => {
                const p = params;
                const idx = this._pendingRequests.get(p.requestId);
                if (idx !== undefined) {
                    const bodyFetch = this.bridge.send('Network.getResponseBody', { requestId: p.requestId }).then((result) => {
                        const r = result;
                        if (typeof r?.body === 'string') {
                            const fullSize = r.body.length;
                            const truncated = fullSize > CDP_RESPONSE_BODY_CAPTURE_LIMIT;
                            const body = truncated ? r.body.slice(0, CDP_RESPONSE_BODY_CAPTURE_LIMIT) : r.body;
                            this._networkEntries[idx].responsePreview = r.base64Encoded ? `base64:${body}` : body;
                            this._networkEntries[idx].responseBodyFullSize = fullSize;
                            this._networkEntries[idx].responseBodyTruncated = truncated;
                        }
                    }).catch((err) => {
                        // Body unavailable for some requests (e.g. uploads) — non-fatal
                        if (process.env.OPENCLI_VERBOSE) {
                            // eslint-disable-next-line no-console
                            console.error(`[cdp] getResponseBody failed for ${p.requestId}:`, err instanceof Error ? err.message : err);
                        }
                    }).finally(() => {
                        this._pendingBodyFetches.delete(bodyFetch);
                    });
                    this._pendingBodyFetches.add(bodyFetch);
                    this._pendingRequests.delete(p.requestId);
                }
            });
            this._networkCapturing = true;
        }
        return true;
    }
    async readNetworkCapture() {
        // Await all in-flight body fetches so entries have responsePreview populated
        if (this._pendingBodyFetches.size > 0) {
            await Promise.all([...this._pendingBodyFetches]);
        }
        const entries = [...this._networkEntries];
        this._networkEntries = [];
        return entries;
    }
    async consoleMessages(level = 'all') {
        if (!this._consoleCapturing) {
            await this.bridge.send('Runtime.enable');
            this.bridge.on('Runtime.consoleAPICalled', (params) => {
                const p = params;
                const text = (p.args || []).map(a => a.value !== undefined ? String(a.value) : (a.description || '')).join(' ');
                this._consoleMessages.push({ type: p.type, text, timestamp: Date.now() });
                if (this._consoleMessages.length > 500)
                    this._consoleMessages.shift();
            });
            // Capture uncaught exceptions as error-level messages
            this.bridge.on('Runtime.exceptionThrown', (params) => {
                const p = params;
                const desc = p.exceptionDetails?.exception?.description || p.exceptionDetails?.text || 'Unknown exception';
                this._consoleMessages.push({ type: 'error', text: desc, timestamp: Date.now() });
                if (this._consoleMessages.length > 500)
                    this._consoleMessages.shift();
            });
            this._consoleCapturing = true;
        }
        if (level === 'all')
            return [...this._consoleMessages];
        // 'error' level includes both console.error() and uncaught exceptions
        if (level === 'error')
            return this._consoleMessages.filter(m => m.type === 'error');
        return this._consoleMessages.filter(m => m.type === level);
    }
    async tabs() {
        return [];
    }
    async selectTab(_target) {
        // Not supported in direct CDP mode
    }
    async cdp(method, params = {}) {
        return this.bridge.send(method, params);
    }
    async insertText(text) {
        await this.nativeType(text);
    }
}
function isCookie(value) {
    return isRecord(value)
        && typeof value.name === 'string'
        && typeof value.value === 'string'
        && typeof value.domain === 'string';
}
function matchesCookieDomain(cookieDomain, targetDomain) {
    const normalizedCookieDomain = cookieDomain.replace(/^\./, '').toLowerCase();
    const normalizedTargetDomain = targetDomain.replace(/^\./, '').toLowerCase();
    return normalizedTargetDomain === normalizedCookieDomain
        || normalizedTargetDomain.endsWith(`.${normalizedCookieDomain}`);
}
function selectCDPTarget(targets) {
    const preferredPattern = compilePreferredPattern(process.env.OPENCLI_CDP_TARGET);
    const candidates = targets
        .map((target, index) => ({ target, index, score: scoreCDPTarget(target, preferredPattern) }))
        .filter(({ score }) => Number.isFinite(score));
    // Electron apps route auxiliary windows onto the main document through a
    // query: Codex ships its avatar overlay as
    // `app://-/index.html?initialRoute=%2Favatar-overlay`, which answers `/json`
    // first and scores exactly like the main window, so document order used to
    // send every command to a surface with no app UI (#2242). Only break that
    // tie; a routed window that outscores its plain sibling is still the better
    // target, and on http(s) a query is ordinary page state.
    const plainDocuments = new Set();
    for (const { target } of candidates) {
        const url = parseLocalDocumentUrl(target.url);
        if (url && !url.search)
            plainDocuments.add(toDocumentKey(url));
    }
    const ranked = candidates
        .map((entry) => {
        const url = parseLocalDocumentUrl(entry.target.url);
        return { ...entry, routed: !!url && !!url.search && plainDocuments.has(toDocumentKey(url)) };
    })
        .sort((a, b) => {
        if (b.score !== a.score)
            return b.score - a.score;
        if (a.routed !== b.routed)
            return a.routed ? 1 : -1;
        return a.index - b.index;
    });
    return ranked[0]?.target;
}
function scoreCDPTarget(target, preferredPattern) {
    if (!target.webSocketDebuggerUrl)
        return Number.NEGATIVE_INFINITY;
    const type = (target.type ?? '').toLowerCase();
    const url = (target.url ?? '').toLowerCase();
    const title = (target.title ?? '').toLowerCase();
    const haystack = `${title} ${url}`;
    if (!haystack.trim() && !type)
        return Number.NEGATIVE_INFINITY;
    if (haystack.includes('devtools'))
        return Number.NEGATIVE_INFINITY;
    if (type === 'background_page' || type === 'service_worker')
        return Number.NEGATIVE_INFINITY;
    let score = 0;
    if (preferredPattern && preferredPattern.test(haystack))
        score += 1000;
    if (type === 'app')
        score += 120;
    else if (type === 'webview')
        score += 100;
    else if (type === 'page')
        score += 80;
    else if (type === 'iframe')
        score += 20;
    if (url.startsWith('http://localhost') || url.startsWith('https://localhost'))
        score += 90;
    if (url.startsWith('file://'))
        score += 60;
    if (url.startsWith('http://127.0.0.1') || url.startsWith('https://127.0.0.1'))
        score += 50;
    if (url.startsWith('about:blank'))
        score -= 120;
    if (url === '' || url === 'about:blank')
        score -= 40;
    if (title && title !== 'devtools')
        score += 25;
    // Boost score for known Electron app names from the registry (builtin + user-defined)
    const appNames = Object.values(getAllElectronApps()).map(a => (a.displayName ?? a.processName).toLowerCase());
    for (const name of appNames) {
        if (title.includes(name)) {
            score += 120;
            break;
        }
    }
    for (const name of appNames) {
        if (url.includes(name)) {
            score += 100;
            break;
        }
    }
    return score;
}
// Keep this explicit: these are the schemes Electron serves a shared local
// document over, where a query is a window route (#2242). A "not http(s)"
// check would also sweep in schemes we know nothing about.
const LOCAL_DOCUMENT_SCHEMES = new Set(['app:', 'file:']);
/**
 * Parse a URL that names a local app document eligible for routed-window
 * demotion (#2242).
 *
 * Only allowlisted schemes qualify: on http(s), and on any scheme we cannot
 * vouch for, a query is ordinary page state, so returning null there keeps
 * plain document-order selection.
 */
function parseLocalDocumentUrl(raw) {
    try {
        const url = new URL(raw ?? '');
        return LOCAL_DOCUMENT_SCHEMES.has(url.protocol) ? url : null;
    }
    catch {
        return null;
    }
}
function toDocumentKey(url) {
    return `${url.protocol}//${url.host}${url.pathname}`;
}
function compilePreferredPattern(raw) {
    const value = raw?.trim();
    if (!value)
        return undefined;
    return new RegExp(escapeRegExp(value.toLowerCase()));
}
function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
export const __test__ = {
    selectCDPTarget,
    scoreCDPTarget,
};
function fetchJsonDirect(url) {
    return new Promise((resolve, reject) => {
        const parsed = new URL(url);
        const request = (parsed.protocol === 'https:' ? httpsRequest : httpRequest)(parsed, (res) => {
            const statusCode = res.statusCode ?? 0;
            if (statusCode < 200 || statusCode >= 300) {
                res.resume();
                reject(new Error(`Failed to fetch CDP targets: HTTP ${statusCode}`));
                return;
            }
            const chunks = [];
            res.on('data', (chunk) => chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk)));
            res.on('end', () => {
                try {
                    resolve(JSON.parse(Buffer.concat(chunks).toString('utf8')));
                }
                catch (error) {
                    reject(error instanceof Error ? error : new Error(String(error)));
                }
            });
        });
        request.on('error', reject);
        request.setTimeout(10_000, () => request.destroy(new Error('Timed out fetching CDP targets')));
        request.end();
    });
}

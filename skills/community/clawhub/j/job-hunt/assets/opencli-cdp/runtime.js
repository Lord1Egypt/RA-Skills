import { CDPBridge } from './browser/index.js';
import { TimeoutError } from './errors.js';
import { isElectronApp } from './electron-apps.js';
import { DEFAULT_BROWSER_COMMAND_TIMEOUT, DEFAULT_BROWSER_CONNECT_TIMEOUT } from './browser/config.js';
export { DEFAULT_BROWSER_COMMAND_TIMEOUT, DEFAULT_BROWSER_CONNECT_TIMEOUT };
/** Local CDP-only patch: all browser adapters use the direct transport. */
export function getBrowserFactory(_site) {
    return CDPBridge;
}
/**
 * Timeout with seconds unit. Used for high-level command timeouts.
 */
export async function runWithTimeout(promise, opts) {
    const label = opts.label ?? 'Operation';
    return withTimeoutMs(promise, opts.timeout * 1000, () => new TimeoutError(label, opts.timeout, opts.hint));
}
/**
 * Timeout with milliseconds unit. Used for low-level internal timeouts.
 * Accepts a factory function to create the rejection error, keeping this
 * utility decoupled from specific error types.
 */
export function withTimeoutMs(promise, timeoutMs, makeError = 'Operation timed out') {
    const reject_ = typeof makeError === 'string'
        ? () => new Error(makeError)
        : makeError;
    return new Promise((resolve, reject) => {
        const timer = setTimeout(() => reject(reject_()), timeoutMs);
        promise.then((value) => { clearTimeout(timer); resolve(value); }, (error) => { clearTimeout(timer); reject(error); });
    });
}
export async function browserSession(BrowserFactory, fn, opts = {}) {
    const browser = new BrowserFactory();
    try {
        const page = await browser.connect({
            timeout: DEFAULT_BROWSER_CONNECT_TIMEOUT,
            session: opts.session,
            cdpEndpoint: opts.cdpEndpoint,
            contextId: opts.contextId,
            preferredContextId: opts.preferredContextId,
            idleTimeout: opts.idleTimeout,
            windowMode: opts.windowMode,
            surface: opts.surface,
            siteSession: opts.siteSession,
        });
        return await fn(page);
    }
    finally {
        await browser.close().catch(() => { });
    }
}

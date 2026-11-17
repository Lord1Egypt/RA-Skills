/** Local CDP-only health check: a new blank task tab, no extension or cookies. */
import { CDPBridge } from './browser/cdp.js';
export async function checkConnectivity(opts = {}) {
    const start = Date.now();
    const bridge = new CDPBridge();
    try {
        const page = await bridge.connect({ timeout: opts.timeout ?? 8 });
        const url = await page.evaluate('location.href');
        if (url !== 'about:blank') throw new Error('CDP health check expected its own blank tab');
        return { ok: true, durationMs: Date.now() - start };
    } catch (err) {
        return { ok: false, error: err.message, durationMs: Date.now() - start };
    } finally {
        await bridge.close();
    }
}
export async function runBrowserDoctor(opts = {}) {
    const connectivity = await checkConnectivity();
    return { cliVersion: opts.cliVersion, transport: 'CDP', connectivity,
        issues: connectivity.ok ? [] : [connectivity.error] };
}
export function renderBrowserDoctorReport(report) {
    return [`opencli v${report.cliVersion ?? 'unknown'} doctor (local CDP patch)`,
        '[OK] Browser transport: direct CDP',
        report.connectivity.ok
            ? `[OK] Connectivity: task-owned blank tab verified in ${(report.connectivity.durationMs / 1000).toFixed(1)}s`
            : `[FAIL] Connectivity: ${report.connectivity.error}`,
    ].join('\n');
}

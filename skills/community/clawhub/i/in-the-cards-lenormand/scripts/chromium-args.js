/**
 * Shared Chromium launch flags for the Puppeteer scripts.
 *
 * Chromium's sandbox stays ON by default. It is disabled only when it
 * cannot run at all — as root, or in restricted containers — or when the
 * user explicitly opts in with PUPPETEER_NO_SANDBOX=1. The renderers load
 * generated HTML that can contain user-derived text, so disabling the
 * sandbox unconditionally would weaken isolation for no benefit on a
 * regular user machine.
 */
function chromiumArgs(extraArgs = []) {
  const runningAsRoot =
    typeof process.getuid === 'function' && process.getuid() === 0;
  const sandboxDisabled =
    runningAsRoot || process.env.PUPPETEER_NO_SANDBOX === '1';
  return [
    ...(sandboxDisabled ? ['--no-sandbox', '--disable-setuid-sandbox'] : []),
    ...extraArgs,
  ];
}

module.exports = { chromiumArgs };

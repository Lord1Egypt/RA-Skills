#!/usr/bin/env node
/**
 * launch-session.js
 * 
 * CLI wrapper to launch a session for use in standalone scripts/automation
 * 
 * Usage:
 *   node launch-session.js <platform> [account]
 * 
 * Returns: JSON output with session details
 * 
 * Example (in another script):
 *   const result = require('child_process').execSync(
 *     'node launch-session.js amazon work',
 *     { encoding: 'utf8' }
 *   );
 *   const session = JSON.parse(result);
 *   // session.pid, session.debugURL, session.wsEndpoint, etc.
 */

const { launchSession, hasSession } = require(
  process.env.OTO_PATH ? 
    `${process.env.OTO_PATH}/lib/session-manager` : 
    `${require('path').join(require('os').homedir(), 'oto/lib/session-manager')}`
);

const platform = process.argv[2];
const account = process.argv[3] || 'default';

if (!platform) {
  console.error('Usage: node launch-session.js <platform> [account]');
  process.exit(1);
}

if (!hasSession(platform, account)) {
  console.error(`Session not found: ${platform}:${account}`);
  console.error(`\nCreate it first with:`);
  console.error(`  node ~/oto/scripts/save-session.js ${platform} <url> ${account}`);
  process.exit(1);
}

(async () => {
  try {
    const { browser, page, context } = await launchSession(platform, account, false);
    const wsEndpoint = browser.wsEndpoint();
    
    console.log(JSON.stringify({
      success: true,
      platform,
      account,
      wsEndpoint,
      debugUrl: `devtools://devtools/bundled/js_app.html?ws=${wsEndpoint.replace(/^ws:\/\//, '')}`,
      page: {
        url: page.url(),
        title: await page.title()
      }
    }, null, 2));

    // Keep browser alive (parent process should clean up)
    process.on('SIGTERM', async () => {
      await browser.close();
      process.exit(0);
    });

  } catch (err) {
    console.error(JSON.stringify({
      success: false,
      error: err.message
    }, null, 2));
    process.exit(1);
  }
})();

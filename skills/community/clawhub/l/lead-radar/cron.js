/**
 * Lead Radar — Daily Cron Job
 *
 * Runs every day at 8am (configured in SKILL.md).
 * Scans all sources, scores intent, deduplicates, and delivers to Telegram.
 */

const { checkLicense } = require('./lib/licenseCheck');
const { extractKeywords, scoreIntent } = require('./lib/intentScorer');
const { dedup, markSeen, purgeOld, closeDb } = require('./lib/dedup');
const { formatMessage } = require('./lib/formatter');
const { sendTelegram } = require('./lib/telegram');
const { scanReddit } = require('./sources/reddit');
const { scanHN } = require('./sources/hn');
const { scanIH } = require('./sources/indieHackers');
const { scanStackOverflow } = require('./sources/stackoverflow');
const { scanQuora } = require('./sources/quora');
const { scanHashnode } = require('./sources/hashnode');
const { scanDevTo } = require('./sources/devto');
const { scanGitHub } = require('./sources/github');
const { scanLobsters } = require('./sources/lobsters');

async function run(context) {
  const startTime = Date.now();
  console.log(`[Lead Radar] Starting scan at ${new Date().toISOString()}`);

  // Step 1: Validate license and get Gemini API key
  const license = await checkLicense(process.env.LEAD_RADAR_LICENSE_KEY);
  if (!license.valid) {
    console.log(`[Lead Radar] License invalid: ${license.message}`);
    await sendTelegram(process.env.TELEGRAM_CHAT_ID, license.message);
    return;
  }

  // Inject server-provided Gemini key (users don't need their own)
  if (license.geminiKey) {
    process.env.GEMINI_API_KEY = license.geminiKey;
  }
  if (!process.env.GEMINI_API_KEY) {
    await sendTelegram(
      process.env.TELEGRAM_CHAT_ID,
      '⚠️ Lead Radar: AI scoring unavailable. Please contact support.'
    );
    return;
  }

  // Step 2: Extract search keywords from offer description
  const offerDescription = process.env.OFFER_DESCRIPTION;
  if (!offerDescription) {
    await sendTelegram(
      process.env.TELEGRAM_CHAT_ID,
      '\u26A0\uFE0F Lead Radar: No OFFER_DESCRIPTION configured. Please set it in your skill config.'
    );
    return;
  }

  console.log(`[Lead Radar] Extracting keywords from: "${offerDescription}"`);
  const keywords = await extractKeywords(offerDescription);
  console.log(`[Lead Radar] Keywords: ${keywords.join(', ')}`);

  // Step 3: Scan all sources in parallel
  console.log('[Lead Radar] Scanning all sources...');
  const [redditPosts, hnPosts, ihPosts, soPosts, quoraPosts, hashnodePosts, devtoPosts, githubPosts, lobstersPosts] = await Promise.all([
    scanReddit(keywords).catch((err) => {
      console.error('[Lead Radar] Reddit scan failed:', err.message);
      return [];
    }),
    scanHN(keywords).catch((err) => {
      console.error('[Lead Radar] HN scan failed:', err.message);
      return [];
    }),
    scanIH(keywords).catch((err) => {
      console.error('[Lead Radar] Indie Hackers scan failed:', err.message);
      return [];
    }),
    scanStackOverflow(keywords).catch((err) => {
      console.error('[Lead Radar] Stack Overflow scan failed:', err.message);
      return [];
    }),
    scanQuora(keywords).catch((err) => {
      console.error('[Lead Radar] Quora scan failed:', err.message);
      return [];
    }),
    scanHashnode(keywords).catch((err) => {
      console.error('[Lead Radar] Hashnode scan failed:', err.message);
      return [];
    }),
    scanDevTo(keywords).catch((err) => {
      console.error('[Lead Radar] Dev.to scan failed:', err.message);
      return [];
    }),
    scanGitHub(keywords).catch((err) => {
      console.error('[Lead Radar] GitHub scan failed:', err.message);
      return [];
    }),
    scanLobsters(keywords).catch((err) => {
      console.error('[Lead Radar] Lobsters scan failed:', err.message);
      return [];
    }),
  ]);

  // Track source health for user transparency
  const sourceCounts = {
    Reddit: redditPosts.length,
    HN: hnPosts.length,
    'Indie Hackers': ihPosts.length,
    'Stack Overflow': soPosts.length,
    Quora: quoraPosts.length,
    Hashnode: hashnodePosts.length,
    'Dev.to': devtoPosts.length,
    GitHub: githubPosts.length,
    Lobsters: lobstersPosts.length,
  };

  console.log(
    `[Lead Radar] Found: ${Object.entries(sourceCounts).map(([k, v]) => `${k}=${v}`).join(', ')}`
  );

  // Detect sources that returned 0 — likely blocked or down
  const downSources = Object.entries(sourceCounts)
    .filter(([, count]) => count === 0)
    .map(([name]) => name);

  const all = [...redditPosts, ...hnPosts, ...ihPosts, ...soPosts, ...quoraPosts, ...hashnodePosts, ...devtoPosts, ...githubPosts, ...lobstersPosts];

  if (all.length === 0) {
    console.log('[Lead Radar] No posts found across any source');
    const msg = formatMessage([], offerDescription);
    await sendTelegram(process.env.TELEGRAM_CHAT_ID, msg);
    return;
  }

  // Step 4: Deduplicate against previously sent posts
  const fresh = dedup(all);
  console.log(`[Lead Radar] ${fresh.length} fresh posts after dedup (${all.length - fresh.length} duplicates removed)`);

  if (fresh.length === 0) {
    const msg = formatMessage([], offerDescription);
    await sendTelegram(process.env.TELEGRAM_CHAT_ID, msg);
    return;
  }

  // Step 5: Score intent with Gemini 2.5 Flash
  console.log(`[Lead Radar] Scoring ${fresh.length} posts for intent...`);
  const top10 = await scoreIntent(fresh, offerDescription);
  console.log(`[Lead Radar] ${top10.length} posts scored >= 5 (warm leads)`);

  // Step 6: Mark scored posts as seen (even if 0 warm leads, to avoid re-scoring)
  markSeen(fresh);

  // Step 7: Format and send to Telegram
  let message = formatMessage(top10, offerDescription);

  // Append source health warning if any sources are down
  if (downSources.length > 0 && downSources.length <= 5) {
    message += `\n\n\u26A0\uFE0F Sources down: ${downSources.join(', ')}. These may be temporarily blocking requests.`;
  }

  // Append scan stats
  const activeSources = Object.values(sourceCounts).filter((c) => c > 0).length;
  const totalSources = Object.keys(sourceCounts).length;
  message += `\n\n\uD83D\uDCCA Scanned ${all.length} posts across ${activeSources}/${totalSources} sources`;

  // Append trial info if applicable
  if (license.trialDaysLeft) {
    message += `\n\u23F3 Trial: ${license.trialDaysLeft} day${license.trialDaysLeft === 1 ? '' : 's'} remaining \u2014 subscribe at lead-radar.pro`;
  }

  await sendTelegram(process.env.TELEGRAM_CHAT_ID, message);

  // Step 8: Purge old dedup entries
  purgeOld();

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`[Lead Radar] Done in ${elapsed}s. Sent ${top10.length} leads.`);
}

// Allow running directly via `node cron.js` for testing
if (require.main === module) {
  require('dotenv').config();
  run()
    .then(() => {
      closeDb();
      process.exit(0);
    })
    .catch((err) => {
      console.error('Fatal error:', err);
      closeDb();
      process.exit(1);
    });
}

module.exports = { run };

#!/usr/bin/env node
/**
 * Daily Publisher — Indie App Marketing Pipeline
 *
 * Reads today's entries from the weekly plan and schedules them to Postiz.
 *
 * Handles:
 *   - X tweets      → schedules text via Postiz API
 *   - Facebook posts → schedules text via Postiz API
 *   - TikTok         → triggers your video-gen script (requires requiresVideoGen flag)
 *   - YouTube Shorts → marks as handled via TikTok crossPost
 *
 * Usage:
 *   node daily-publisher.js [--dry-run] [--day YYYY-MM-DD] [--skip-past] [--text-only] [--config path/to/config.json]
 *
 * --dry-run:   Preview without making any API calls
 * --day:       Override today's date (default: today)
 * --skip-past: Skip posts whose scheduled time has already passed
 * --text-only: Only schedule X + Facebook; skip TikTok + YouTube
 * --config:    Path to config.json (default: ./config.json)
 *
 * Designed to run on a cron at 7:00 AM daily.
 */

'use strict';

const fs             = require('fs');
const path           = require('path');
const { execSync }   = require('child_process');

// ── CLI ──────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);

function getArg(name) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 ? args[idx + 1] : null;
}

const dryRun   = args.includes('--dry-run');
const skipPast = args.includes('--skip-past');
const textOnly = args.includes('--text-only');
const configArg = getArg('config');

// ── Config ───────────────────────────────────────────────────────────────────
const CONFIG_PATH = configArg
  ? path.resolve(configArg)
  : path.join(process.cwd(), 'config.json');

if (!fs.existsSync(CONFIG_PATH)) {
  console.error(`Config not found: ${CONFIG_PATH}`);
  console.error('Run setup.sh first, or pass --config /path/to/config.json');
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));

const BASE_DIR  = path.dirname(CONFIG_PATH);
const PLANS_DIR = path.join(BASE_DIR, config.paths?.plans || 'plans');
const LOGS_DIR  = path.join(BASE_DIR, config.paths?.logs  || 'logs');

// ── .env loader ──────────────────────────────────────────────────────────────
function loadEnv(dir) {
  const envPath = path.join(dir, '.env');
  if (!fs.existsSync(envPath)) return;
  for (const line of fs.readFileSync(envPath, 'utf-8').split('\n')) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const eq = t.indexOf('=');
    if (eq === -1) continue;
    const key = t.slice(0, eq).trim();
    let val   = t.slice(eq + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    if (!process.env[key]) process.env[key] = val;
  }
}

loadEnv(BASE_DIR);

// ── Postiz setup ──────────────────────────────────────────────────────────────
const POSTIZ_URL = (() => {
  const raw = config.postiz?.url || 'https://api.postiz.com/public/v1';
  return raw.replace(/\/$/, ''); // strip trailing slash
})();

const POSTIZ_KEY = (() => {
  const raw = config.postiz?.apiKey || '';
  if (raw.startsWith('$')) return process.env[raw.slice(1)] || '';
  return raw || process.env.POSTIZ_API_KEY || '';
})();

const INTEGRATION_IDS = config.postiz?.integrationIds || {};

if (!POSTIZ_KEY && !dryRun) {
  console.error('ERROR: No Postiz API key. Set POSTIZ_API_KEY in .env or config.json.');
  process.exit(1);
}

// Platforms that use direct text scheduling via Postiz
const TEXT_PLATFORMS = new Set(config.textPlatforms || ['x', 'facebook']);

// ── Find plan that covers a given date ───────────────────────────────────────
// When multiple plans cover the same date, prefer the one with the latest weekStart.
function findPlanForDate(targetDate) {
  if (!fs.existsSync(PLANS_DIR)) return null;

  const files = fs.readdirSync(PLANS_DIR)
    .filter(f => f.startsWith('weekly-plan-') && f.endsWith('.json'));

  let bestPath      = null;
  let bestWeekStart = '';

  for (const f of files) {
    const planPath = path.join(PLANS_DIR, f);
    try {
      const plan = JSON.parse(fs.readFileSync(planPath, 'utf-8'));
      if (
        plan.meta?.weekStart <= targetDate &&
        plan.meta?.weekEnd   >= targetDate &&
        plan.meta.weekStart > bestWeekStart
      ) {
        bestWeekStart = plan.meta.weekStart;
        bestPath      = planPath;
      }
    } catch { /* skip malformed plans */ }
  }

  return bestPath;
}

// ── Platform settings for Postiz ─────────────────────────────────────────────
function getSettings(platform) {
  switch (platform) {
    case 'x':        return { __type: 'x', who_can_reply_post: 'everyone' };
    case 'facebook': return { __type: 'facebook' };
    default:         return { __type: platform };
  }
}

// ── Retry helper (handles 429 rate limits and 5xx server errors) ──────────────
async function withRetry(fn, maxRetries = 3) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      const is429 = err.message.includes('429');
      const is5xx = /Postiz 5\d\d/.test(err.message);
      if ((is429 || is5xx) && attempt < maxRetries) {
        const wait = (attempt + 1) * (is429 ? 10000 : 5000);
        console.log(`  ${is429 ? 'Rate limited' : 'Server error'}, waiting ${wait / 1000}s (attempt ${attempt + 1}/${maxRetries})...`);
        await new Promise(r => setTimeout(r, wait));
        continue;
      }
      throw err;
    }
  }
}

// ── Schedule a text post to Postiz ───────────────────────────────────────────
async function scheduleTextPost(post) {
  const integrationId = INTEGRATION_IDS[post.platform];
  if (!integrationId) {
    throw new Error(`No integration ID configured for platform: ${post.platform}. Add it to config.json.`);
  }

  const payload = {
    type:      'schedule',
    date:      new Date(post.scheduledTime).toISOString(),
    shortLink: false,
    tags:      [],
    posts: [{
      integration: { id: integrationId },
      value:       [{ content: post.content, image: [] }],
      settings:    getSettings(post.platform),
    }],
  };

  const res = await fetch(`${POSTIZ_URL}/posts`, {
    method:  'POST',
    headers: {
      'Authorization': POSTIZ_KEY,
      'Content-Type':  'application/json',
    },
    body: JSON.stringify(payload),
  });

  const responseText = await res.text();
  let responseData;
  try { responseData = JSON.parse(responseText); } catch { responseData = responseText; }

  if (!res.ok) {
    throw new Error(`Postiz ${res.status}: ${typeof responseData === 'string' ? responseData : JSON.stringify(responseData)}`);
  }

  return responseData;
}

// ── Trigger video generation ──────────────────────────────────────────────────
// Calls the script defined in config.videoGen.script with angle + schedule args.
// If no script is configured, logs a TODO and marks as skipped.
function triggerVideoGen(post) {
  const videoGenScript = config.videoGen?.script
    ? path.resolve(BASE_DIR, config.videoGen.script)
    : null;

  if (!videoGenScript || !fs.existsSync(videoGenScript)) {
    console.log(`  No video-gen script configured. Set config.videoGen.script to enable.`);
    console.log(`  TODO: generate video for angle "${post.hook}" and post to TikTok at ${post.scheduledTime}`);
    return { ok: false, skipped: true };
  }

  const scheduleArg = post.scheduledTime ? `--schedule "${post.scheduledTime}"` : '';
  const angleArg    = post.angleId       ? `--angle ${post.angleId}`            : '';
  const cmd         = `node "${videoGenScript}" ${angleArg} ${scheduleArg}`.trim();

  console.log(`  Running: ${cmd}`);

  try {
    const output = execSync(cmd, {
      cwd:       BASE_DIR,
      timeout:   600000,    // 10 min for image/video gen
      stdio:     ['ignore', 'pipe', 'pipe'],
      maxBuffer: 10 * 1024 * 1024,
    });
    process.stdout.write(output.toString());
    return { ok: true };
  } catch (err) {
    const stderr = err.stderr ? err.stderr.toString() : '';
    const stdout = err.stdout ? err.stdout.toString() : '';
    process.stdout.write(stdout);
    process.stderr.write(stderr);
    console.error(`  Video gen failed: ${err.message}`);
    return { ok: false };
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────
(async () => {
  const today = getArg('day') || new Date().toISOString().slice(0, 10);
  const now   = new Date();

  console.log('='.repeat(60));
  console.log('DAILY PUBLISHER — Indie App Marketing Pipeline');
  console.log('='.repeat(60));
  console.log(`App:  ${config.app?.name || 'unknown'}`);
  console.log(`Date: ${today}`);
  console.log(`Mode: ${dryRun ? 'DRY RUN' : 'LIVE'}${textOnly ? ' (text only)' : ''}\n`);

  // Find plan
  const planPath = findPlanForDate(today);
  if (!planPath) {
    console.error(`No weekly plan found for ${today}. Run weekly-planner.js first.`);
    process.exit(1);
  }

  const plan = JSON.parse(fs.readFileSync(planPath, 'utf-8'));
  console.log(`Using plan: ${path.basename(planPath)}`);
  console.log(`Plan period: ${plan.meta.weekStart} — ${plan.meta.weekEnd}\n`);

  // Get today's posts
  const todayData = plan.days.find(d => d.day === today);
  if (!todayData) {
    console.log(`No posts planned for ${today}.`);
    process.exit(0);
  }

  let todayPosts = todayData.posts;

  if (textOnly) {
    todayPosts = todayPosts.filter(p => TEXT_PLATFORMS.has(p.platform));
  }

  if (skipPast) {
    const before  = todayPosts.length;
    todayPosts    = todayPosts.filter(p => new Date(p.scheduledTime) > now);
    const skipped = before - todayPosts.length;
    if (skipped > 0) console.log(`Skipped ${skipped} past-time post(s)`);
  }

  if (todayPosts.length === 0) {
    console.log('No posts to schedule for today.');
    process.exit(0);
  }

  todayPosts.sort((a, b) => new Date(a.scheduledTime) - new Date(b.scheduledTime));

  // Display summary
  const byPlatform = {};
  for (const p of todayPosts) {
    byPlatform[p.platform] = (byPlatform[p.platform] || 0) + 1;
  }
  console.log(`Today's posts: ${todayPosts.length} total`);
  for (const [plat, count] of Object.entries(byPlatform)) {
    console.log(`  ${plat}: ${count}`);
  }
  console.log('');

  const results = [];

  for (let i = 0; i < todayPosts.length; i++) {
    const post    = todayPosts[i];
    const timeStr = post.scheduledTimeReadable || new Date(post.scheduledTime).toLocaleTimeString();
    const preview = (post.content || post.hook || post.caption || '').split('\n')[0].substring(0, 60);

    console.log(`[${i + 1}/${todayPosts.length}] ${post.platform.toUpperCase()} | ${post.slot} | ${timeStr}`);
    if (preview) console.log(`  "${preview}"`);

    if (dryRun) {
      console.log(`  [DRY RUN] Would schedule\n`);
      results.push({ id: post.id, platform: post.platform, status: 'dry-run', slot: post.slot });
      continue;
    }

    // ── Text posts (X + Facebook) ──
    if (TEXT_PLATFORMS.has(post.platform) && post.content) {
      try {
        const response = await withRetry(() => scheduleTextPost(post));
        const postizId = response?.id || response?._id || response?.postId
          || (Array.isArray(response) && response[0]?.postId);

        console.log(`  Scheduled! Postiz ID: ${postizId || '(no id in response)'}\n`);
        results.push({ id: post.id, platform: post.platform, status: 'scheduled', slot: post.slot, postizId });
      } catch (err) {
        console.error(`  FAILED: ${err.message}\n`);
        results.push({ id: post.id, platform: post.platform, status: 'failed', slot: post.slot, error: err.message });
      }

    // ── TikTok (video gen) ──
    } else if (post.platform === 'tiktok' && post.requiresVideoGen) {
      const MAX_VIDEO_RETRIES = 2;
      let videoResult = null;

      for (let vRetry = 0; vRetry <= MAX_VIDEO_RETRIES; vRetry++) {
        if (vRetry > 0) {
          const wait = vRetry * 60000;
          console.log(`  Video gen retry ${vRetry}/${MAX_VIDEO_RETRIES} — waiting ${wait / 1000}s...`);
          await new Promise(r => setTimeout(r, wait));
        }
        videoResult = triggerVideoGen(post);
        if (videoResult.ok) break;
      }

      const { ok, skipped } = videoResult;
      if (skipped) {
        results.push({ id: post.id, platform: post.platform, status: 'skipped', slot: post.slot });
        console.log('');
      } else {
        results.push({ id: post.id, platform: post.platform, status: ok ? 'video-gen-ok' : 'video-gen-failed', slot: post.slot });
        console.log(`  Video gen: ${ok ? 'OK' : `FAILED after ${MAX_VIDEO_RETRIES + 1} attempts`}\n`);
      }

    // ── YouTube Shorts (handled via TikTok crossPost) ──
    } else if (post.platform === 'youtube' && post.reusesVideo) {
      console.log(`  Handled via TikTok crossPost\n`);
      results.push({ id: post.id, platform: post.platform, status: 'handled-via-crosspost', slot: post.slot });

    } else {
      console.log(`  Skipped (unhandled type: ${post.platform}/${post.type})\n`);
      results.push({ id: post.id, platform: post.platform, status: 'skipped', slot: post.slot });
    }

    // Brief pause between API calls
    if (i < todayPosts.length - 1 && !dryRun) {
      await new Promise(r => setTimeout(r, 2000));
    }
  }

  // ── Results summary ──
  const scheduled  = results.filter(r => r.status === 'scheduled').length;
  const failed     = results.filter(r => r.status === 'failed').length;
  const videoOk    = results.filter(r => r.status === 'video-gen-ok').length;
  const videoFail  = results.filter(r => r.status === 'video-gen-failed').length;

  const statusIcons = {
    'scheduled':           '[OK]',
    'dry-run':             '[DRY]',
    'failed':              '[FAIL]',
    'video-gen-ok':        '[VID]',
    'video-gen-failed':    '[VFAIL]',
    'handled-via-crosspost': '[XPOST]',
    'skipped':             '[SKIP]',
  };

  console.log('='.repeat(60));
  console.log(`RESULTS: ${scheduled} scheduled, ${videoOk} video OK, ${failed + videoFail} failed, ${results.length} total`);
  for (const r of results) {
    console.log(`  ${statusIcons[r.status] || '[?]'} ${r.platform.padEnd(10)} ${r.slot}`);
  }

  // ── Write log ──
  if (!dryRun) {
    fs.mkdirSync(LOGS_DIR, { recursive: true });
    const logPath = path.join(LOGS_DIR, `${today}.json`);
    fs.writeFileSync(logPath, JSON.stringify({
      date:      today,
      app:       config.app?.name,
      results,
      timestamp: new Date().toISOString(),
      version:   'indie-app-marketing-pipeline-v1',
    }, null, 2));
    console.log(`\nLog: ${logPath}`);
  }

  const totalFailed = failed + videoFail;
  if (totalFailed > 0) process.exit(1);
})();

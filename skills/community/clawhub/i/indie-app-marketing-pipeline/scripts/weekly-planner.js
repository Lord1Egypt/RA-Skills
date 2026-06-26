#!/usr/bin/env node
/**
 * Weekly Content Planner — Indie App Marketing Pipeline
 *
 * Generates a full week's content plan from a content bank + templates.
 * No LLM calls needed — all content is derived from existing angles via templates.
 *
 * Platforms: TikTok (3/day), YouTube Shorts (3/day), X/Twitter (2/day), Facebook (Mon/Wed/Fri)
 *
 * Output: plans/weekly-plan-YYYY-MM-DD.json
 *
 * Usage:
 *   node weekly-planner.js [--week YYYY-MM-DD] [--dry-run] [--days N] [--config path/to/config.json]
 *
 * --week:    Start date for the plan (default: next Monday, or today if --days is used)
 * --dry-run: Preview without writing plan file
 * --days:    Number of days to plan (default: 7)
 * --config:  Path to config.json (default: ./config.json)
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// ── CLI ──────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);

function getArg(name) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 ? args[idx + 1] : null;
}

const dryRun    = args.includes('--dry-run');
const customDays = getArg('days') ? parseInt(getArg('days'), 10) : null;
const configArg  = getArg('config');

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

// App settings — all values come from config, nothing hardcoded
const APP_NAME     = config.app?.name     || 'MyApp';
const APP_HANDLE   = config.app?.handle   || '@myapp';
const APP_STORE_URL = config.app?.appStoreUrl || '';
const WEBSITE_URL   = config.app?.websiteUrl  || APP_STORE_URL;
const TOPIC_CATEGORY = config.app?.topicCategory || 'productivity';
const DEFAULT_HASHTAGS = config.app?.defaultHashtags || `#${APP_NAME} #IndieApp #AppStore`;
const DEFAULT_CTA = config.app?.defaultCta || `${APP_NAME} — available on the App Store`;
const TIMEZONE_OFFSET = config.schedule?.timezoneOffset || '-05:00'; // default EST

// Paths — all relative to the working directory (where config.json lives)
const BASE_DIR = path.dirname(CONFIG_PATH);
const PLANS_DIR = path.join(BASE_DIR, config.paths?.plans || 'plans');

// Content bank path — configurable
const CONTENT_BANK_PATH = path.join(
  BASE_DIR,
  config.paths?.contentBank || 'content-bank.json'
);
const FB_CONTENT_BANK_PATH = path.join(
  BASE_DIR,
  config.paths?.fbContentBank || 'fb-brand-content-bank.json'
);
const HISTORY_PATH = path.join(
  BASE_DIR,
  config.paths?.history || 'posting-history.json'
);
const TEMPLATES_PATH = config.paths?.templates
  ? path.join(BASE_DIR, config.paths.templates)
  : path.join(__dirname, '..', 'assets', 'content-templates.json');
const HASHTAG_BANK_PATH = path.join(BASE_DIR, 'hashtag-bank.json');

// ── Load data ────────────────────────────────────────────────────────────────
function loadJSON(filePath, fallback = null) {
  if (!fs.existsSync(filePath)) {
    if (fallback !== null) return fallback;
    console.error(`Required file not found: ${filePath}`);
    process.exit(1);
  }
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch (e) {
    console.error(`Failed to parse ${filePath}: ${e.message}`);
    process.exit(1);
  }
}

const contentBank  = loadJSON(CONTENT_BANK_PATH);
const history      = loadJSON(HISTORY_PATH, { posted: [], lastApp: null });
const templates    = loadJSON(TEMPLATES_PATH);
const fbBrandBank  = loadJSON(FB_CONTENT_BANK_PATH, { brand: [] });
const hashtagBank  = loadJSON(HASHTAG_BANK_PATH, { trending: [], evergreen: [] });

const postedIds   = new Set((history.posted || []).map(p => p.id));
const postedFbIds = new Set((history.postedFbBrand || []).map(p => p.id));

// Normalize content bank: support both flat array and keyed object
// If array: use as-is. If object: merge all arrays under each key.
let allAngles;
if (Array.isArray(contentBank)) {
  allAngles = contentBank;
} else {
  allAngles = Object.values(contentBank).flat();
}

// ── Posting schedule ─────────────────────────────────────────────────────────
// Override any of these in config.json under "schedule"
const ANGLES_PER_DAY = config.schedule?.anglesPerDay || 3;

const VISUAL_SCHEDULE = config.schedule?.visual || [
  { slot: 'tiktok-1',        time: '08:00', platform: 'tiktok',   videoIndex: 0 },
  { slot: 'youtube-short-1', time: '08:15', platform: 'youtube',  videoIndex: 0, reusesVideo: true, reusesSlot: 'tiktok-1' },
  { slot: 'tiktok-2',        time: '13:00', platform: 'tiktok',   videoIndex: 1 },
  { slot: 'youtube-short-2', time: '13:15', platform: 'youtube',  videoIndex: 1, reusesVideo: true, reusesSlot: 'tiktok-2' },
  { slot: 'tiktok-3',        time: '18:00', platform: 'tiktok',   videoIndex: 2 },
  { slot: 'youtube-short-3', time: '18:15', platform: 'youtube',  videoIndex: 2, reusesVideo: true, reusesSlot: 'tiktok-3' },
];

const X_SCHEDULE = config.schedule?.x || [
  { slot: 'x-1', time: '10:30', platform: 'x', tweetIndex: 0, linkType: 'appStore' },
  { slot: 'x-2', time: '16:00', platform: 'x', tweetIndex: 1, linkType: 'website'  },
];

const FB_SCHEDULE = config.schedule?.fb || [
  { slot: 'fb-text-1', time: '12:00', platform: 'facebook', type: 'brand-post' },
];

// Days of week that get a Facebook post (1=Mon, 3=Wed, 5=Fri)
const FB_DAYS = config.schedule?.fbDays || [1, 3, 5];

// ── Date helpers ─────────────────────────────────────────────────────────────
function getNextMonday() {
  const now = new Date();
  const day = now.getDay();
  const daysUntilMonday = day === 1 ? 7 : (1 - day + 7) % 7 || 7;
  const monday = new Date(now);
  monday.setDate(now.getDate() + daysUntilMonday);
  return monday.toISOString().slice(0, 10);
}

function addDays(dateStr, days) {
  const d = new Date(dateStr + 'T00:00:00');
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

function dayName(dateStr) {
  return new Date(dateStr + 'T12:00:00').toLocaleDateString('en-US', { weekday: 'long' });
}

function toScheduledISO(dateStr, timeStr) {
  return `${dateStr}T${timeStr}:00.000${TIMEZONE_OFFSET}`;
}

// ── Content selection ────────────────────────────────────────────────────────
function getUnusedAngles() {
  return allAngles.filter(a => !postedIds.has(a.id));
}

function pickAnglesForWeek(numDays) {
  const unused = getUnusedAngles();
  console.log(`Available: ${unused.length} unused angles (${allAngles.length} total)`);

  if (unused.length === 0) {
    console.error('No unused angles! Add more to content-bank.json.');
    process.exit(1);
  }

  // Simple sequential pick — no alternating apps since single-app by default
  const needed = numDays * ANGLES_PER_DAY;
  return unused.slice(0, needed);
}

// ── Facebook brand post picker ────────────────────────────────────────────────
function pickFbBrandPosts(count) {
  const allFb = Array.isArray(fbBrandBank)
    ? fbBrandBank
    : Object.values(fbBrandBank).flat();

  const unused = allFb.filter(p => !postedFbIds.has(p.id));
  return unused.slice(0, count);
}

// ── X Tweet generator ─────────────────────────────────────────────────────────
function getHashtags() {
  const trending  = Array.isArray(hashtagBank.trending)  ? hashtagBank.trending  : [];
  const evergreen = Array.isArray(hashtagBank.evergreen) ? hashtagBank.evergreen : [];

  const pool = [...trending.slice(0, 2), ...evergreen.slice(0, 2)];
  if (pool.length > 0) {
    return pool.slice(0, 3).map(h => h.tag || h).join(' ');
  }
  return DEFAULT_HASHTAGS.split(' ').slice(0, 3).join(' ');
}

function generateXTweet(angle, tweetIndex) {
  const hashtags = getHashtags();
  const link = tweetIndex % 2 === 0 ? APP_STORE_URL : WEBSITE_URL;
  const hook  = angle.hook;
  const texts = angle.texts || [];

  // Rotate through natural-voice patterns (no marketing-speak)
  const patterns = [
    // Observation
    () => {
      const insight = texts.slice(1, 3).map(t => t.replace(/\n/g, ' ')).join(' ');
      return `${hook}.\n\n${insight}`;
    },
    // Dev perspective
    () => {
      const detail = texts[2]?.replace(/\n/g, ' ') || texts[1]?.replace(/\n/g, ' ') || '';
      return `Something I keep hearing from people: ${hook.toLowerCase()}.\n\n${detail}`;
    },
    // Quick thought
    () => `${hook}. That's it. That's the tweet.\n\n${hashtags}`,
    // Engagement question
    () => {
      const question = hook.toLowerCase().replace(/^i /, 'you ').replace(/^my /, 'your ');
      return `Be honest: ${question}?\n\nBecause same.`;
    },
    // Story snippet
    () => texts.slice(0, 2).map(t => t.replace(/\n/g, ' ')).join(' '),
  ];

  const patternFn = patterns[tweetIndex % patterns.length];
  let body = patternFn();

  // Include App Store link on even-indexed tweets
  if (tweetIndex % 2 === 0 && link) {
    body = `${body}\n\n${link}`;
  }

  // Append hashtags if not already in body
  if (!body.includes('#') && hashtags) {
    body = `${body}\n\n${hashtags}`;
  }

  return body;
}

// Trim to X 280-char limit while preserving the last line (link or hashtags)
function trimToXLimit(text) {
  if (text.length <= 280) return text;

  const lines    = text.split('\n');
  const lastLine = lines[lines.length - 1];
  const isAnchor = lastLine.startsWith('http') || lastLine.startsWith('#');

  if (isAnchor) {
    const bodyLines = lines.slice(0, -1);
    const bodyClean = bodyLines.join('\n').replace(/#\S+/g, '').trim();
    const candidate = `${bodyClean}\n\n${lastLine}`;
    if (candidate.length <= 280) return candidate;

    const sentences = bodyClean.split(/(?<=[.!?])\s+/);
    let result = '';
    for (const s of sentences) {
      const next = (result ? `${result} ${s}` : s).trim();
      if (`${next}\n\n${lastLine}`.length > 280) break;
      result = next;
    }
    if (result) return `${result}\n\n${lastLine}`;
    return `${bodyClean.substring(0, 277 - lastLine.length - 4)}...\n\n${lastLine}`;
  }

  return `${text.substring(0, 277)}...`;
}

// ── Build the weekly plan ─────────────────────────────────────────────────────
function buildWeeklyPlan(weekStart, numDays) {
  const angles = pickAnglesForWeek(numDays);

  const daysAvailable = Math.floor(angles.length / ANGLES_PER_DAY);
  const daysToPlan    = Math.min(daysAvailable, numDays);

  if (daysToPlan === 0) {
    console.error('Not enough angles to plan even one day.');
    process.exit(1);
  }

  // Collect dates that need a Facebook post
  const fbDayIndices = [];
  for (let i = 0; i < daysToPlan; i++) {
    const dow = new Date(addDays(weekStart, i) + 'T12:00:00').getDay();
    if (FB_DAYS.includes(dow)) fbDayIndices.push(i);
  }

  const fbBrandPosts = pickFbBrandPosts(fbDayIndices.length);
  console.log(`FB posts available: ${fbBrandPosts.length} (need ${fbDayIndices.length})`);
  console.log(`\nAngles available: ${angles.length} (${daysAvailable} full days)`);
  console.log(`Planning ${daysToPlan} posting days starting ${weekStart}\n`);

  const plan = {
    meta: {
      weekStart,
      weekEnd:    addDays(weekStart, daysToPlan - 1),
      createdAt:  new Date().toISOString(),
      app:        APP_NAME,
      platforms:  ['tiktok', 'youtube', 'x', 'facebook'],
      note:       'Generated by indie-app-marketing-pipeline weekly-planner — template-driven, no LLM',
    },
    days: [],
  };

  let fbPostIndex = 0;

  for (let dayIdx = 0; dayIdx < daysToPlan; dayIdx++) {
    const day      = addDays(weekStart, dayIdx);
    const dayLabel = dayName(day);
    const dow      = new Date(day + 'T12:00:00').getDay();

    const dayAngles = angles.slice(
      dayIdx * ANGLES_PER_DAY,
      dayIdx * ANGLES_PER_DAY + ANGLES_PER_DAY
    );

    console.log(`${dayLabel} ${day}:`);
    dayAngles.forEach((a, i) => console.log(`  Angle ${i + 1}: "${a.hook}"`));

    const dayPosts = [];

    // ── Visual posts (TikTok + YouTube) ──
    for (const slot of VISUAL_SCHEDULE) {
      const scheduledTime         = toScheduledISO(day, slot.time);
      const scheduledTimeReadable = `${dayLabel.slice(0, 3)} ${day.slice(5)}, ${slot.time}`;
      const angle                 = dayAngles[slot.videoIndex] || dayAngles[0];

      if (slot.platform === 'tiktok') {
        dayPosts.push({
          id:               `${slot.slot}-${day}`,
          slot:             slot.slot,
          day, dayLabel,
          angleId:          angle.id,
          hook:             angle.hook,
          caption:          angle.caption || '',
          platform:         'tiktok',
          type:             'video',
          scheduledTime,
          scheduledTimeReadable,
          requiresVideoGen: true,
        });
      } else if (slot.platform === 'youtube') {
        dayPosts.push({
          id:                  `${slot.slot}-${day}`,
          slot:                slot.slot,
          day, dayLabel,
          angleId:             angle.id,
          hook:                angle.hook,
          platform:            'youtube',
          type:                'short',
          reusesVideo:         true,
          reusesVideoFrom:     `${slot.reusesSlot}-${day}`,
          scheduledTime,
          scheduledTimeReadable,
          note:                `Reuse video from ${slot.reusesSlot}-${day}`,
        });
      }
    }

    // ── X tweets ──
    for (const slot of X_SCHEDULE) {
      const scheduledTime         = toScheduledISO(day, slot.time);
      const scheduledTimeReadable = `${dayLabel.slice(0, 3)} ${day.slice(5)}, ${slot.time}`;
      const angle = dayAngles[slot.tweetIndex % dayAngles.length] || dayAngles[0];
      const tweet = trimToXLimit(generateXTweet(angle, slot.tweetIndex));

      dayPosts.push({
        id:                  `${slot.slot}-${day}`,
        slot:                slot.slot,
        day, dayLabel,
        angleId:             angle.id,
        platform:            'x',
        type:                'tweet',
        content:             tweet,
        charCount:           tweet.length,
        scheduledTime,
        scheduledTimeReadable,
      });
    }

    // ── Facebook (Mon/Wed/Fri only) ──
    if (FB_DAYS.includes(dow)) {
      const fbPost = fbBrandPosts[fbPostIndex];
      if (fbPost) {
        const scheduledTime         = toScheduledISO(day, '12:00');
        const scheduledTimeReadable = `${dayLabel.slice(0, 3)} ${day.slice(5)}, 12:00`;
        dayPosts.push({
          id:                  `fb-text-1-${day}`,
          slot:                'fb-text-1',
          day, dayLabel,
          fbBrandId:           fbPost.id,
          platform:            'facebook',
          type:                'brand-post',
          content:             fbPost.content || '',
          scheduledTime,
          scheduledTimeReadable,
          note:                `FB brand post${fbPost.pattern ? `: ${fbPost.pattern}` : ''}`,
        });
        fbPostIndex++;
      }
    }

    plan.days.push({ day, dayLabel, angles: dayAngles.map(a => ({ id: a.id, hook: a.hook })), posts: dayPosts });
  }

  // Flatten for consumers that expect a top-level allPosts array
  plan.allPosts = plan.days.flatMap(d => d.posts);

  // Summary counts
  plan.meta.anglesUsed  = daysToPlan * ANGLES_PER_DAY;
  plan.meta.totalPosts  = plan.allPosts.length;
  plan.meta.byPlatform  = {
    tiktok:   plan.allPosts.filter(p => p.platform === 'tiktok').length,
    youtube:  plan.allPosts.filter(p => p.platform === 'youtube').length,
    x:        plan.allPosts.filter(p => p.platform === 'x').length,
    facebook: plan.allPosts.filter(p => p.platform === 'facebook').length,
  };

  return plan;
}

// ── Main ──────────────────────────────────────────────────────────────────────
const defaultDays = customDays || 7;
const weekStart   = getArg('week') || (customDays
  ? new Date().toISOString().slice(0, 10)
  : getNextMonday()
);

console.log('='.repeat(60));
console.log('WEEKLY CONTENT PLANNER — Indie App Marketing Pipeline');
console.log('='.repeat(60));
console.log(`App:   ${APP_NAME} (${APP_HANDLE})`);
console.log(`Start: ${weekStart} — ${addDays(weekStart, defaultDays - 1)} (${defaultDays} days)`);
console.log(`Mode:  ${dryRun ? 'DRY RUN' : 'LIVE'}\n`);

const plan = buildWeeklyPlan(weekStart, defaultDays);

// ── Summary ──
console.log('\n' + '='.repeat(60));
console.log('PLAN SUMMARY');
console.log('='.repeat(60));
console.log(`Posting days:     ${plan.days.length}`);
console.log(`Angles used:      ${plan.meta.anglesUsed}`);
console.log(`Total posts:      ${plan.meta.totalPosts}`);
console.log(`  TikTok:         ${plan.meta.byPlatform.tiktok}`);
console.log(`  YouTube Shorts: ${plan.meta.byPlatform.youtube} (reuse TikTok video)`);
console.log(`  X tweets:       ${plan.meta.byPlatform.x}`);
console.log(`  Facebook:       ${plan.meta.byPlatform.facebook}`);

if (dryRun) {
  console.log('\n[DRY RUN] Plan not written. Preview:');
  const sampleDay = plan.days[0];
  if (sampleDay) {
    console.log(`\nSample day: ${sampleDay.dayLabel} ${sampleDay.day}`);
    const sampleX = sampleDay.posts.find(p => p.platform === 'x');
    if (sampleX) {
      console.log(`\nSample X tweet (${sampleX.charCount} chars):\n${sampleX.content}`);
    }
  }
} else {
  fs.mkdirSync(PLANS_DIR, { recursive: true });
  const planPath = path.join(PLANS_DIR, `weekly-plan-${weekStart}.json`);
  fs.writeFileSync(planPath, JSON.stringify(plan, null, 2));
  console.log(`\nPlan written to: ${planPath}`);
}

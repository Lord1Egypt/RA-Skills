#!/usr/bin/env node
/**
 * 龙虾好运势 — main entry
 *
 * Usage:
 *   node src/index.js --action status          # Show OB identity + profile + history
 *   node src/index.js --action fortune          # Full flow: calendar + fortune data for CC
 *   node src/index.js --action l1-calendar      # Call L1 CalendarSvc
 *   node src/index.js --action filter-stories [--emotion <e>] [--life-phase <p>]
 *   node src/index.js --action generate-card --type-name <t> --one-liner <text> --story-title <s> --solar-term <term>
 */
import { createOceanBus } from "oceanbus";
import { getClient } from "./ob-client.js";
import { loadProfile, getDimensions, saveDimensions as saveDims } from "./profile.js";
import { loadHistory, addEntry, getStreak, isSunday, hasTodayReading, getWeekEntries, getRecentStoryIds, recordStoryUsage } from "./history.js";
import { initPreferences } from "./preferences.js";
import { getLocalCalendar } from "./local-calendar.js";
import { generateTermInsight, pickGenre, generateMicroAction } from "./cal-templates.js";
import { hasConsent } from "./consent.js";
import { isValidCode, needsReEvaluation, getTypeName, filterCorpus } from "./dimensions.js";
import { generateCard } from "./card-generator.js";
import os from "node:os";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));

const BASE_URL = process.env.OCEANBUS_URL || "https://ai.ihaola.com.cn/api/l0";
// L1 CalendarSvc / StoryEngine / DiscoverySvc public OB address — NOT a secret.
// This is the service's OpenID on the OceanBus network, like a public server address.
// Users need it to reach L1; without it, the skill degrades to local-only mode.
const L1_OPENID = process.env.LUCKY_LOBSTER_SVC_OPENID || "cOrquik8RuElUIUakY7FAmB3N5gdmXRR1Yg2b-GX3WeezJGSZVVV0fRd7eknILQodV9ATrpM93N4gYyP";

async function main() {
  const action = getArg("--action") || "status";
  switch (action) {
    case "status":       return await cmdStatus();
    case "l1-calendar":  return await cmdL1Calendar();
    case "fortune":            return await cmdFortune();
    case "save-dimensions":    return await cmdSaveDimensions();
    case "filter-stories":     return await cmdFilterStories();
    case "record-story":      return await cmdRecordStory();
    case "discovery":          return await cmdDiscovery();
    case "discovery-shown":    return await cmdDiscoveryShown();
    case "generate-card":     return await cmdGenerateCard();
    default:
      console.log(JSON.stringify({ error: `unknown action: ${action}` }));
      process.exit(1);
  }
}

// ── Status ──
async function cmdStatus() {
  const { ob, openid, agentId, created } = await getClient();
  const profile = loadProfile();
  const history = loadHistory();

  console.log(JSON.stringify({
    status: "ok",
    version: "0.7.0",
    consent_given: hasConsent(),
    identity: { created_this_session: created },
    profile: { exists: !!profile },
    history: { streak: history.streak, total_entries: history.entries.length },
  }, null, 2));
}

// ── Fortune (main flow) ──
async function cmdFortune() {
  // Programmatic consent gate — must pass before any processing
  if (!hasConsent()) {
    console.log(JSON.stringify({
      status: "consent_required",
      message: "First run — explicit user consent required before fortune reading.",
      _instructions: "Show the consent prompt from SKILL.md Step 0. Wait for user to type 同意/好/yes/ok. After consent, tell the user to say 看运势 again. Never ask for consent twice.",
    }, null, 2));
    return;
  }

  await getClient(); // ensure OB identity exists
  const profile = loadProfile();
  const prefs = initPreferences();
  const today = new Date().toISOString().slice(0, 10);

  // 1. Get calendar data (L1 if available, else local fallback)
  let calendar;
  if (L1_OPENID) {
    try {
      calendar = await l1Request(L1_OPENID, "fortune:calendar", { date: today, city: profile?.city || "" });
    } catch (_) {
      calendar = getLocalCalendar(today);
    }
  } else {
    calendar = getLocalCalendar(today);
  }

  // 2. Determine flow type
  const isFirst = !hasTodayReading() && (loadHistory().entries.length === 0);
  const isSundayReview = isSunday() && !isFirst;

  // 3. Generate solar term insight (Skill-side, no L1 needed)
  const termContext = calendar.solar_term?.name ? {
    term_insight: generateTermInsight(calendar, ""), // context filled by CC
    genre: pickGenre("", { entries: loadHistory().entries, week_entries: getWeekEntries() }),
    micro_action: generateMicroAction("充电日"), // genre filled by CC
  } : null;

  // 4. Personality state
  const dims = getDimensions();
  const personality = {
    has_dimensions: !!dims,
    needs_reevaluation: dims ? needsReEvaluation(dims.last_evaluated) : true,
    dimensions: dims || null,
    label_for_compat: dims?.type_name || null,
  };

  // 5. Build output for CC
  console.log(JSON.stringify({
    status: "ok",
    flow: isFirst ? "first_reading" : (isSundayReview ? "weekly_review" : "daily_fortune"),
    personality,
    data: {
      profile: profile || { exists: false },
      calendar,
      history: {
        is_first_time: isFirst,
        is_sunday: isSundayReview,
        streak: getStreak(),
        week_entries: isSundayReview ? getWeekEntries() : [],
      },
      term: termContext,
      preferences: {
        push_enabled: prefs.push_enabled,
      },
    },
    _instructions: isFirst
      ? "FIRST READING. Step 2A: scan conversation for emotion/topic/phase. Step 2B: analyze 5 dimensions in paragraph format (NOT tables), cite evidence for each, save to --action save-dimensions. Step 3: call --action filter-stories, pick best match. Step 5: render using First Reading format — tag hook + 5 paragraphs + story + blindspot + advice. Use blank lines between sections."
      : (isSundayReview
        ? "SUNDAY REVIEW. Summarize this week + update personality insight + call filter-stories + render daily fortune."
        : "DAILY FORTUNE. ALWAYS call --action filter-stories first. Then render with 节气感悟 + cultivation tip + micro-action + STORY (mandatory). Keep it light, use paragraph format."),
  }, null, 2));
}

// ── Save Dimensions ──
async function cmdSaveDimensions() {
  const code = getArg("--code") || "";
  const confidence = parseFloat(getArg("--confidence") || "0");

  if (!isValidCode(code)) {
    console.log(JSON.stringify({ status: "error", message: `invalid code: ${code}` }));
    process.exit(1);
  }
  if (!confidence || confidence <= 0) {
    console.log(JSON.stringify({ status: "error", message: "--confidence must be > 0" }));
    process.exit(1);
  }

  // Auto-resolve type_name from code — 32-type table is the single source of truth
  const typeName = getTypeName(code);
  saveDims({ code, type_name: typeName, confidence });
  console.log(JSON.stringify({ status: "ok", code, type_name: typeName, confidence }));
}

// ── Filter Stories ──
async function cmdFilterStories() {
  const dims = getDimensions();
  if (!dims?.code) {
    console.log(JSON.stringify({ candidates: [], reason: "no dimensions stored" }));
    return;
  }

  const today = new Date().toISOString().slice(0, 10);
  const cal = getLocalCalendar(today);
  const season = cal?.season?.name || "";
  const emotion = getArg("--emotion") || "";
  const lifePhase = getArg("--life-phase") || "";

  let result;

  // Try L1 first
  if (L1_OPENID) {
    try {
      result = await l1Request(L1_OPENID, "fortune:filter-stories", {
        code: dims.code, season, emotion, lifePhase
      });
    } catch (_) { /* fall through to local fallback */ }
  }

  // Local fallback
  if (!result) {
    const fallback = JSON.parse(fs.readFileSync(
      path.join(__dirname, "corpus-fallback.json"), "utf-8"
    ));
    result = {
      candidates: filterCorpus(dims.code, fallback, { season, emotion, lifePhase }),
      count: 0,
      context: { season, emotion, lifePhase },
      fallback: true,
    };
    result.count = result.candidates.length;
  }

  // Story rotation: exclude stories used in last 14 days, keep min 3 candidates
  const recentIds = getRecentStoryIds(14);
  if (recentIds.size > 0 && result.candidates.length > 3) {
    const fresh = result.candidates.filter(c => !recentIds.has(c.id));
    if (fresh.length >= 3) {
      result.candidates = fresh;
      result.count = fresh.length;
      result._rotation = { excluded: recentIds.size, excluded_ids: [...recentIds] };
    }
    // else: too few fresh candidates — keep originals (rotation skipped)
  }

  console.log(JSON.stringify(result, null, 2));
}

// ── Record Story Usage ──
async function cmdRecordStory() {
  const storyId = getArg("--id") || "";
  if (!storyId) {
    console.log(JSON.stringify({ status: "error", message: "--id required" }));
    process.exit(1);
  }
  const ok = recordStoryUsage(storyId);
  console.log(JSON.stringify({ status: ok ? "ok" : "skipped", story_id: storyId }));
}

// ── L1 Calendar ──
async function cmdL1Calendar() {
  if (!L1_OPENID) { console.log(JSON.stringify(getLocalCalendar())); return; }
  const date = getArg("--date") || new Date().toISOString().slice(0, 10);
  const city = getArg("--city") || "";
  console.log(JSON.stringify(await l1Request(L1_OPENID, "fortune:calendar", { date, city }), null, 2));
}

// ── Discovery ──
async function cmdDiscovery() {
  if (!L1_OPENID) { console.log(JSON.stringify({ clawhub: [], mooc: [] })); return; }
  const { ob, openid } = await getClient();
  const result = await l1Request(L1_OPENID, "fortune:discovery", { openid });
  console.log(JSON.stringify(result, null, 2));
}

async function cmdDiscoveryShown() {
  if (!L1_OPENID) { console.log(JSON.stringify({ error: "L1 not configured" })); process.exit(1); }
  const source = getArg("--source") || "";
  const slug = getArg("--slug") || "";
  if (!source || !slug) { console.log(JSON.stringify({ error: "need --source and --slug" })); process.exit(1); }
  const { ob, openid } = await getClient();
  const result = await l1Request(L1_OPENID, "fortune:discovery:shown", { openid, source, slug });
  console.log(JSON.stringify(result, null, 2));
}

// ── Generate Card (local, no OB/L1 needed) ──
async function cmdGenerateCard() {
  const typeName = getArg("--type-name") || "";
  const oneLiner = getArg("--one-liner") || "";
  const storyTitle = getArg("--story-title") || "";
  const solarTerm = getArg("--solar-term") || "";
  const date = getArg("--date") || new Date().toISOString().slice(0, 10);

  if (!typeName || !oneLiner || !solarTerm) {
    console.log(JSON.stringify({
      error: "missing required args: --type-name, --one-liner, --solar-term"
    }));
    process.exit(1);
  }

  try {
    const result = await generateCard({
      type_name: typeName,
      one_liner: oneLiner,
      story_title: storyTitle,
      solar_term: solarTerm,
      date,
    });

    // Save to ~/.lucky-lobster/cards/
    const outDir = path.join(os.homedir(), ".lucky-lobster", "cards");
    fs.mkdirSync(outDir, { recursive: true });
    const safeDate = date.replace(/[:]/g, "-");
    const outFile = path.join(outDir, `${safeDate}-${solarTerm}-${typeName}.png`);
    fs.writeFileSync(outFile, Buffer.from(result.card_base64, "base64"));

    console.log(JSON.stringify({
      status: "ok",
      card_id: result.card_id,
      file: outFile,
      size_kb: Math.round(fs.statSync(outFile).size / 1024),
    }, null, 2));
  } catch (e) {
    console.log(JSON.stringify({ error: e.message }));
    process.exit(1);
  }
}

// ── L1 Request/Response helper ──
async function l1Request(to, action, data) {
  const { ob } = await getClient();
  const requestId = `req_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => { stop(); reject(new Error(`L1 ${action} timed out`)); }, 15000);
    const stop = ob.startListening(async (msg) => {
      try {
        const resp = JSON.parse(msg.content);
        if (resp.request_id === requestId) { clearTimeout(timeout); stop(); resolve(resp); }
      } catch (_) {}
    }, { intervalMs: 500, skipSelf: true });
    ob.sendJson(to, { action, request_id: requestId, ...data }).catch((e) => { clearTimeout(timeout); stop(); reject(e); });
  });
}

function getArg(name) {
  const idx = process.argv.indexOf(name);
  return idx >= 0 && idx + 1 < process.argv.length ? process.argv[idx + 1] : null;
}

main().catch((e) => { console.error(JSON.stringify({ status: "error", message: e.message })); process.exit(1); });

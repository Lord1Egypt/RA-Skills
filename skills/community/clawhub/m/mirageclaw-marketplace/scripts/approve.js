#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: MARKETPLACE_API_KEY (passed to bid.js)
//   External endpoints called: {BASE}/upload/image, {BASE}/jobs/:jobId/bids
//   Local files read: ~/.openclaw/marketplace-config.json, /tmp/marketplace_pending.json
//   Local files written: /tmp/job_spec_*.json, /tmp/result_*, /tmp/protection_*, /tmp/price_* (auto-deleted)

'use strict';

require('./lib/env').loadEnv();

const fs   = require('fs');
const path = require('path');
const os   = require('os');
const { execFileSync } = require('child_process');

const { CONFIG_PATH, PENDING_PATH, MIME_MAP, markCompleted } = require('./lib/constants');
const { send, replace, del } = require('./lib/messaging');
const SKILL_DIR    = path.resolve(__dirname, '..');
const BASE_URL     = 'https://api.mirageclaw.io';

// ─── Base64 image encoding ───────────────────────────────────────────────
function fileToDataUri(filePath) {
  const buf = fs.readFileSync(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const mime = MIME_MAP[ext] || 'image/png';
  return `data:${mime};base64,${buf.toString('base64')}`;
}

async function main() {

const jobId = process.argv[2];
const quiet = process.argv.includes('--quiet'); // parallel mode: suppress intermediate progress messages
const fromDaemon = process.argv.includes('--from-daemon'); // spawned by listen.js (bid-intent already emitted)
if (!jobId) {
  console.error('Usage: approve.js <jobId>');
  process.exit(1);
}

// Manual mode (invoked by gateway on [Start] click): signal listen.js to emit bid-intent via file IPC
if (!fromDaemon) {
  try { fs.writeFileSync(`/tmp/bid_intent_req_${jobId}`, jobId); } catch (_) {}
}

const { notify } = require('./lib/notify');

// ─── Load + validate config ───────────────────────────────────────────────
let config;
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
} catch (err) {
  notify('MARKETPLACE_ERROR', { message: `Failed to read config: ${err.message}` });
  process.exit(1);
}

// ─── Load pending ─────────────────────────────────────────────────────────
let pending;
try {
  pending = JSON.parse(fs.readFileSync(PENDING_PATH, 'utf-8'));
} catch (err) {
  notify('MARKETPLACE_ERROR', { message: `Failed to read pending: ${err.message}` });
  process.exit(1);
}

const entry = pending[jobId];
if (!entry) {
  notify('MARKETPLACE_ERROR', { jobId, message: `❌ No pending job: ${jobId}` });
  process.exit(1);
}

const job        = entry.job;
const matchGroup = entry.matchGroup;
const noShowRate = entry.noShowRate ?? job.requesterNoShowRate ?? null;
const budget     = job.spec?.budget ?? 0;
const category   = job.spec?.style || job.spec?.purpose || 'unknown';
const desc       = job.spec?.description || '';

// Resolve capability for this job
const jobType = (job.spec?.type) || 'photo';
let capability;
if (jobType === 'video') {
  capability = config.capabilities?.video;
  if (!capability) {
    notify('MARKETPLACE_ERROR', {
      jobId,
      message: `❌ No video capability configured. Set capabilities.video in config to accept video jobs.`
    });
    process.exit(1);
  }
} else {
  capability = config.capabilities?.[matchGroup] || config.capabilities?.default;
}

if (!capability) {
  notify('MARKETPLACE_ERROR', {
    jobId,
    message: `❌ No capability configured for group "${matchGroup}" and no default set.`
  });
  process.exit(1);
}

const specPath   = `/tmp/job_spec_${jobId}.json`;
const resultBase = `/tmp/result_${jobId}`;

notify('MARKETPLACE_PROCESS_START', {
  jobId, category, budget, matchGroup,
  capability: typeof capability === 'string' ? capability : capability.api,
  message: `⚙️ Starting — Job #${jobId} (${category} / ${budget}) via ${typeof capability === 'string' ? capability : capability.api}`
});

const protectionPath = `/tmp/protection_${jobId}.txt`;
const pricePath      = `/tmp/price_${jobId}.txt`;

// Replace-in-place progress message ID (delete old + send new)
let progressMsgId = null;
let previewMsgId = null;   // preview image at step 4.5 — deleted after bid submission
const chatId = config.telegramChatId;

// Delete the job offer message (the one with [Start]/[Skip] buttons) immediately
if (entry.offerMsgId && chatId) {
  try { del(chatId, entry.offerMsgId); } catch (_) {}
  // Clear offerMsgId from pending so the 1-min auto-cancel timer knows bid is in progress
  try {
    const pClear = JSON.parse(fs.readFileSync(PENDING_PATH, 'utf-8'));
    if (pClear[jobId]) {
      delete pClear[jobId].offerMsgId;
      const tmpClear = PENDING_PATH + '.tmp';
      fs.writeFileSync(tmpClear, JSON.stringify(pClear, null, 2));
      fs.renameSync(tmpClear, PENDING_PATH);
    }
  } catch (_) {}
}

function cleanup() {
  if (fs.existsSync(specPath)) fs.unlinkSync(specPath);
  if (fs.existsSync(protectionPath)) fs.unlinkSync(protectionPath);
  if (fs.existsSync(pricePath)) fs.unlinkSync(pricePath);
  fs.readdirSync('/tmp')
    .filter(f => f.startsWith(`result_${jobId}`))
    .forEach(f => fs.unlinkSync(`/tmp/${f}`));
}

try {
  // ── Step 1: Write job spec ───────────────────────────────────────────
  process.stderr.write(`[PROCESS_STEP] ⚙️ [1/5] Preparing job spec...\n`);

  if (chatId && !quiet) {
    try {
      progressMsgId = replace(chatId, null, `⚙️ [1/5] Preparing job spec...\nJob #${jobId} · ${category} · ${budget}cr`);
    } catch (_) { /* non-blocking */ }
  }

  const jobSpec = {
    jobId,
    title:         job.spec?.title       || '',
    category,
    type:          jobType,
    style:         job.spec?.style       || '',
    mood:          job.spec?.mood        || '',
    color:         job.spec?.color       || '',
    description:   desc,
    ratio:         job.spec?.ratio       || '',
    budget,
    referenceUrls: job.spec?.referenceUrls || [],
    matchGroup,
    capability: typeof capability === 'string'
      ? { type: 'script', value: capability }
      : capability
  };
  fs.writeFileSync(specPath, JSON.stringify(jobSpec, null, 2));

  // ── Step 2: Execute ──────────────────────────────────────────────────
  const execLabel = jobSpec.capability.type === 'script' ? 'script' : jobSpec.capability.api;
  process.stderr.write(`[PROCESS_STEP] ⚙️ [2/5] Executing job via ${execLabel}...\n`);

  if (chatId && (progressMsgId || quiet)) {
    try {
      const progressMsg = quiet
        ? `⚙️ Job #${jobId} accepted — generating ${jobType === 'video' ? 'video' : 'image'}. Will notify you when done.\n${category} · ${budget}cr`
        : `⚙️ [2/5] Generating ${jobType === 'video' ? 'video' : 'image'} via ${execLabel}...\nJob #${jobId} · ${category} · ${budget}cr`;
      progressMsgId = replace(chatId, progressMsgId, progressMsg);
    } catch (_) { /* non-blocking */ }
  }

  // Resolve executor:
  // capability can be:
  //   string → local script path
  //   { api, envKey } → direct API call via provider-engine
  if (typeof capability === 'string') {
    // Local script executor
    // Contract: script <outputPath> <specPath>
    //   $1 = output file path (with extension, e.g. /tmp/result_xxx.png or .mp4)
    //   $2 = job spec JSON path (for reading job details)
    const executorPath = capability.replace(/^~/, os.homedir());

    if (!fs.existsSync(executorPath)) {
      notify('MARKETPLACE_ERROR', { jobId, message: `❌ Executor not found: ${executorPath}` });
      cleanup();
      process.exit(1);
    }

    const defaultExt = jobType === 'video' ? '.mp4' : '.png';
    const resultPath = resultBase + defaultExt;

    const { spawnSync } = require('child_process');
    const result = spawnSync(executorPath, [resultPath, specPath], {
      encoding: 'utf-8',
      timeout: 15 * 60 * 1000
    });

    if (result.error || result.status !== 0) {
      notify('MARKETPLACE_ERROR', {
        jobId,
        message: `❌ Executor failed (exit ${result.status}): ${(result.stderr || result.error?.message || '').slice(0, 200)}`
      });
      cleanup();
      process.exit(1);
    }

  } else {
    // Direct API call via provider registry — no LLM dependency
    const { callProvider } = require('./provider-engine');

    process.stderr.write(`[PROCESS_STEP] [2/5] Calling ${capability.api} API directly...\n`);

    await callProvider(capability, specPath, resultBase);
  }

  // ── Verify result file exists ────────────────────────────────────────
  const resultFile = fs.readdirSync('/tmp').find(f => f.startsWith(`result_${jobId}`));
  if (!resultFile) {
    notify('MARKETPLACE_ERROR', {
      jobId,
      message: `❌ No result file found at /tmp/result_${jobId}* — execution may have failed`
    });
    cleanup();
    process.exit(1);
  }

  let resultFullPath = `/tmp/${resultFile}`;
  process.stderr.write(`[PROCESS_STEP] ✅ [2/5] Result ready — ${resultFile}\n`);

  // ── Video re-encode for server compatibility ──────────────────────────
  // LTX-Video (and some other generators) produce mp4 with non-standard codecs
  // that the server's ffmpeg cannot process for watermarking. Re-encode to
  // H.264/AAC before upload to ensure compatibility.
  const resultExt = path.extname(resultFullPath).toLowerCase();
  if (jobType === 'video') {
    const outExt = resultExt || '.mp4';
    const compatPath = resultFullPath.replace(/(\.[^.]+)?$/, `_compat${outExt}`);
    process.stderr.write(`[PROCESS_STEP] 🎬 Re-encoding video for server compatibility...\n`);
    try {
      execFileSync('ffmpeg', [
        '-i', resultFullPath,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-movflags', '+faststart',
        '-y',
        compatPath
      ], { timeout: 5 * 60 * 1000 });
      // Replace original with re-encoded version
      fs.unlinkSync(resultFullPath);
      // Ensure final file has correct video extension (fix .png misdetection)
      const finalPath = resultFullPath.replace(/(\.[^.]+)?$/, outExt);
      fs.renameSync(compatPath, finalPath);
      resultFullPath = finalPath;
      process.stderr.write(`[PROCESS_STEP] ✅ Video re-encoded successfully — ${path.basename(finalPath)}\n`);
    } catch (err) {
      process.stderr.write(`[PROCESS_STEP] ⚠️ Video re-encode failed: ${err.message} — uploading original\n`);
      // Clean up partial file if exists
      try { if (fs.existsSync(compatPath)) fs.unlinkSync(compatPath); } catch (_) {}
    }
  }

  // ── Image ready — signal OpenClaw to send image to Telegram ──────────
  const imageData = fileToDataUri(resultFullPath);

  notify('MARKETPLACE_IMAGE_READY', {
    jobId,
    resultPath: resultFullPath,
    imageData,
    message: `🖼️ Image ready — Job #${jobId} · ${resultFile}`
  });

  // ── Step 3: Watermark protection level selection (Telegram) ──────────
  let protection = 'medium';

  if (config.presetMode === true) {
    // Preset mode — skip Telegram prompt
    protection = config.presetProtection || 'medium';
    process.stderr.write(`[PROCESS_STEP] 🔒 [3/5] Preset protection: ${protection}\n`);

    if (chatId && progressMsgId && !quiet) {
      try {
        progressMsgId = replace(chatId, progressMsgId, `🔒 [3/5] Protection: ${protection} (preset)\nJob #${jobId} · ${category} · ${budget}cr`);
      } catch (_) { /* non-blocking */ }
    }
  } else {
    process.stderr.write(`[PROCESS_STEP] 🔒 [3/5] Waiting for protection level selection...\n`);
  }

  if (config.presetMode !== true && chatId) {
    const protectionMessage = [
      `🖼️ Image ready — Job #${jobId}`,
      ``,
      `Select watermark protection level for the preview:`,
      ``,
      `  🔓 Low    — Noise 8.6%  | Opacity 45% | Mosaic 28px | Res 75%`,
      `              Best preview quality, less protected`,
      `  🔒 Medium — Noise 16.5% | Opacity 65% | Mosaic 18px | Res 60%  (recommended)`,
      `  🔐 High   — Noise 24.3% | Opacity 82% | Mosaic 12px | Res 50%`,
      `              Strongest protection, lower preview quality`
    ].join('\n');

    const protectionButtons = [[
      { text: '🔓 Low (75% res)',    callback_data: `protection ${jobId} low` },
      { text: '🔒 Medium (60% res)', callback_data: `protection ${jobId} medium` },
      { text: '🔐 High (50% res)',   callback_data: `protection ${jobId} high` }
    ]];

    try {
      // Replace the progress message with protection buttons
      progressMsgId = replace(chatId, progressMsgId, protectionMessage, { buttons: protectionButtons });

      notify('MARKETPLACE_PROTECTION_PROMPT', {
        jobId,
        message: `🔒 [3/5] Protection level prompt sent — waiting for Telegram response...`
      });
    } catch (err) {
      notify('MARKETPLACE_ERROR', {
        jobId,
        message: `⚠️ Telegram protection prompt failed: ${err.message} — using default (medium)`
      });
    }

    // Poll for user's protection level choice (up to 5 minutes)
    const protectionDeadline = Date.now() + 5 * 60 * 1000;
    while (Date.now() < protectionDeadline) {
      if (fs.existsSync(protectionPath)) break;
      await new Promise(r => setTimeout(r, 2000));
    }

    if (fs.existsSync(protectionPath)) {
      protection = fs.readFileSync(protectionPath, 'utf-8').trim();
      fs.unlinkSync(protectionPath);
    }
  }

  notify('MARKETPLACE_PROTECTION_SELECTED', {
    jobId, protection,
    message: `🔒 [3/5] Protection level: ${protection}`
  });

  // ── Step 4: Bid price selection (Telegram) ────────────────────────────
  const MIN_BID = 10; // API minimum: 10 credits = $0.10
  let bidPrice = budget;

  if (config.presetMode === true) {
    // Preset mode — skip Telegram prompt
    const pct = config.presetPricePercent ?? 100;
    bidPrice = Math.max(MIN_BID, Math.round(budget * pct / 100));
    process.stderr.write(`[PROCESS_STEP] 💰 [4/5] Preset price: ${bidPrice} credits (${pct}% of ${budget})\n`);

    if (chatId && progressMsgId && !quiet) {
      try {
        progressMsgId = replace(chatId, progressMsgId, `💰 [4/5] Bid price: ${bidPrice}cr (${pct}% preset)\nJob #${jobId} · ${category} · ${budget}cr`);
      } catch (_) { /* non-blocking */ }
    }
  } else {
    process.stderr.write(`[PROCESS_STEP] 💰 [4/5] Waiting for bid price selection...\n`);
  }

  if (config.presetMode !== true && chatId) {
    // Clamp preset options to API minimum (10 credits)
    const price50  = Math.max(MIN_BID, Math.round(budget * 0.50));
    const price75  = Math.max(MIN_BID, Math.round(budget * 0.75));
    const price100 = budget;

    const fmt = (cr) => `${cr} credits ($${(cr / 100).toFixed(2)})`;
    const budgetUsd = (budget / 100).toFixed(2);

    const priceMessage = [
      `💰 Select your bid price for Job #${jobId}`,
      ``,
      `  Budget : ${budget} credits ($${budgetUsd})`,
      ``,
      `  50%  — ${fmt(price50)} — competitive`,
      `  75%  — ${fmt(price75)} — fair`,
      `  100% — ${fmt(price100)} — full budget`,
      `  ✏️ Custom — enter your own amount (min ${MIN_BID} credits / $${(MIN_BID/100).toFixed(2)})`
    ].join('\n');

    const priceButtons = [[
      { text: `💰 ${price50}cr ($${(price50/100).toFixed(2)}) 50%`,  callback_data: `price ${jobId} ${price50}` },
      { text: `💰 ${price75}cr ($${(price75/100).toFixed(2)}) 75%`,  callback_data: `price ${jobId} ${price75}` }
    ], [
      { text: `💰 ${price100}cr ($${(price100/100).toFixed(2)}) 100%`, callback_data: `price ${jobId} ${price100}` },
      { text: `✏️ Custom`, callback_data: `price-custom ${jobId}` }
    ]];

    try {
      // Replace the progress message with price buttons
      progressMsgId = replace(chatId, progressMsgId, priceMessage, { buttons: priceButtons });

      notify('MARKETPLACE_PRICE_PROMPT', {
        jobId, budget,
        message: `💰 [4/5] Bid price prompt sent — waiting for Telegram response...`
      });
    } catch (err) {
      notify('MARKETPLACE_ERROR', {
        jobId,
        message: `⚠️ Telegram price prompt failed: ${err.message} — using full budget (${budget} credits)`
      });
    }

    // Poll for user's price choice (up to 5 minutes)
    const priceDeadline = Date.now() + 5 * 60 * 1000;
    while (Date.now() < priceDeadline) {
      if (fs.existsSync(pricePath)) break;
      await new Promise(r => setTimeout(r, 2000));
    }

    if (fs.existsSync(pricePath)) {
      const raw = parseInt(fs.readFileSync(pricePath, 'utf-8').trim(), 10);
      // Validate: must be integer, at least MIN_BID, and within budget
      if (Number.isInteger(raw) && raw >= MIN_BID && raw <= budget) {
        bidPrice = raw;
      }
      fs.unlinkSync(pricePath);
    }
  }

  notify('MARKETPLACE_PRICE_SELECTED', {
    jobId, price: bidPrice, budget,
    message: `💰 [4/5] Bid price: ${bidPrice} credits ($${(bidPrice/100).toFixed(2)}) — ${budget > 0 ? Math.round(bidPrice / budget * 100) : 0}% of budget`
  });

  // ── Step 4.5: Final confirmation before submission ─────────────────────
  const confirmPath = `/tmp/confirm_${jobId}.txt`;

  if (chatId) {
    // Send preview image + warning + Submit/Cancel buttons
    const confirmMessage = [
      `⚠️ Final Review — Job #${jobId}`,
      ``,
      `  Price      : ${bidPrice} credits ($${(bidPrice/100).toFixed(2)})`,
      `  Protection : ${protection}`,
      ``,
      `⚠️ WARNING:`,
      `Submitting adult content, illegal material, or content that`,
      `violates third-party rights (copyright, portrait rights,`,
      `trademarks) may result in account suspension and legal liability.`,
      `ALL legal responsibility for generated content lies with the`,
      `agent owner.`,
      ``,
      `Proceed with bid submission?`
    ].join('\n');

    const confirmButtons = [[
      { text: '✅ Submit Bid', callback_data: `confirm ${jobId} submit` },
      { text: '❌ Cancel', callback_data: `confirm ${jobId} cancel` }
    ]];

    try {
      // Send preview image first (save msgId for cleanup after bid submission)
      if (resultFullPath) {
        const workspaceDir = path.join(os.homedir(), '.openclaw/workspace');
        if (!fs.existsSync(workspaceDir)) fs.mkdirSync(workspaceDir, { recursive: true });
        const previewCopy = path.join(workspaceDir, `preview_${jobId}${path.extname(resultFullPath) || '.png'}`);
        fs.copyFileSync(resultFullPath, previewCopy);
        try { previewMsgId = send(chatId, `🖼️ Preview — Job #${jobId}`, { media: previewCopy }); } catch (_) {}
        try { fs.unlinkSync(previewCopy); } catch (_) {}
      }
      // Then send confirmation with buttons
      progressMsgId = replace(chatId, progressMsgId, confirmMessage, { buttons: confirmButtons });
    } catch (_) { /* non-blocking */ }

    // Poll for confirmation (up to 5 minutes)
    const confirmDeadline = Date.now() + 5 * 60 * 1000;
    while (Date.now() < confirmDeadline) {
      if (fs.existsSync(confirmPath)) break;
      await new Promise(r => setTimeout(r, 2000));
    }

    let confirmed = true; // default: submit if timeout
    if (fs.existsSync(confirmPath)) {
      const decision = fs.readFileSync(confirmPath, 'utf-8').trim().toLowerCase();
      fs.unlinkSync(confirmPath);
      if (decision === 'cancel') {
        confirmed = false;
      }
    }

    if (!confirmed) {
      // User cancelled — clean up and exit
      notify('MARKETPLACE_BID_CANCELLED', {
        jobId,
        message: `❌ Bid cancelled by user — Job #${jobId}`
      });
      if (progressMsgId) {
        try { del(chatId, progressMsgId); } catch (_) {}
      }
      try { send(chatId, `❌ Bid cancelled — Job #${jobId}`); } catch (_) {}
      cleanup();
      const freshPending = JSON.parse(fs.readFileSync(PENDING_PATH, 'utf-8'));
      delete freshPending[jobId];
      const tmp2 = PENDING_PATH + '.tmp';
      fs.writeFileSync(tmp2, JSON.stringify(freshPending, null, 2));
      fs.renameSync(tmp2, PENDING_PATH);
      process.exit(0);
    }
  }

  // ── Step 5: Upload + Bid ─────────────────────────────────────────────
  process.stderr.write(`[PROCESS_STEP] 📤 [5/5] Uploading (protection=${protection}) and submitting bid @ ${bidPrice} credits ($${(bidPrice/100).toFixed(2)})...\n`);

  if (chatId && progressMsgId && !quiet) {
    try {
      progressMsgId = replace(chatId, progressMsgId, `📤 [5/5] Uploading & submitting bid...\nJob #${jobId} · ${bidPrice}cr · ${protection} protection`);
    } catch (_) { /* non-blocking */ }
  }

  // Build bid introduction from config
  const agentPitch = config.introduction || `I specialize in ${Object.keys(config.capabilities).filter(k => k !== 'default').join(', ')}.`;
  const introduction = `${agentPitch} Created to match your requirements.`;

  execFileSync('node', [
    `${SKILL_DIR}/scripts/bid.js`,
    '--job-id', jobId,
    '--preview', resultFullPath,
    '--price', String(bidPrice),
    '--introduction', introduction,
    '--protection', protection,
    '--preview-type', jobType === 'video' ? 'video' : 'image'
  ]);

  // ── Telegram: send result image + completion text (BEFORE cleanup) ───
  const title = job.spec?.title || 'Untitled';
  const budgetUsd = (budget / 100).toFixed(2);
  const bidUsd = (bidPrice / 100).toFixed(2);
  const pct = budget > 0 ? Math.round(bidPrice / budget * 100) : 0;
  const caption = [
    `✅ Bid submitted — ${title}`,
    `${category} · ${bidPrice}cr ($${bidUsd}) · ${protection} protection`
  ].join('\n');

  // Emit image event so OpenClaw sends the actual image file to Telegram.
  // resultFullPath still exists here — cleanup() has NOT run yet.
  notify('MARKETPLACE_BID_IMAGE', {
    jobId,
    resultPath: resultFullPath,
    imageData,
    caption,
    message: `🖼️ Bid result image — Job #${jobId} · ${resultFullPath}`
  });

  // Send result image + caption via openclaw CLI (--media flag)
  if (chatId) {
    // Delete the progress message and preview image — final result replaces both
    if (progressMsgId) {
      try { del(chatId, progressMsgId); } catch (_) { /* non-blocking */ }
    }
    if (previewMsgId) {
      try { del(chatId, previewMsgId); } catch (_) { /* non-blocking */ }
    }

    const { fmtNoShow } = require('./lib/format');
    const photoCaption = [
      `✅ Bid submitted — ${title}`,
      ``,
      `  Category   : ${category}`,
      `  Budget     : ${budget} credits ($${budgetUsd})`,
      `  Bid Price  : ${bidPrice} credits ($${bidUsd}) — ${pct}%`,
      `  Protection : ${protection}`,
      `  No-Show    : ${fmtNoShow(noShowRate)}`,
      ``,
      `Waiting for requester's decision...`
    ].join('\n');

    // Copy image to workspace — /tmp is blocked by openclaw message send
    const workspaceDir = path.join(os.homedir(), '.openclaw/workspace');
    if (!fs.existsSync(workspaceDir)) fs.mkdirSync(workspaceDir, { recursive: true });
    const workspaceCopy = path.join(workspaceDir,
      `bid_result_${jobId}${path.extname(resultFullPath) || '.png'}`);
    fs.copyFileSync(resultFullPath, workspaceCopy);

    try {
      send(chatId, photoCaption, { media: workspaceCopy, timeout: 15000 });
    } catch (mediaErr) {
      // Fallback: text-only notification if image send fails
      process.stderr.write(`[MEDIA_FALLBACK] Image send failed: ${mediaErr.message}\n`);
      try {
        send(chatId, photoCaption);
      } catch (_) { /* non-blocking */ }
    } finally {
      // Clean up workspace copy
      try { fs.unlinkSync(workspaceCopy); } catch (_) {}
    }
  }

  // Now safe to clean up temp files
  cleanup();

  // Save bid info for bid-selected notification (listen.js reads this later)
  const bidInfoPath = `/tmp/bid_info_${jobId}.json`;
  fs.writeFileSync(bidInfoPath, JSON.stringify({
    title: job.spec?.title || 'Untitled',
    category,
    price: bidPrice,
    previewType: jobType === 'video' ? 'video' : 'image'
  }));

  const freshPending = JSON.parse(fs.readFileSync(PENDING_PATH, 'utf-8'));
  delete freshPending[jobId];
  const tmp = PENDING_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(freshPending, null, 2));
  fs.renameSync(tmp, PENDING_PATH);

  // Mark job as completed for dedup — prevents reprocessing on catchUp/reconnect
  markCompleted(jobId);

  notify('MARKETPLACE_BID_DONE', {
    jobId, category, price: bidPrice,
    message: `🎉 Bid submitted! Job #${jobId} (${category}) @ ${bidPrice} credits ($${(bidPrice/100).toFixed(2)})`
  });

} catch (err) {
  cleanup();
  notify('MARKETPLACE_ERROR', { jobId, message: `❌ Error: ${err.message}` });
  process.exit(1);
}

} // end main

main().catch(err => {
  process.stderr.write(`[FATAL] ${err.message}\n`);
  process.exit(1);
});

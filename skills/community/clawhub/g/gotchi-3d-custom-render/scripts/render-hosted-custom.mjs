#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { loadRenderRequest } from "./load-render-request.mjs";

const DAPP_BASE = "https://www.aavegotchi.com";
const BATCH_ENDPOINT = `${DAPP_BASE}/api/renderer/batch`;
const RENDER_TYPES = ["PNG_Full", "PNG_Headshot", "GLB_3DModel"];
let GLOBAL_QUIET_FAIL = false;

function parseArgs(argv) {
  const args = {
    inputJson: null,
    quietFail: false
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = argv[i + 1];
    if (arg === "--input-json" && next) {
      args.inputJson = next;
      i += 1;
      continue;
    }
    if (arg === "--quiet-fail") {
      args.quietFail = true;
      continue;
    }
    if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    }
  }

  return args;
}

function printHelp() {
  console.log(`Usage:
  node scripts/render-hosted-custom.mjs --input-json <request.json> [--quiet-fail]
`);
}

function normalizeKey(raw) {
  return String(raw || "")
    .replace(/[_\-\s]/g, "")
    .toUpperCase();
}

function mapCollateral(raw) {
  const key = normalizeKey(raw);
  switch (key) {
    case "ETH": return "Eth";
    case "AAVE": return "Aave";
    case "DAI": return "Dai";
    case "LINK": return "Link";
    case "USDT": return "USDT";
    case "USDC": return "USDC";
    case "TUSD": return "TUSD";
    case "UNI": return "Uni";
    case "YFI": return "Yfi";
    case "POLYGON": return "Polygon";
    case "WETH": return "wEth";
    case "WBTC": return "wBTC";
    default: return "Eth";
  }
}

const EXACT_EYE_SHAPES = new Set([
  "ETH", "AAVE", "DAI", "LINK", "USDT", "USDC", "TUSD", "UNI", "YFI", "POLYGON", "wETH", "wBTC",
  "Common1", "Common2", "Common3",
  "UncommonLow1", "UncommonLow2", "UncommonLow3",
  "UncommonHigh1", "UncommonHigh2", "UncommonHigh3",
  "RareLow1", "RareLow2", "RareLow3",
  "RareHigh1", "RareHigh2", "RareHigh3",
  "MythicalLow1_H1", "MythicalLow2_H1", "MythicalLow1_H2", "MythicalLow2_H2"
]);

function parseEyeShape(raw) {
  const value = String(raw || "").trim();
  if (EXACT_EYE_SHAPES.has(value)) return value;
  switch (normalizeKey(value)) {
    case "ETH": return "ETH";
    case "AAVE": return "AAVE";
    case "DAI": return "DAI";
    case "LINK": return "LINK";
    case "USDT": return "USDT";
    case "USDC": return "USDC";
    case "TUSD": return "TUSD";
    case "UNI": return "UNI";
    case "YFI": return "YFI";
    case "POLYGON": return "POLYGON";
    case "WETH": return "wETH";
    case "WBTC": return "wBTC";
    case "COMMON": return "Common1";
    case "UNCOMMONLOW": return "UncommonLow1";
    case "UNCOMMONHIGH": return "UncommonHigh1";
    case "RARELOW": return "RareLow1";
    case "RAREHIGH": return "RareHigh1";
    case "MYTHICAL":
    case "MYTHICALLOW":
    case "MYTHICALHIGH":
      return "MythicalLow1_H1";
    default:
      return "Common1";
  }
}

const EXACT_EYE_COLORS = new Set([
  "Common",
  "Uncommon_Low", "Uncommon_High",
  "Rare_Low", "Rare_High",
  "Mythical_Low", "Mythical_High"
]);

function defaultEyeColorForShape(shape) {
  if (shape.startsWith("Mythical")) return "Mythical_High";
  if (shape.startsWith("RareHigh")) return "Rare_High";
  if (shape.startsWith("RareLow")) return "Rare_Low";
  if (shape.startsWith("UncommonHigh")) return "Uncommon_High";
  if (shape.startsWith("UncommonLow")) return "Uncommon_Low";
  return "Common";
}

function parseEyeColor(raw, shape) {
  const value = String(raw || "").trim();
  if (EXACT_EYE_COLORS.has(value)) return value;
  switch (normalizeKey(value)) {
    case "COMMON": return "Common";
    case "UNCOMMONLOW": return "Uncommon_Low";
    case "UNCOMMONHIGH": return "Uncommon_High";
    case "RARELOW": return "Rare_Low";
    case "RAREHIGH": return "Rare_High";
    case "MYTHICALLOW": return "Mythical_Low";
    case "MYTHICALHIGH": return "Mythical_High";
    case "LOW":
      return shape.startsWith("Mythical")
        ? "Mythical_Low"
        : shape.startsWith("Rare")
          ? "Rare_Low"
          : shape.startsWith("Uncommon")
            ? "Uncommon_Low"
            : "Common";
    case "HIGH":
      return shape.startsWith("Mythical")
        ? "Mythical_High"
        : shape.startsWith("Rare")
          ? "Rare_High"
          : shape.startsWith("Uncommon")
            ? "Uncommon_High"
            : "Common";
    default:
      return defaultEyeColorForShape(shape);
  }
}

function deriveHash(request) {
  const collateral = mapCollateral(request.collateral);
  const eyeShape = parseEyeShape(request.eye_shape);
  const eyeColor = parseEyeColor(request.eye_color, eyeShape);
  const wearables = request.wearables || {};
  const body = Number(wearables.body || 0);
  const face = Number(wearables.face || 0);
  const eyes = Number(wearables.eyes || 0);
  const head = Number(wearables.head || 0);
  const rightHand = Number(wearables.hand_right || 0);
  const leftHand = Number(wearables.hand_left || 0);
  const pet = Number(wearables.pet || 0);
  return [collateral, eyeShape, eyeColor, body, face, eyes, head, rightHand, leftHand, pet].join("-");
}

async function postJson(url, body, maxAttempts = 4) {
  let lastError = null;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      const text = await response.text();
      let json = null;
      try {
        json = text ? JSON.parse(text) : null;
      } catch {
        json = null;
      }
      return { response, text, json };
    } catch (error) {
      lastError = error;
      if (attempt < maxAttempts) {
        await sleep(1200 * attempt);
        continue;
      }
    }
  }

  throw lastError;
}

function isRetryableStatus(status) {
  return [403, 404, 408, 409, 423, 425, 429, 500, 502, 503, 504].includes(Number(status));
}

async function downloadFile(url, filePath, maxAttempts = 6) {
  let lastStatus = null;
  let lastBody = "";
  let lastError = null;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    let response;
    try {
      response = await fetch(url);
    } catch (error) {
      lastError = error;
      if (attempt < maxAttempts) {
        await sleep(1200 * attempt);
        continue;
      }
      break;
    }

    if (response.ok) {
      const bytes = Buffer.from(await response.arrayBuffer());
      fs.writeFileSync(filePath, bytes);
      return filePath;
    }

    lastStatus = response.status;
    lastBody = "";
    if (attempt < maxAttempts && isRetryableStatus(response.status)) {
      await sleep(1200 * attempt);
      continue;
    }

    try {
      lastBody = (await response.text()).slice(0, 300);
    } catch {
      lastBody = "";
    }
    break;
  }

  if (lastError && lastStatus === null) {
    throw new Error(`Failed to download ${url}: ${lastError.message || String(lastError)}`);
  }

  const detail = lastBody ? `: ${lastBody}` : "";
  throw new Error(`Failed to download ${url} (${lastStatus ?? "unknown"})${detail}`);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function ensureParent(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function withTempSuffix(filePath, suffix) {
  const parsed = path.parse(filePath);
  return path.join(parsed.dir, `${parsed.name}${suffix}${parsed.ext}`);
}

async function applyBackground(inputPath, outputPath, hexColor) {
  const { applySolidBackground } = await import("./add-bg-color.mjs");
  applySolidBackground(inputPath, outputPath, hexColor);
}

function emitAndExit(obj, code = 0, quiet = false) {
  const text = JSON.stringify(obj, null, 2);
  if (!quiet || code === 0) {
    console.log(text);
  }
  process.exit(code);
}

function getAvailability(result, type) {
  return result?.availability?.[type] || null;
}

function assetsReady(result) {
  const full = getAvailability(result, "PNG_Full");
  const headshot = getAvailability(result, "PNG_Headshot");
  return Boolean(
    result?.proxyUrls?.PNG_Full &&
    result?.proxyUrls?.PNG_Headshot &&
    full?.exists &&
    headshot?.exists
  );
}

async function requestBatch(hash, force = false) {
  const batch = await postJson(BATCH_ENDPOINT, {
    hashes: [hash],
    renderTypes: RENDER_TYPES,
    verify: true,
    force
  });
  return {
    batch,
    result: batch?.json?.data?.results?.[0] || null,
    force
  };
}

async function resolveBatch(hash) {
  let last = await requestBatch(hash, false);
  if (!last.batch?.response?.ok || assetsReady(last.result)) {
    return { ...last, attempts: 1, forced: false };
  }

  last = await requestBatch(hash, true);
  if (!last.batch?.response?.ok || assetsReady(last.result)) {
    return { ...last, attempts: 2, forced: true };
  }

  for (let attempt = 1; attempt <= 12; attempt += 1) {
    await sleep(2500);
    last = await requestBatch(hash, false);
    if (!last.batch?.response?.ok || assetsReady(last.result)) {
      return { ...last, attempts: attempt + 2, forced: true };
    }
  }

  return { ...last, attempts: 14, forced: true };
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  GLOBAL_QUIET_FAIL = options.quietFail;
  if (!options.inputJson) {
    printHelp();
    throw new Error("Provide --input-json <request.json>.");
  }

  const request = loadRenderRequest(options.inputJson);
  const manifestPath = request?.output?.manifest_json;
  const fullOutput = request?.output?.full_png;
  const headshotOutput = request?.output?.headshot_png;
  if (!manifestPath || !fullOutput || !headshotOutput) {
    emitAndExit({
      ok: false,
      status: "bad_request",
      message: "Request JSON is missing output paths."
    }, 1, options.quietFail);
  }

  if (Number(request.skin_id || 0) > 0) {
    emitAndExit({
      ok: false,
      status: "hosted_unsupported_skin",
      message: "Hosted renderer path does not support custom skin_id reliably yet.",
      request
    }, 1, options.quietFail);
  }

  ensureParent(manifestPath);
  ensureParent(fullOutput);
  ensureParent(headshotOutput);

  const hash = deriveHash(request);
  const { batch, result, attempts, forced } = await resolveBatch(hash);

  if (!batch?.response?.ok) {
    emitAndExit({
      ok: false,
      status: "hosted_batch_failed",
      message: `Hosted renderer batch failed (${batch?.response?.status ?? "unknown"}).`,
      hash,
      request,
      response_text: batch?.text?.slice(0, 500)
    }, 1, options.quietFail);
  }

  const proxyUrls = result?.proxyUrls || {};
  if (!assetsReady(result)) {
    emitAndExit({
      ok: false,
      status: "hosted_assets_unavailable",
      message: "Hosted renderer did not make the PNG assets available for this hash before timeout.",
      hash,
      forced,
      attempts,
      request,
      batch: batch.json,
      availability: {
        full: getAvailability(result, "PNG_Full"),
        headshot: getAvailability(result, "PNG_Headshot"),
        glb: getAvailability(result, "GLB_3DModel")
      }
    }, 1, options.quietFail);
  }

  const fullUrl = proxyUrls.PNG_Full.startsWith("http") ? proxyUrls.PNG_Full : `${DAPP_BASE}${proxyUrls.PNG_Full}`;
  const headshotUrl = proxyUrls.PNG_Headshot.startsWith("http") ? proxyUrls.PNG_Headshot : `${DAPP_BASE}${proxyUrls.PNG_Headshot}`;
  const glbUrl = proxyUrls.GLB_3DModel
    ? (proxyUrls.GLB_3DModel.startsWith("http") ? proxyUrls.GLB_3DModel : `${DAPP_BASE}${proxyUrls.GLB_3DModel}`)
    : null;

  let finalFull = fullOutput;
  let finalHeadshot = headshotOutput;
  let transparentFull = null;
  let transparentHeadshot = null;
  const warnings = [];

  if (String(request.pose || "idle").toLowerCase() !== "idle") {
    warnings.push("Hosted renderer uses its own fixed pose and ignored the requested pose.");
  }

  const background = String(request.background || "transparent");
  const needsBg = background && background.toLowerCase() !== "transparent";

  if (needsBg) {
    transparentFull = withTempSuffix(fullOutput, "-transparent");
    transparentHeadshot = withTempSuffix(headshotOutput, "-transparent");
    await downloadFile(fullUrl, transparentFull);
    await downloadFile(headshotUrl, transparentHeadshot);

    try {
      applyBackground(transparentFull, fullOutput, background);
      applyBackground(transparentHeadshot, headshotOutput, background);
    } catch (error) {
      warnings.push(`Background compositing failed; leaving transparent PNGs only. ${error.message}`);
      finalFull = transparentFull;
      finalHeadshot = transparentHeadshot;
    }
  } else {
    await downloadFile(fullUrl, fullOutput);
    await downloadFile(headshotUrl, headshotOutput);
  }

  const summary = {
    ok: true,
    status: warnings.length ? "rendered_with_warnings" : "rendered",
    message: "Hosted Aavegotchi renderer produced the final PNG artifacts.",
    render_mode: "hosted",
    hash,
    forced,
    attempts,
    full_png: finalFull,
    headshot_png: finalHeadshot,
    manifest_json: manifestPath,
    request,
    warnings,
    artifacts: {
      transparent_full_png: transparentFull,
      transparent_headshot_png: transparentHeadshot,
      glb_url: glbUrl,
      batch_status: batch.response.status
    }
  };

  fs.writeFileSync(manifestPath, `${JSON.stringify(summary, null, 2)}\n`);
  emitAndExit(summary, 0, false);
}

main().catch((error) => {
  emitAndExit({
    ok: false,
    status: "hosted_exception",
    message: error?.message || String(error)
  }, 1, GLOBAL_QUIET_FAIL);
});

#!/usr/bin/env node
/**
 * init-model.mjs — Download and verify the OpenClaw local embedding GGUF model.
 *
 * This script is part of the openclaw-local-embedding skill. It handles:
 *  1. Auto-detecting the OpenClaw installation directory
 *  2. Checking if the model is already cached (idempotent)
 *  3. Probing network connectivity with progressive proxy fallback
 *  4. Downloading the model via node-llama-cpp's resolveModelFile
 *  5. Verifying the model can be loaded
 *
 * Proxy handling:
 *  - First checks if HTTPS can reach HuggingFace without extra config
 *  - If not, tries the built-in Kuaishou proxy (http://10.74.176.8:11080)
 *  - Proxy env vars are process-scoped and do not affect other processes
 *
 * Usage:
 *  node init-model.mjs [--proxy <url>] [--openclaw-dir <path>]
 *
 * Environment:
 *  - Node.js >= 22
 *  - cmake >= 3.19 (for source compilation on GLIBC < 2.32)
 */

import { createRequire } from "node:module";
import path from "node:path";
import os from "node:os";
import fs from "node:fs";
import net from "node:net";
import tls from "node:tls";
import { execSync } from "node:child_process";

// ─── Constants ───────────────────────────────────────────────────────────────
const MODEL_ID =
  "hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf";
const MODEL_CACHE_FILE = "hf_ggml-org_embeddinggemma-300m-qat-Q8_0.gguf";
// Default proxy for Kuaishou cloud VMs. Tried automatically when direct access fails.
const KUAISHOU_DEFAULT_PROXY = "http://10.74.176.8:11080";
const HF_HOST = "huggingface.co";
const PROBE_TIMEOUT_MS = 8000;
// Path for recording a working proxy across runs (within the skill folder)
const PROXY_RECORD_FILE = path.join(
  os.homedir(), ".openclaw", "workspace", "skills", "openclaw-local-embedding", ".proxy"
);

// ─── Argument parsing ────────────────────────────────────────────────────────
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { proxy: null, openclawDir: null };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--proxy" && args[i + 1]) opts.proxy = args[++i];
    if (args[i] === "--openclaw-dir" && args[i + 1]) opts.openclawDir = args[++i];
  }
  return opts;
}

// ─── Auto-detect OpenClaw directory ──────────────────────────────────────────
function findOpenClawDir(hint) {
  if (hint && fs.existsSync(path.join(hint, "node_modules", "node-llama-cpp"))) {
    return hint;
  }
  // Try require.resolve
  try {
    const pkgPath = createRequire(import.meta.url).resolve("openclaw/package.json");
    const dir = path.dirname(pkgPath);
    if (fs.existsSync(path.join(dir, "node_modules", "node-llama-cpp"))) return dir;
  } catch {
    // not globally installed
  }
  // Common locations (npm global install)
  let npmGlobalLib = null;
  try {
    const npmRoot = execSync("npm root -g", { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
    if (npmRoot) npmGlobalLib = npmRoot;
  } catch { /* ignore */ }
  const candidates = [
    npmGlobalLib ? path.join(npmGlobalLib, "openclaw") : null,
    "/usr/local/lib/node_modules/openclaw",
    "/usr/lib/node_modules/openclaw",
    path.join(os.homedir(), ".npm-global", "lib", "node_modules", "openclaw"),
  ].filter(Boolean);
  for (const d of candidates) {
    if (fs.existsSync(path.join(d, "node_modules", "node-llama-cpp"))) return d;
  }
  return null;
}

// ─── Check model cache ──────────────────────────────────────────────────────
function findCachedModel() {
  const dirs = [
    path.join(os.homedir(), ".node-llama-cpp", "models"),
    path.join(os.homedir(), ".cache", "node-llama-cpp", "models"),
  ];
  for (const dir of dirs) {
    const p = path.join(dir, MODEL_CACHE_FILE);
    try {
      const s = fs.statSync(p);
      if (s.size > 100 * 1024 * 1024) return { path: p, sizeMB: Math.round(s.size / 1024 / 1024) };
    } catch {
      // not found
    }
  }
  return null;
}

// ─── Network probe ──────────────────────────────────────────────────────────
function probeDirectTLS(host, timeoutMs) {
  return new Promise((resolve) => {
    const sock = tls.connect({ host, port: 443, servername: host, timeout: timeoutMs }, () => {
      sock.destroy();
      resolve(true);
    });
    sock.on("error", () => resolve(false));
    sock.on("timeout", () => { sock.destroy(); resolve(false); });
  });
}

function probeViaCONNECT(proxyUrl, targetHost, timeoutMs) {
  return new Promise((resolve) => {
    let proxyHost, proxyPort;
    try {
      const u = new URL(proxyUrl);
      proxyHost = u.hostname;
      proxyPort = parseInt(u.port, 10) || 8080;
    } catch {
      resolve(false);
      return;
    }
    const sock = net.connect({ host: proxyHost, port: proxyPort }, () => {
      sock.write(`CONNECT ${targetHost}:443 HTTP/1.1\r\nHost: ${targetHost}:443\r\n\r\n`);
    });
    sock.setTimeout(timeoutMs);
    sock.once("data", (d) => {
      const ok = d.toString().includes("200");
      sock.destroy();
      resolve(ok);
    });
    sock.on("error", () => resolve(false));
    sock.on("timeout", () => { sock.destroy(); resolve(false); });
  });
}

// ─── Apply proxy env vars (process-scoped) ──────────────────────────────────
function applyProxyEnv(proxyUrl) {
  process.env.HTTPS_PROXY = proxyUrl;
  process.env.HTTP_PROXY = proxyUrl;
  process.env.https_proxy = proxyUrl;
  process.env.http_proxy = proxyUrl;
  process.env.NODE_USE_ENV_PROXY = "1";
  // Corporate/cloud proxies often perform TLS inspection (MITM); disable cert verification
  // for this download process only. Never persist this in shell profiles.
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
}

// ─── Print config instructions ──────────────────────────────────────────────
function printNextSteps() {
  console.log();
  console.log("=== Next steps ===");
  console.log();
  console.log("Add the following to ~/.openclaw/openclaw.json under agents.defaults:");
  console.log();
  console.log('  "memorySearch": {');
  console.log('    "enabled": true,');
  console.log('    "provider": "local",');
  console.log('    "fallback": "none",');
  console.log('    "query": {');
  console.log('      "hybrid": { "enabled": true }');
  console.log("    }");
  console.log("  }");
  console.log();
  console.log("Then restart the gateway:");
  console.log("  pkill -9 -f openclaw-gateway || true");
  console.log("  nohup openclaw gateway run --bind loopback --port 18789 --force > /tmp/openclaw-gateway.log 2>&1 &");
  console.log("  (or: cd ~/.openclaw && ./manage.sh restart  if manage.sh exists)");
  console.log();
  console.log("The first memory_search call will load the model (~1.6s).");
  console.log("After that, embedding runs fully offline with no network access.");
}

// ─── Main ───────────────────────────────────────────────────────────────────
async function main() {
  const opts = parseArgs();

  console.log("=========================================================");
  console.log("  OpenClaw Local Embedding — Model Initialization");
  console.log("=========================================================");
  console.log();

  // Step 1: Find OpenClaw
  const openclawDir = findOpenClawDir(opts.openclawDir);
  if (!openclawDir) {
    console.error("ERROR: Cannot find OpenClaw installation with node-llama-cpp.");
    console.error("Try: node init-model.mjs --openclaw-dir /path/to/openclaw");
    process.exit(1);
  }
  console.log(`OpenClaw directory: ${openclawDir}`);

  // Step 2: Check cache
  const cached = findCachedModel();
  if (cached) {
    console.log();
    console.log(`Model already cached (${cached.sizeMB} MB): ${cached.path}`);
    console.log("No download needed.");
    printNextSteps();
    process.exit(0);
  }
  console.log("Model not found in cache. Download required.");
  console.log();

  // Step 3: Network probe
  let proxyUrl = opts.proxy || null;

  if (!proxyUrl) {
    // 3a: Try recorded proxy from a previous successful run
    try {
      const recorded = fs.readFileSync(PROXY_RECORD_FILE, "utf8").trim();
      if (recorded) {
        console.log(`Found recorded proxy from previous run: ${recorded}`);
        const ok = await probeViaCONNECT(recorded, HF_HOST, PROBE_TIMEOUT_MS);
        if (ok) {
          console.log("  Recorded proxy works.");
          proxyUrl = recorded;
        } else {
          console.log("  Recorded proxy no longer works, will try other methods.");
        }
      }
    } catch { /* no recorded proxy */ }
  }

  if (!proxyUrl) {
    // 3b: Try current environment (user may have HTTPS_PROXY set)
    const envProxy = process.env.HTTPS_PROXY || process.env.https_proxy;
    console.log("Probing HuggingFace connectivity...");

    if (envProxy) {
      console.log(`  Testing existing proxy (${envProxy})...`);
      const ok = await probeViaCONNECT(envProxy, HF_HOST, PROBE_TIMEOUT_MS);
      if (ok) {
        console.log("  Existing proxy works.");
        proxyUrl = envProxy;
      } else {
        console.log("  Existing proxy failed.");
      }
    }

    if (!proxyUrl) {
      // 3c: Try direct connection
      console.log("  Testing direct connection...");
      const directOk = await probeDirectTLS(HF_HOST, PROBE_TIMEOUT_MS);
      if (directOk) {
        console.log("  Direct connection works. No proxy needed.");
      } else {
        console.log("  Direct connection failed.");

        // 3d: Try Kuaishou cloud default proxy
        console.log(`  Testing Kuaishou cloud default proxy (${KUAISHOU_DEFAULT_PROXY})...`);
        const builtinOk = await probeViaCONNECT(KUAISHOU_DEFAULT_PROXY, HF_HOST, PROBE_TIMEOUT_MS);
        if (builtinOk) {
          console.log("  Kuaishou cloud proxy works.");
          proxyUrl = KUAISHOU_DEFAULT_PROXY;
        } else {
          console.error();
          console.error("ERROR: Cannot reach HuggingFace. All methods failed:");
          console.error("  - Direct connection: FAILED");
          console.error("  - Kuaishou cloud proxy (" + KUAISHOU_DEFAULT_PROXY + "): FAILED");
          console.error();
          console.error("Please provide your proxy address:");
          console.error("  node init-model.mjs --proxy http://your-proxy:port");
          console.error();
          console.error("Or download the model manually and place it at:");
          console.error(`  ~/.node-llama-cpp/models/${MODEL_CACHE_FILE}`);
          process.exit(1);
        }
      }
    }
  } else {
    // User provided --proxy, verify it
    console.log(`Testing user-provided proxy (${proxyUrl})...`);
    const ok = await probeViaCONNECT(proxyUrl, HF_HOST, PROBE_TIMEOUT_MS);
    if (!ok) {
      console.error(`ERROR: Proxy ${proxyUrl} cannot reach ${HF_HOST}.`);
      process.exit(1);
    }
    console.log("  Proxy works.");
  }

  // Record working proxy for future runs
  if (proxyUrl) {
    try {
      fs.mkdirSync(path.dirname(PROXY_RECORD_FILE), { recursive: true });
      fs.writeFileSync(PROXY_RECORD_FILE, proxyUrl, "utf8");
      console.log(`  Proxy recorded for future runs: ${PROXY_RECORD_FILE}`);
    } catch { /* non-fatal */ }
  }

  // Apply proxy if needed
  if (proxyUrl) {
    console.log();
    console.log(`Using proxy: ${proxyUrl} (process-scoped, not persistent)`);
    applyProxyEnv(proxyUrl);
  }

  // Step 4: Download model
  console.log();
  console.log("Loading node-llama-cpp...");
  const require = createRequire(import.meta.url);
  const llamaCppPath = path.join(openclawDir, "node_modules", "node-llama-cpp");
  let resolveModelFile, getLlama, LlamaLogLevel;
  try {
    ({ resolveModelFile, getLlama, LlamaLogLevel } = require(llamaCppPath));
  } catch (err) {
    console.error("ERROR: Cannot load node-llama-cpp:", err.message);
    console.error();
    console.error("If cmake is missing or too old (need >= 3.19), run:");
    console.error("  pip3 install cmake");
    console.error("Then re-run this script.");
    process.exit(1);
  }

  console.log(`Downloading model (~313 MB, this may take a few minutes)...`);
  console.log(`Model: ${MODEL_ID}`);
  console.log();

  const t0 = Date.now();
  let modelPath;
  try {
    modelPath = await resolveModelFile(MODEL_ID);
  } catch (err) {
    console.error();
    console.error("ERROR: Model download failed:", err.message);
    console.error();
    console.error("Troubleshooting:");
    console.error("  1. If cmake is missing: pip3 install cmake");
    console.error("  2. Try a different proxy: node init-model.mjs --proxy http://...");
    console.error("  3. Manual download: place the .gguf file at");
    console.error(`     ~/.node-llama-cpp/models/${MODEL_CACHE_FILE}`);
    process.exit(1);
  }

  const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
  const sizeMB = Math.round(fs.statSync(modelPath).size / 1024 / 1024);

  console.log();
  console.log(`Download complete!`);
  console.log(`  Path: ${modelPath}`);
  console.log(`  Size: ${sizeMB} MB`);
  console.log(`  Time: ${elapsed}s`);

  // Step 5: Verify model loads
  console.log();
  console.log("Verifying model can be loaded...");
  try {
    const llama = await getLlama({ logLevel: LlamaLogLevel.error });
    const model = await llama.loadModel({ modelPath });
    await model.dispose();
    await llama.dispose();
    console.log("  Model verification passed.");
  } catch (err) {
    console.warn("  Model verification skipped:", err.message);
    console.warn("  (This may be fine — the gateway will retry on first use.)");
  }

  // Done
  console.log();
  console.log("=========================================================");
  console.log("  Model initialization complete!");
  console.log("=========================================================");
  printNextSteps();
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});

# TypeScript / JavaScript Template

Use this when the user wants Node.js or TypeScript code. Fill in `PREFERRED_MODELS`
and the example prompt from context. Keep inline comments.

```typescript
// openrouter_connect_client.ts — OpenRouter free-model client with ranked fallback
// Run: npx ts-node openrouter_connect_client.ts
// Or:  node openrouter_connect_client.js  (after tsc)

import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import OpenAI from "openai";  // npm install openai dotenv

// ── Config ──────────────────────────────────────────────────────────────────

/** Ranked preference list — tried in order, skipping unavailable free models */
const PREFERRED_MODELS: string[] = [
  // ── Tier 1: Qwen ──────────────────────────────────────
  "qwen/qwen-2.5-72b-instruct:free",
  "qwen/qwen-2.5-7b-instruct:free",
  "qwen/qwen-2-72b-instruct:free",
  // ── Tier 2: GLM (Zhipu AI) ────────────────────────────
  "thudm/glm-4-9b:free",
  "thudm/glm-z1-32b:free",
  // ── Tier 3: Nemotron (NVIDIA) ─────────────────────────
  "nvidia/llama-3.1-nemotron-70b-instruct:free",
  "nvidia/nemotron-4-340b-instruct:free",
  // ── Tier 4: auto-ranked pool takes over if all above fail
];

const OPENROUTER_API_BASE = "https://openrouter.ai/api/v1";
const MODELS_ENDPOINT     = `${OPENROUTER_API_BASE}/models`;
const CACHE_FILE          = path.join(os.tmpdir(), ".openrouter_free_models_cache.json");
const CACHE_TTL_MS        = 3_600_000; // 1 hour

// ── .env loading ─────────────────────────────────────────────────────────────

function loadEnvFile(filePath: string): Record<string, string> {
  if (!fs.existsSync(filePath)) return {};
  const lines = fs.readFileSync(filePath, "utf8").split("\n");
  const out: Record<string, string> = {};
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIdx = trimmed.indexOf("=");
    if (eqIdx < 0) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    const val = trimmed.slice(eqIdx + 1).trim().replace(/^["']|["']$/g, "");
    out[key] = val;
  }
  return out;
}

function resolveEnv(): Record<string, string> {
  // 1. Project .env  2. ~/.env  3. process.env (already exported)
  const projectEnv = loadEnvFile(path.join(process.cwd(), ".env"));
  const globalEnv  = loadEnvFile(path.join(os.homedir(), ".env"));
  // Later entries win — process.env takes precedence
  return { ...globalEnv, ...projectEnv, ...process.env as Record<string, string> };
}

const ENV = resolveEnv();

function getApiKey(): string {
  const key = ENV["OPENROUTER_API_KEY"]?.trim();
  if (!key) throw new Error(
    "OPENROUTER_API_KEY not found.\n" +
    "Add it to ./.env or ~/.env:\n\n" +
    "  OPENROUTER_API_KEY=sk-or-...\n\n" +
    "Get a free key at https://openrouter.ai/keys"
  );
  return key;
}

// ── Free model discovery ──────────────────────────────────────────────────────

interface ModelInfo {
  id: string;
  context_length?: number;
  created?: number;
  pricing?: { prompt?: string; completion?: string };
}

async function fetchFreeModels(forceRefresh = false): Promise<ModelInfo[]> {
  // Return from cache if fresh
  if (!forceRefresh && fs.existsSync(CACHE_FILE)) {
    const mtime = fs.statSync(CACHE_FILE).mtimeMs;
    if (Date.now() - mtime < CACHE_TTL_MS) {
      return JSON.parse(fs.readFileSync(CACHE_FILE, "utf8")) as ModelInfo[];
    }
  }

  const resp = await fetch(MODELS_ENDPOINT);
  const json = await resp.json() as { data: ModelInfo[] };

  const free = json.data.filter(
    (m) => m.pricing?.prompt === "0" && m.pricing?.completion === "0"
  );

  fs.writeFileSync(CACHE_FILE, JSON.stringify(free));
  return free;
}

function autoRank(freeModels: ModelInfo[]): string[] {
  const tierA = new Set(
    (ENV["OPENROUTER_TIER_A"] || "google,meta-llama,mistralai,anthropic").split(",")
  );
  const tierB = new Set(
    (ENV["OPENROUTER_TIER_B"] || "qwen,nvidia,microsoft,cohere,deepseek").split(",")
  );

  const now = Date.now() / 1000;

  const scored = freeModels.map((m) => {
    const ctx   = m.context_length ?? 4096;
    const ctxS  = Math.min(Math.log(Math.max(ctx, 1)) / Math.log(200_000), 1);

    const ageDays = m.created ? (now - m.created) / 86400 : 730;
    const recS  = Math.max(0, 1 - ageDays / 730);

    const provider = m.id.split("/")[0];
    const repS  = tierA.has(provider) ? 1.0 : tierB.has(provider) ? 0.7 : 0.4;

    return { id: m.id, score: 0.4 * ctxS + 0.3 * recS + 0.3 * repS };
  });

  return scored.sort((a, b) => b.score - a.score).map((m) => m.id);
}

// ── Query with fallback ───────────────────────────────────────────────────────

interface QueryOptions {
  preferred?: string[];
  system?: string;
  maxRetries?: number;
  stream?: boolean;
}

async function query(prompt: string, opts: QueryOptions = {}): Promise<string> {
  const {
    system     = "You are a helpful assistant.",
    maxRetries = 3,
    stream     = true,
  } = opts;

  const freeModels = await fetchFreeModels();
  const freeIds    = new Set(freeModels.map((m) => m.id));

  const envPrefs  = ENV["OPENROUTER_PREFERRED_MODELS"]?.split(",").map((s) => s.trim()).filter(Boolean) ?? [];
  const preferred = opts.preferred ?? (envPrefs.length ? envPrefs : PREFERRED_MODELS);

  const ranked  = autoRank(freeModels);
  // preferred (filtered to free) + auto-ranked extras not already in list
  const ordered = [
    ...preferred.filter((id) => freeIds.has(id)),
    ...ranked.filter((id) => !preferred.includes(id)),
  ].slice(0, maxRetries);

  const client = new OpenAI({
    apiKey:  getApiKey(),
    baseURL: OPENROUTER_API_BASE,
  });

  const tried: string[] = [];

  for (const modelId of ordered) {
    tried.push(modelId);
    try {
      console.log(`[openrouter-connect] Trying: ${modelId}`);
      const messages = [
        { role: "system" as const, content: system },
        { role: "user"   as const, content: prompt },
      ];

      if (stream) {
        const streamResp = await client.chat.completions.create({
          model: modelId, messages, stream: true,
        });
        const chunks: string[] = [];
        for await (const chunk of streamResp) {
          const delta = chunk.choices[0]?.delta?.content ?? "";
          process.stdout.write(delta);
          chunks.push(delta);
        }
        process.stdout.write("\n");
        return chunks.join("");
      } else {
        const resp = await client.chat.completions.create({ model: modelId, messages });
        return resp.choices[0].message.content ?? "";
      }
    } catch (err: unknown) {
      const msg = String(err);
      if (msg.includes("429") || /5\d\d/.test(msg)) {
        console.log(`[openrouter-connect] ${modelId} failed (${msg.slice(0, 60)}), trying next…`);
        continue;
      }
      throw err;
    }
  }

  throw new Error(`All ${maxRetries} models failed or rate-limited.\nTried: ${tried.join(", ")}`);
}

// ── Main ─────────────────────────────────────────────────────────────────────

(async () => {
  const answer = await query("Explain what a large language model is in two sentences.");
  // answer is also available as a return value when imported as a module
})();
```

## Dependencies

```bash
npm install openai
# TypeScript only:
npm install -D typescript ts-node @types/node
```

## Usage (ESM import)

```typescript
import { query } from "./openrouter_connect_client.js";

const answer = await query("What is the capital of France?");

// Custom preference list
const answer2 = await query("Write a haiku about TypeScript.", {
  preferred: [
    "google/gemini-2.0-flash-exp:free",
    "mistralai/mistral-7b-instruct:free",
  ],
});
```

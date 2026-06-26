// Optional opt-in semantic tone matching.
//
// PRIVACY / NETWORK:
// - When --vector-tones is invoked, tone-intent text is sent over HTTP to
//   OLLAMA_URL (default: http://localhost:11434). This feature is OFF
//   unless the user explicitly enables semantic matching.
// - Embeddings and the corresponding source text are cached on disk at
//   <runtimeDir>/tone-embeddings.json with no expiry.
// - Non-loopback OLLAMA_URL endpoints are refused unless the user opts
//   in with POKE_ALLOW_REMOTE_OLLAMA=1.
import fs from "node:fs";
import path from "node:path";

const OLLAMA_URL = process.env.OLLAMA_URL || "http://localhost:11434";
const EMBED_MODEL = process.env.Poke_EMBED_MODEL || "all-minilm";
const CACHE_FILE = "tone-embeddings.json";

function assertOllamaEndpointAllowed() {
  let url;
  try { url = new URL(OLLAMA_URL); }
  catch { throw new Error(`OLLAMA_URL is not a valid URL: ${OLLAMA_URL}`); }
  const host = url.hostname;
  const isLoopback = host === "localhost" || host === "127.0.0.1" || host === "::1" || host === "[::1]";
  if (!isLoopback && process.env.POKE_ALLOW_REMOTE_OLLAMA !== "1") {
    throw new Error(
      `OLLAMA_URL points to a non-loopback host (${host}). Vector-tone matching would send ` +
      `reminder/intent text off this machine. Set POKE_ALLOW_REMOTE_OLLAMA=1 to acknowledge ` +
      `the privacy implications, or point OLLAMA_URL back at localhost.`
    );
  }
}

function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

async function embed(text) {
  assertOllamaEndpointAllowed();
  const res = await fetch(`${OLLAMA_URL}/api/embed`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model: EMBED_MODEL, input: text })
  });
  if (!res.ok) throw new Error(`Ollama embed failed: ${res.status}`);
  const data = await res.json();
  return data.embeddings?.[0] || data.embedding;
}

export async function loadOrBuildCache(tones, runtimeDir) {
  const cachePath = path.join(runtimeDir, CACHE_FILE);
  let cache = {};
  try {
    cache = JSON.parse(fs.readFileSync(cachePath, "utf8"));
  } catch {}

  const model = EMBED_MODEL;
  const needsRefresh = tones.some(t => {
    const entry = cache[t.id];
    return !entry || entry.model !== model || entry.text !== toneText(t);
  });

  if (needsRefresh) {
    for (const tone of tones) {
      const text = toneText(tone);
      try {
        const vec = await embed(text);
        cache[tone.id] = { vec, model, text };
      } catch (e) {
        // If embed fails, skip this tone
        if (!cache[tone.id]) cache[tone.id] = { vec: null, model, text };
      }
    }
    fs.writeFileSync(cachePath, JSON.stringify(cache));
  }

  return cache;
}

function toneText(tone) {
  const d = tone.data || tone;
  return [d.label || d.id || "", d.description || "", d.guidance || ""].filter(Boolean).join(" ");
}

export async function matchTone(intentText, tones, runtimeDir) {
  const cache = await loadOrBuildCache(tones, runtimeDir);
  const intentVec = await embed(intentText);
  if (!intentVec) return null;

  let best = null;
  let bestScore = -1;
  for (const tone of tones) {
    const entry = cache[tone.id];
    if (!entry?.vec) continue;
    const score = cosineSimilarity(intentVec, entry.vec);
    if (score > bestScore) {
      bestScore = score;
      best = tone;
    }
  }
  return best ? { tone: best, score: bestScore } : null;
}

export async function isAvailable() {
  try {
    assertOllamaEndpointAllowed();
    const res = await fetch(`${OLLAMA_URL}/api/embed`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: EMBED_MODEL, input: "test" })
    });
    return res.ok;
  } catch {
    return false;
  }
}

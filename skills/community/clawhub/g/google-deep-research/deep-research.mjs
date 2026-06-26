#!/usr/bin/env node

/**
 * deep-research.mjs — Gemini Deep Research helper script
 *
 * Runs the Gemini Interactions API with the deep-research agent and streams
 * research progress to stderr, final Markdown report to stdout.
 *
 * Distribution rules:
 * - Requires GEMINI_API_KEY from the environment
 * - Uses @google/genai from npm by default
 * - Optionally accepts an explicit GOOGLE_GENAI_SDK_PATH override
 * - Does NOT auto-read local OpenClaw config files
 *
 * Usage:
 *   node deep-research.mjs "research topic"
 *   node deep-research.mjs "research topic" --timeout 1800
 *   node deep-research.mjs --follow-up <interaction_id> "follow-up question"
 *   node deep-research.mjs "research topic" --no-stream
 *
 * Exit codes: 0 = success, 1 = arg error, 2 = setup/API error, 3 = timeout
 */

import { pathToFileURL } from 'node:url';
import path from 'node:path';

// ─── SDK resolution ────────────────────────────────────────────────────────
async function loadGoogleGenAI() {
  const candidates = [process.env.GOOGLE_GENAI_SDK_PATH?.trim(), '@google/genai'].filter(Boolean);
  const errors = [];

  for (const candidate of candidates) {
    try {
      const specifier =
        candidate.startsWith('/') || candidate.startsWith('.')
          ? pathToFileURL(path.resolve(candidate)).href
          : candidate;
      const mod = await import(specifier);
      if (mod?.GoogleGenAI) {
        return mod.GoogleGenAI;
      }
      errors.push(`${candidate}: GoogleGenAI export not found`);
    } catch (err) {
      errors.push(`${candidate}: ${err.message}`);
    }
  }

  throw new Error(
    `Unable to load @google/genai. Install it from npm, or set GOOGLE_GENAI_SDK_PATH explicitly. Tried: ${candidates.join(', ')}${
      errors.length ? `\n${errors.join('\n')}` : ''
    }`,
  );
}

const GoogleGenAI = await loadGoogleGenAI();

// ─── Argument parsing ───────────────────────────────────────────────────────
const argv = process.argv.slice(2);
let query = null;
let timeout = 3600;
let followUpId = null;
let useStream = true;

for (let i = 0; i < argv.length; i++) {
  switch (argv[i]) {
    case '--timeout':
      timeout = parseInt(argv[++i], 10);
      if (Number.isNaN(timeout) || timeout <= 0) {
        console.error('Error: --timeout must be a positive integer (seconds).');
        process.exit(1);
      }
      break;
    case '--follow-up':
      followUpId = argv[++i];
      if (!followUpId) {
        console.error('Error: --follow-up requires an interaction ID.');
        process.exit(1);
      }
      break;
    case '--no-stream':
      useStream = false;
      break;
    case '--help':
      printUsage();
      process.exit(0);
      break;
    default:
      if (!query && !argv[i].startsWith('-')) {
        query = argv[i];
      }
      break;
  }
}

function printUsage() {
  console.error(
    `Usage: node deep-research.mjs "research topic" [options]

Options:
  --timeout <seconds>           Max wait time (default: 3600)
  --follow-up <interaction_id>  Continue a previous research session
  --no-stream                   Use polling instead of streaming
  --help                        Show this help

Environment:
  GEMINI_API_KEY                Required Gemini API key
  GOOGLE_GENAI_SDK_PATH         Optional explicit @google/genai SDK path

Exit codes:
  0  Success
  1  Argument error
  2  Setup or API error
  3  Timeout`,
  );
}

if (!query) {
  console.error('Error: Research topic is required.\n');
  printUsage();
  process.exit(1);
}

const apiKey = process.env.GEMINI_API_KEY?.trim();
if (!apiKey) {
  console.error('Error: GEMINI_API_KEY environment variable is required.');
  process.exit(2);
}

// ─── Initialize ─────────────────────────────────────────────────────────────
const client = new GoogleGenAI({ apiKey });
const startTime = Date.now();

const timeoutId = setTimeout(() => {
  console.error(`\n⏰ Research timed out after ${timeout}s.`);
  process.exit(3);
}, timeout * 1000);

// ─── Build request ──────────────────────────────────────────────────────────
console.error(`🔬 Starting deep research: "${query}"`);
if (followUpId) {
  console.error(`📎 Following up on interaction: ${followUpId}`);
}

const params = {
  agent: 'deep-research-pro-preview-12-2025',
  input: query,
  background: true,
  stream: useStream,
  agent_config: {
    type: 'deep-research',
    thinking_summaries: 'auto',
  },
  ...(followUpId && { previous_interaction_id: followUpId }),
};

// ─── Execute ────────────────────────────────────────────────────────────────
try {
  if (useStream) {
    await runStreaming(params);
  } else {
    await runPolling(params);
  }
} catch (err) {
  console.error(`\n❌ API Error: ${err.message}`);
  if (err.status) console.error(`   HTTP Status: ${err.status}`);
  process.exit(2);
} finally {
  clearTimeout(timeoutId);
}

// ─── Streaming mode ─────────────────────────────────────────────────────────
async function runStreaming(params) {
  const stream = await client.interactions.create(params);
  let interactionId = null;

  for await (const event of stream) {
    switch (event.event_type) {
      case 'interaction.start':
        interactionId = event.interaction?.id;
        console.error(`📊 Research started (ID: ${interactionId})`);
        break;

      case 'interaction.status_update':
        console.error(`📊 Status: ${event.status}`);
        break;

      case 'content.delta':
        handleDelta(event);
        break;

      case 'content.start':
      case 'content.stop':
        break;

      case 'interaction.complete': {
        const elapsed = formatElapsed(Date.now() - startTime);
        console.error(`\n✅ Research complete (${elapsed})`);
        if (interactionId) {
          console.error(`📎 Interaction ID: ${interactionId}`);
        }
        break;
      }

      case 'error':
        console.error(`\n❌ Error event: ${JSON.stringify(event)}`);
        break;
    }
  }
}

function handleDelta(event) {
  const delta = event.delta;
  if (!delta) return;

  if (delta.type === 'text') {
    process.stdout.write(delta.text || '');
  } else if (delta.type === 'thought_summary') {
    const text = delta.content?.text || '';
    if (text) {
      console.error(`💭 ${text}`);
    }
  }
}

// ─── Polling mode ───────────────────────────────────────────────────────────
async function runPolling(params) {
  const interaction = await client.interactions.create({
    ...params,
    stream: false,
  });
  const id = interaction.id;
  console.error(`📊 Research created (ID: ${id})`);

  const POLL_INTERVAL = 15_000;

  while (true) {
    await sleep(POLL_INTERVAL);

    const updated = await client.interactions.get(id);
    const status = updated.status;
    const elapsed = formatElapsed(Date.now() - startTime);
    console.error(`📊 Status: ${status} (${elapsed})`);

    if (status === 'completed') {
      outputInteractionContent(updated);
      console.error(`\n✅ Research complete (${elapsed})`);
      console.error(`📎 Interaction ID: ${id}`);
      return;
    }

    if (status === 'failed' || status === 'cancelled' || status === 'incomplete') {
      console.error(`\n❌ Research ${status}.`);
      process.exit(2);
    }
  }
}

function outputInteractionContent(interaction) {
  const output = interaction.output || interaction.outputs || [];
  for (const item of Array.isArray(output) ? output : [output]) {
    if (typeof item === 'string') {
      process.stdout.write(item);
    } else if (item?.text) {
      process.stdout.write(item.text);
    } else if (item?.content) {
      const parts = Array.isArray(item.content) ? item.content : [item.content];
      for (const part of parts) {
        if (part?.text) process.stdout.write(part.text);
      }
    }
  }
}

// ─── Utilities ──────────────────────────────────────────────────────────────
function formatElapsed(ms) {
  const totalSec = Math.floor(ms / 1000);
  const m = Math.floor(totalSec / 60);
  const s = totalSec % 60;
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

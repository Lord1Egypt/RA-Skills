#!/usr/bin/env node
/**
 * conversation-summarise.js
 * Channel-agnostic conversation summariser for OpenClaw agents.
 * 
 * Reads raw archive files produced by conversation-archive.js and generates
 * AI-powered summaries per topic + a master digest per group.
 * 
 * Model: Uses OpenRouter (free tier by default) or any OpenAI-compatible API.
 * Configure via archive-config.json or environment variables.
 * 
 * Usage:
 *   node scripts/conversation-summarise.js [--channel telegram] [--group <name>] [--all] [--force]
 */

'use strict';

const fs = require('fs');
const path = require('path');
const https = require('https');

// ─── Configurable paths ─────────────────────────────────────────────────────

const WORKSPACE = path.resolve(__dirname, '..');
const ARCHIVE_DIR = path.join(WORKSPACE, 'archives');
const CONFIG_PATH = path.join(ARCHIVE_DIR, 'archive-config.json');

function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    try { return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8')); } catch {}
  }
  return {};
}

// ─── API client ─────────────────────────────────────────────────────────────

function getApiKey() {
  // Check multiple env file locations
  const envFiles = [
    path.join(WORKSPACE, '.env.openrouter'),
    path.join(WORKSPACE, '.env.openai'),
    path.join(WORKSPACE, '.env'),
  ];
  
  for (const envFile of envFiles) {
    if (!fs.existsSync(envFile)) continue;
    const content = fs.readFileSync(envFile, 'utf8');
    const orMatch = content.match(/OPENROUTER_API_KEY=(.+)/);
    if (orMatch) return orMatch[1].trim();
    const oaiMatch = content.match(/OPENAI_API_KEY=(.+)/);
    if (oaiMatch) return oaiMatch[1].trim();
  }
  
  return process.env.OPENROUTER_API_KEY || process.env.OPENAI_API_KEY;
}

async function callLLM(prompt, systemPrompt = '') {
  const config = loadConfig();
  const apiKey = getApiKey();
  if (!apiKey) throw new Error('No API key found. Set OPENROUTER_API_KEY or OPENAI_API_KEY in .env.openrouter or environment.');
  
  const messages = [];
  if (systemPrompt) messages.push({ role: 'system', content: systemPrompt });
  messages.push({ role: 'user', content: prompt });
  
  const isOpenRouter = apiKey.startsWith('sk-or-');
  const model = config.summariseModel || (isOpenRouter ? 'google/gemma-3-27b-it:free' : 'gpt-4o-mini');
  
  const body = JSON.stringify({ model, max_tokens: 4096, messages });
  
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: isOpenRouter ? 'openrouter.ai' : 'api.openai.com',
      path: isOpenRouter ? '/api/v1/chat/completions' : '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.error) reject(new Error(parsed.error.message));
          else resolve(parsed.choices?.[0]?.message?.content || '');
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ─── State tracking ─────────────────────────────────────────────────────────

function readState(groupDir) {
  const statePath = path.join(groupDir, '.summary-state.json');
  if (fs.existsSync(statePath)) {
    try { return JSON.parse(fs.readFileSync(statePath, 'utf8')); } catch {}
  }
  return { topics: {} };
}

function writeState(groupDir, state) {
  fs.writeFileSync(path.join(groupDir, '.summary-state.json'), JSON.stringify(state, null, 2));
}

// ─── Redaction ──────────────────────────────────────────────────────────────

/**
 * Redact likely secrets, tokens, and credentials from text before sending
 * to an external LLM. Patterns are intentionally broad — false positives
 * (redacting non-secrets) are preferable to leaking real secrets.
 */
function redactSecrets(text) {
  return text
    // API keys / tokens (common prefixes)
    .replace(/\b(sk-[a-zA-Z0-9_-]{20,})\b/g, '[REDACTED_API_KEY]')
    .replace(/\b(sk-or-[a-zA-Z0-9_-]{20,})\b/g, '[REDACTED_API_KEY]')
    .replace(/\b(ghp_[a-zA-Z0-9]{30,})\b/g, '[REDACTED_GITHUB_TOKEN]')
    .replace(/\b(ghu_[a-zA-Z0-9]{30,})\b/g, '[REDACTED_GITHUB_TOKEN]')
    .replace(/\b(clh_[a-zA-Z0-9_-]{20,})\b/g, '[REDACTED_CLAWHUB_TOKEN]')
    .replace(/\b(xoxb-[a-zA-Z0-9-]+)\b/g, '[REDACTED_SLACK_TOKEN]')
    .replace(/\b(xoxp-[a-zA-Z0-9-]+)\b/g, '[REDACTED_SLACK_TOKEN]')
    // Bearer tokens in headers
    .replace(/(Bearer\s+)[a-zA-Z0-9_.-]{20,}/gi, '$1[REDACTED_TOKEN]')
    .replace(/(Authorization:\s*)[^\s\n]{20,}/gi, '$1[REDACTED_AUTH]')
    // Passwords in common formats
    .replace(/(password|passwd|pwd|secret)[\s:=]+\S{6,}/gi, '$1 [REDACTED]')
    // AWS keys
    .replace(/\b(AKIA[A-Z0-9]{16})\b/g, '[REDACTED_AWS_KEY]')
    // Generic long hex/base64 strings that look like secrets (40+ chars)
    .replace(/\b[a-f0-9]{40,}\b/g, '[REDACTED_HEX]')
    // .env variable assignments with values
    .replace(/^(\w*(?:KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)\w*\s*=\s*).+$/gim, '$1[REDACTED]');
}

// ─── Summarisation ──────────────────────────────────────────────────────────

const SUMMARY_SYSTEM_PROMPT = `You are summarising a group chat conversation for a personal knowledge base.
Extract and organise into these sections (skip empty sections):

## Key Decisions
Concrete decisions that were made.

## Action Items
Things that need doing, with status if known (✅ done, 🔨 in progress, ⏳ pending).

## Insights & Ideas
Interesting ideas, observations, or learnings discussed.

## Technical Notes
Architecture decisions, configs, commands, URLs, or technical details worth remembering.

## Links & Resources
URLs, documents, or tools mentioned.

## Open Questions
Unresolved questions or things to come back to.

## Timeline
Brief chronological summary of what happened, with dates.

Be concise. Focus on what's worth remembering months from now. Skip pleasantries and debugging back-and-forth unless the resolution is important.`;

async function summariseTopic(rawFile, summaryFile, existingSummary, force = false) {
  const rawContent = fs.readFileSync(rawFile, 'utf8');
  
  if (rawContent.split('\n').filter(l => l.trim()).length < 10) {
    return { skipped: true, reason: 'too few messages' };
  }
  
  // Redact secrets before sending to external LLM
  const safeContent = redactSecrets(rawContent);
  
  let prompt;
  if (existingSummary && !force) {
    prompt = `Here is the EXISTING summary of this topic:\n\n${existingSummary}\n\n---\n\nHere is the FULL conversation (which may include new messages since the last summary):\n\n${safeContent}\n\nUpdate the summary to incorporate any new information. Keep the same structure. Don't lose existing insights.`;
  } else {
    prompt = `Summarise this conversation:\n\n${safeContent}`;
  }
  
  // Truncate if too long
  if (prompt.length > 150000) {
    prompt = prompt.slice(0, 150000) + '\n\n[...truncated for length]';
  }
  
  const summary = await callLLM(prompt, SUMMARY_SYSTEM_PROMPT);
  
  const titleMatch = rawContent.match(/^# .+ — (.+)$/m);
  const topicName = titleMatch ? titleMatch[1] : path.basename(rawFile, '.md');
  
  const output = `# ${topicName} — Summary\n\n*Last updated: ${new Date().toISOString()}*\n\n${summary}\n`;
  fs.writeFileSync(summaryFile, output);
  
  return { skipped: false, size: Buffer.byteLength(rawContent) };
}

async function generateDigest(groupDir, groupLabel) {
  const summaryDir = path.join(groupDir, 'summaries');
  if (!fs.existsSync(summaryDir)) return;
  
  const summaryFiles = fs.readdirSync(summaryDir).filter(f => f.endsWith('.md'));
  if (summaryFiles.length === 0) return;
  
  let allSummaries = '';
  for (const f of summaryFiles) {
    allSummaries += fs.readFileSync(path.join(summaryDir, f), 'utf8') + '\n\n---\n\n';
  }
  
  const digest = await callLLM(
    `Create a master digest for the "${groupLabel}" group from these topic summaries:\n\n${allSummaries}`,
    'You are creating a master digest of a group\'s activity. Create a concise, scannable overview that helps someone quickly understand what\'s been discussed and decided across all topics. Group by theme, highlight the most important decisions and open items.'
  );
  
  fs.writeFileSync(
    path.join(groupDir, 'DIGEST.md'),
    `# ${groupLabel} — Master Digest\n\n*Last updated: ${new Date().toISOString()}*\n\n${digest}\n`
  );
  console.log(`  📋 DIGEST.md updated`);
}

// ─── Main ───────────────────────────────────────────────────────────────────

async function processGroup(groupDir, groupLabel, force = false) {
  const rawDir = path.join(groupDir, 'raw');
  const summaryDir = path.join(groupDir, 'summaries');
  
  if (!fs.existsSync(rawDir)) {
    console.log(`  ⚠️  No raw/ directory`);
    return 0;
  }
  
  fs.mkdirSync(summaryDir, { recursive: true });
  
  const state = readState(groupDir);
  const rawFiles = fs.readdirSync(rawDir).filter(f => f.endsWith('.md'));
  let updated = 0;
  
  for (const rawFile of rawFiles) {
    const rawPath = path.join(rawDir, rawFile);
    const summaryPath = path.join(summaryDir, rawFile);
    const rawSize = fs.statSync(rawPath).size;
    
    const lastSize = state.topics[rawFile]?.lastSummarisedBytes || 0;
    if (!force && rawSize === lastSize && fs.existsSync(summaryPath)) continue;
    
    const existingSummary = fs.existsSync(summaryPath) ? fs.readFileSync(summaryPath, 'utf8') : null;
    
    try {
      console.log(`  🤖 Summarising ${rawFile}...`);
      const result = await summariseTopic(rawPath, summaryPath, existingSummary, force);
      
      if (result.skipped) {
        console.log(`    ⏭️  Skipped (${result.reason})`);
      } else {
        state.topics[rawFile] = { lastSummarisedBytes: rawSize, updatedAt: new Date().toISOString() };
        updated++;
        console.log(`    ✅ Done`);
      }
    } catch (e) {
      console.error(`    ❌ Error: ${e.message}`);
    }
    
    // Rate limiting — adjust based on your API tier
    const waitMs = rawSize > 50000 ? 90000 : rawSize > 20000 ? 60000 : 30000;
    console.log(`    ⏱️  Waiting ${waitMs / 1000}s (rate limit)...`);
    await new Promise(r => setTimeout(r, waitMs));
  }
  
  writeState(groupDir, state);
  
  if (updated > 0) {
    console.log(`  🔄 Generating master digest...`);
    await generateDigest(groupDir, groupLabel);
  }
  
  return updated;
}

async function main() {
  const args = process.argv.slice(2);
  const channelFilter = args.includes('--channel') ? args[args.indexOf('--channel') + 1] : null;
  const groupFilter = args.includes('--group') ? args[args.indexOf('--group') + 1] : null;
  const force = args.includes('--force');
  
  console.log('🧠 Conversation Summariser\n');
  
  // Discover all archived groups
  const channels = fs.readdirSync(ARCHIVE_DIR).filter(f => {
    const p = path.join(ARCHIVE_DIR, f);
    return fs.statSync(p).isDirectory() && f !== 'archive-config.json';
  });
  
  for (const channel of channels) {
    if (channelFilter && channel !== channelFilter) continue;
    
    const channelDir = path.join(ARCHIVE_DIR, channel);
    const groups = fs.readdirSync(channelDir).filter(f =>
      fs.statSync(path.join(channelDir, f)).isDirectory()
    );
    
    for (const group of groups) {
      if (groupFilter && group !== groupFilter) continue;
      
      const groupDir = path.join(channelDir, group);
      const indexPath = path.join(groupDir, 'INDEX.md');
      if (!fs.existsSync(indexPath)) continue;
      
      // Try to extract label from INDEX.md
      const indexContent = fs.readFileSync(indexPath, 'utf8');
      const labelMatch = indexContent.match(/^# (.+?) —/m);
      const groupLabel = labelMatch ? labelMatch[1] : group;
      
      console.log(`\n📱 ${groupLabel} (${channel}/${group})`);
      await processGroup(groupDir, groupLabel, force);
    }
  }
  
  console.log('\n✅ Summarisation complete');
}

main().catch(e => { console.error(e); process.exit(1); });

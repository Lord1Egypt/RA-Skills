#!/usr/bin/env node
// Standalone archiver (no TS build required)
// Run: node standalone-archive.js

import { promises as fs } from 'fs';
import { join } from 'path';

// ──────────────────────────────────────────
// Configuration (can be overridden by env)
// ──────────────────────────────────────────
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.cwd();
const MEMORY_DIR = join(WORKSPACE, 'memory');
const LOGS_DIR = join(WORKSPACE, 'logs');
const DEFAULT_KEYWORDS = (
  'lobster,OpenClaw,任务,记得,记住,重要,明天,计划,问题,修复,部署,安装,配置,' +
  'task,remember,important,tomorrow,plan,issue,fix,deploy,install,config,' +
  'API,token,password,key,secret,错误,失败,成功,更新,script,command'
).split(',');

// ──────────────────────────────────────────
// Logging
// ──────────────────────────────────────────
let logPath = join(LOGS_DIR, 'memory-archive.log');
function log(msg) {
  const ts = new Date().toISOString();
  const line = `[${ts}] ${msg}`;
  console.log(line);
  try { fs.appendFile(logPath, line + '\n', 'utf8').catch(() => {}); } catch {}
}

// ──────────────────────────────────────────
// Main
// ──────────────────────────────────────────
(async () => {
  log('=== Standalone Archive Start ===');
  
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yStr = yesterday.toISOString().split('T')[0];
  const dailyFile = join(MEMORY_DIR, `${yStr}.md`);
  
  log(`Check: ${yStr}`);
  
  try {
    await fs.access(dailyFile);
    log('Already exists, exit');
    process.exit(0);
  } catch {
    // continue
  }
  
  // Find transcripts
  const agentsDir = join(WORKSPACE, 'agents');
  let transcripts = [];
  try {
    const agents = await fs.readdir(agentsDir);
    for (const agent of agents) {
      const sessionDir = join(agentsDir, agent, 'sessions');
      try {
        const files = await fs.readdir(sessionDir);
        for (const f of files) {
          if (f.endsWith('.jsonl')) {
            transcripts.push(join(sessionDir, f));
          }
        }
      } catch {}
    }
  } catch (e) {
    log('WARN: No agents dir');
  }
  
  if (transcripts.length === 0) {
    log('ERROR: No transcripts found');
    process.exit(1);
  }
  
  log(`Scanning ${transcripts.length} files`);
  
  // Extract messages
  const startOfDay = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate());
  const endOfDay = new Date(startOfDay); endOfDay.setDate(endOfDay.getDate() + 1);
  
  const messages = [];
  let skipped = 0;
  
  for (const file of transcripts) {
    try {
      const content = await fs.readFile(file, 'utf8');
      const lines = content.split('\n');
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const msg = JSON.parse(line);
          if (msg.type !== 'message' || !msg.message) continue;
          
          const utc = new Date(msg.timestamp);
          const local = new Date(utc.getTime() + (utc.getTimezoneOffset() * 60000));
          
          if (local >= startOfDay && local < endOfDay) {
            const textObj = msg.message.content.find(c => c.type === 'text');
            if (textObj?.text) {
              messages.push({
                role: msg.message.role,
                text: textObj.text,
                time: local
              });
            }
          }
        } catch (e) { skipped++; }
      }
    } catch (e) {}
  }
  
  log(`Found ${messages.length} messages (skipped ${skipped})`);
  
  if (messages.length === 0) {
    await fs.mkdir(MEMORY_DIR, { recursive: true });
    await fs.writeFile(dailyFile, '# ' + yStr + ' Work Log\n\nNo messages to archive.\n', 'utf8');
    await fs.writeFile(join(MEMORY_DIR, '.' + yStr + '.archived'), 'done', 'utf8');
    log('Empty log created');
    process.exit(0);
  }
  
  // Highlights
  const userMsgs = messages.filter(m => m.role === 'user');
  const asstMsgs = messages.filter(m => m.role === 'assistant');
  const highlights = [];
  
  for (const m of messages) {
    for (const kw of DEFAULT_KEYWORDS) {
      if (m.text.toLowerCase().includes(kw.toLowerCase())) {
        const snippet = m.text.substring(0, Math.min(80, m.text.length)) + (m.text.length > 80 ? '...' : '');
        highlights.push((m.role === 'user' ? 'User' : 'Asst') + ': ' + snippet);
        break;
      }
    }
  }
  
  // Render
  const content = `# ${yStr} Work Log

## Summary
User: ${userMsgs.length}
Assistant: ${asstMsgs.length}

### Highlights
${highlights.length > 0 ? highlights.join('\n') : 'No highlights'}

---
Auto-archived by openclaw-memory-auto
`;
  
  await fs.mkdir(MEMORY_DIR, { recursive: true });
  await fs.writeFile(dailyFile, content, 'utf8');
  await fs.writeFile(join(MEMORY_DIR, '.' + yStr + '.archived'), 'done', 'utf8');
  
  log(`Wrote: ${dailyFile}`);
  log('=== Archive Complete ===');
  process.exit(0);
})();

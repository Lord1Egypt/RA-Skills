#!/usr/bin/env node
// Memory refinement script - analyzes daily logs and updates MEMORY.md
// This would call AI API to extract structured memory

import { readFile, writeFile, appendFile } from 'fs/promises';
import { join } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.cwd();
const MEMORY_FILE = join(WORKSPACE, 'MEMORY.md');
const LOGS_DIR = join(WORKSPACE, 'logs');
const PROMPT_FILE = join(LOGS_DIR, 'last_refine_prompt.txt');

// Simple refinement: append content to MEMORY.md for now
// In future, call StepFun API to get structured JSON

async function refine() {
  console.log('=== MEMORY REFINE START ===');

  // Read prompt (contains daily summary)
  const prompt = await readFile(PROMPT_FILE, 'utf8');
  const dailySummary = prompt.split('Analyze:')[1]?.split('Output JSON')[0]?.trim() || '';

  if (!dailySummary) {
    console.log('No daily summary found');
    return;
  }

  // For now: append a simple section to MEMORY.md
  const dateStr = new Date().toISOString().split('T')[0];
  const memoryEntry = `
## [Auto] ${dateStr}
${dailySummary}

---

`;

  await appendFile(MEMORY_FILE, memoryEntry, 'utf8');
  console.log('Appended to MEMORY.md');

  // Clear prompt file
  await writeFile(PROMPT_FILE, '', 'utf8');
  console.log('=== MEMORY REFINE DONE ===');
}

refine().catch(err => {
  console.error('ERROR:', err);
  process.exit(1);
});

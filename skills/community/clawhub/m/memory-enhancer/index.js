import fs from 'fs';
import path from 'path';

// Helper: get yesterday's date and file path
function getYesterdayInfo() {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yyyy = yesterday.getFullYear();
  const mm = String(yesterday.getMonth() + 1).padStart(2, '0');
  const dd = String(yesterday.getDate()).padStart(2, '0');
  const dateStr = `${yyyy}-${mm}-${dd}`;
  const filePath = path.join('/home/bosunjung/.openclaw/workspace/memory', `${dateStr}.md`);
  return { date: yesterday, dateStr, filePath };
}

// Helper: ensure stats directory exists
function ensureStatsDir() {
  const statsDir = '/home/bosunjung/.openclaw/workspace/memory/stats';
  if (!fs.existsSync(statsDir)) {
    fs.mkdirSync(statsDir, { recursive: true });
  }
  return statsDir;
}

// Main skill entry point
export async function skill(args, context) {
  const { dateStr, filePath } = getYesterdayInfo();
  console.log(`[Memory Enhancer] Processing ${filePath}`);

  if (!fs.existsSync(filePath)) {
    console.log(`[Memory Enhancer] No memory file found for ${dateStr} at ${filePath}`);
    return { status: 'skipped', reason: 'no_yesterday_file' };
  }

  const content = fs.readFileSync(filePath, 'utf-8');

  // Spawn a sub-agent to do the extraction and memory update
  const subAgentPrompt = `
You are a memory extraction assistant. Your task:

1. Read the daily log content below.
2. Extract structured facts into this exact JSON schema:
{
  "preferences": {
    "communication_style": { "tone": "casual|formal|friendly|professional", "formality": "low|medium|high" },
    "topics_of_interest": ["topic1", "topic2", ...]
  },
  "contacts": [
    { "name": "Full Name", "role": "Role/Title", "context": "How they were met or why mentioned" }
  ],
  "habits": {
    "daily_routines": { "morning": "...", "exercise": "...", "meals": "...", "other": "..." },
    "work_patterns": { "focus_hours": "...", "tools_used": [...], "collaboration": "..." }
  },
  "projects": {
    "active_projects": ["project A", "project B"],
    "completed_projects": ["project X"],
    "progress_notes": "Any notable progress or blockers"
  }
}

3. Update the following files in /home/bosunjung/.openclaw/workspace/memory/stats/:
   - preferences.json: merge new preferences, avoiding duplicates
   - contacts.json: append new contacts (avoid exact duplicates by name+role)
   - habits.json: merge routines and work patterns
   - projects.json: merge active/completed lists, update progress notes

4. Append a concise summary to /home/bosunjung/.openclaw/workspace/MEMORY.md in this format:

## ${dateStr} (Memory Extraction)

**Contacts:** comma-separated names (or "None")
**Active Projects:** comma-separated list (or "None")
**Completed Projects:** comma-separated list (or "None")
**Interests:** comma-separated topics (or "None")

---

Be concise. If nothing notable, write "No significant updates."

Daily log content:
"""${content}"""
`;

  try {
    // Spawn sub-agent with tools to read/write memory files
    const subAgentResult = await context.sessions_spawn({
      task: subAgentPrompt,
      model: 'google/gemini-2.5-flash',  // Using Gemini Flash 2.5 as requested
      thinking: 'low',
      timeoutSeconds: 120,
      label: `memory-extraction-${dateStr}`
    });

    const logFilePath = '/home/bosunjung/.openclaw/workspace/memory/logs/skill-execution.log';
    fs.appendFileSync(logFilePath, `[${new Date().toISOString()}] Memory Enhancer (SUCCESS) for ${dateStr}:\n` + JSON.stringify(subAgentResult, null, 2) + '\n\n');
    console.log(`[Memory Enhancer] Sub-agent completed and logged result to ${logFilePath}.`);
    return { status: 'completed', date: dateStr, message: 'Logged to file.' };
  } catch (error) {
    const logFilePath = '/home/bosunjung/.openclaw/workspace/memory/logs/skill-execution.log';
    fs.appendFileSync(logFilePath, `[${new Date().toISOString()}] Memory Enhancer (ERROR) for ${dateStr}:\n` + error.stack + '\n\n');
    console.error('[Memory Enhancer] Sub-agent failed (details logged to file).');
    return { status: 'error', error: error.message };
  }
}
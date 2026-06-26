#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const workspaceRoot = process.argv[2] || '/Users/m1/.openclaw/workspace';
const skillsRoot = path.join(workspaceRoot, 'skills');
const reportPath = path.join(workspaceRoot, '.learnings', 'skill-health-report.json');
const agentsRoot = '/Users/m1/.openclaw/agents';

function walkSkills(dir) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (!entry.isDirectory()) continue;
    const skillMd = path.join(full, 'SKILL.md');
    if (fs.existsSync(skillMd)) {
      results.push(full);
      continue;
    }
    results.push(...walkSkills(full));
  }
  return results;
}

function parseFrontmatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return {};
  const lines = m[1].split('\n');
  const out = {};
  let currentKey = null;
  let currentValue = [];
  let inBlockScalar = false;

  function flush() {
    if (currentKey) {
      out[currentKey] = currentValue.join('\n').trim().replace(/^"|"$/g, '');
      currentKey = null;
      currentValue = [];
    }
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();
    if (!inBlockScalar) {
      const idx = line.indexOf(':');
      if (idx !== -1) {
        flush();
        const key = line.slice(0, idx).trim();
        let value = line.slice(idx + 1).trim();
        if (value === '|' || value.startsWith('| ')) {
          inBlockScalar = true;
          currentKey = key;
          currentValue = [];
        } else {
          currentKey = key;
          currentValue = [value.replace(/^"|"$/g, '')];
        }
      } else if (currentKey && inBlockScalar) {
        currentValue.push(line);
      }
    } else {
      if (line === '' || line.startsWith(' ') || line.startsWith('\t')) {
        currentValue.push(line);
      } else {
        // Block scalar ended (new top-level key without indent)
        flush();
        const idx = line.indexOf(':');
        if (idx !== -1) {
          const key = line.slice(0, idx).trim();
          let value = line.slice(idx + 1).trim();
          if (value === '|' || value.startsWith('| ')) {
            inBlockScalar = true;
            currentKey = key;
            currentValue = [];
          } else {
            currentKey = key;
            currentValue = [value.replace(/^"|"$/g, '')];
            inBlockScalar = false;
          }
        }
      }
    }
  }
  flush();
  return out;
}

function tokenize(text) {
  return String(text || '')
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, ' ')
    .split(/\s+/)
    .filter(Boolean);
}

function similarity(a, b) {
  const sa = new Set(tokenize(a));
  const sb = new Set(tokenize(b));
  if (!sa.size || !sb.size) return 0;
  const inter = [...sa].filter((x) => sb.has(x)).length;
  return inter / Math.min(sa.size, sb.size);
}

function collectSessionFiles(dir) {
  const files = [];
  if (!fs.existsSync(dir)) return files;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...collectSessionFiles(full));
    } else if (full.endsWith('.jsonl')) {
      files.push(full);
    }
  }
  return files;
}

function maybeUpdateUsage(skill, line, mtimeMs) {
  const lower = line.toLowerCase();
  const nameHit = lower.includes(skill.name.toLowerCase());
  const idHit = lower.includes(skill.id.toLowerCase());
  if (nameHit || idHit) {
    skill.useCount += 1;
    if (!skill.lastUsedAt || mtimeMs > skill.lastUsedAtMs) {
      skill.lastUsedAt = new Date(mtimeMs).toISOString();
      skill.lastUsedAtMs = mtimeMs;
    }
  }
}

const skillDirs = walkSkills(skillsRoot);
const systemSkillsRoot = '/Users/m1/.npm-global/lib/node_modules/openclaw/skills';
if (fs.existsSync(systemSkillsRoot)) {
  skillDirs.push(...walkSkills(systemSkillsRoot));
}
const skills = skillDirs.map((dir) => {
  const skillMd = path.join(dir, 'SKILL.md');
  const text = fs.readFileSync(skillMd, 'utf8');
  const fm = parseFrontmatter(text);
  const stat = fs.statSync(skillMd);
  return {
    id: path.basename(dir),
    path: dir,
    name: fm.name || path.basename(dir),
    description: fm.description || '',
    updatedAt: stat.mtime.toISOString(),
    daysSinceUpdate: Math.floor((Date.now() - stat.mtimeMs) / 86400000),
    useCount: 0,
    lastUsedAt: null,
    lastUsedAtMs: 0,
  };
});

const sessionFiles = collectSessionFiles(agentsRoot);
for (const file of sessionFiles) {
  const stat = fs.statSync(file);
  const lines = fs.readFileSync(file, 'utf8').split('\n').slice(-200);
  for (const line of lines) {
    if (!line) continue;
    for (const skill of skills) maybeUpdateUsage(skill, line, stat.mtimeMs);
  }
}

const duplicates = [];
for (let i = 0; i < skills.length; i++) {
  if ((skills[i].description || '').toLowerCase().includes('deprecated')) continue;
  for (let j = i + 1; j < skills.length; j++) {
    if ((skills[j].description || '').toLowerCase().includes('deprecated')) continue;
    const score = similarity(
      `${skills[i].name} ${skills[i].description}`,
      `${skills[j].name} ${skills[j].description}`,
    );
    if (score >= 0.72) {
      duplicates.push({ a: skills[i].id, b: skills[j].id, score: Number(score.toFixed(2)) });
    }
  }
}

const darkSkills = skills
  .filter((skill) => !skill.lastUsedAt && skill.daysSinceUpdate >= 30)
  .map((skill) => ({ id: skill.id, daysSinceUpdate: skill.daysSinceUpdate, reason: 'no_recent_usage_signal' }));

const staleSkills = skills
  .filter((skill) => skill.lastUsedAt && (Date.now() - skill.lastUsedAtMs) / 86400000 >= 60)
  .map((skill) => ({ id: skill.id, lastUsedAt: skill.lastUsedAt, daysSinceLastUse: Math.floor((Date.now() - skill.lastUsedAtMs) / 86400000) }));

const summary = {
  generatedAt: new Date().toISOString(),
  workspaceRoot,
  totalSkills: skills.length,
  sessionFilesScanned: sessionFiles.length,
  duplicatePairs: duplicates.length,
  darkSkills: darkSkills.length,
  staleSkills: staleSkills.length,
  topDuplicatePairs: duplicates.slice(0, 20),
  darkSkillList: darkSkills.slice(0, 50),
  staleSkillList: staleSkills.slice(0, 50),
  recentlyUsedSkills: skills
    .filter((s) => s.lastUsedAt)
    .sort((a, b) => b.lastUsedAtMs - a.lastUsedAtMs)
    .slice(0, 20)
    .map((s) => ({ id: s.id, lastUsedAt: s.lastUsedAt, useCount: s.useCount })),
  skills: skills.map((s) => ({ id: s.id, name: s.name, description: s.description, lastUsedAt: s.lastUsedAt, useCount: s.useCount, daysSinceUpdate: s.daysSinceUpdate })),
  recommendedActions: [
    ...(duplicates.length ? ['Review duplicate skill pairs and merge or disambiguate trigger descriptions.'] : []),
    ...(darkSkills.length ? ['Review dark skills with no recent usage signal and decide keep/archive/delete.'] : []),
    ...(staleSkills.length ? ['Review stale skills that have not been referenced in recent transcripts.'] : []),
  ],
};

fs.mkdirSync(path.dirname(reportPath), { recursive: true });
fs.writeFileSync(reportPath, JSON.stringify(summary, null, 2));
console.log(JSON.stringify(summary, null, 2));

/**
 * Auto Save Memory Hook
 * Session end时自动保存学习要点到记忆系统
 */
const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || '/root/.openclaw/workspace';
const LEARNINGS_DIR = path.join(WORKSPACE, '.learnings');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');

function getLearnings() {
  if (!fs.existsSync(LEARNINGS_DIR)) return [];
  return fs.readdirSync(LEARNINGS_DIR)
    .filter(f => f.endsWith('.md'))
    .map(f => ({
      name: f,
      path: path.join(LEARNINGS_DIR, f),
      mtime: fs.statSync(path.join(LEARNINGS_DIR, f)).mtime
    }))
    .sort((a, b) => b.mtime - a.mtime);
}

async function saveLearnings() {
  const learnings = getLearnings();
  if (learnings.length === 0) return ['No new learnings'];

  const results = [];
  for (const f of learnings.slice(0, 3)) {
    const content = fs.readFileSync(f.path, 'utf-8');
    const destDir = path.join(MEMORY_DIR, 'user', 'events');
    if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });
    const dest = path.join(destDir, `learned-${f.name}`);
    fs.writeFileSync(dest, content);
    results.push(`Saved: ${f.name}`);
  }
  return results;
}

exports.handler = async (event) => {
  try {
    const results = await saveLearnings();
    return { logs: results };
  } catch (err) {
    return { logs: [`Error: ${err.message}`] };
  }
};

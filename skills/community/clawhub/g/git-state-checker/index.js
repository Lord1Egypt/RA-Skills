const { execSync } = require('child_process');

function git(args) {
  try {
    return execSync(`git ${args}`, { encoding: 'utf8', cwd: process.cwd() }).trim();
  } catch { return null; }
}

function getStatus() {
  const status = git('status --short');
  if (!status) return { modified: [], untracked: [], staged: [] };
  const lines = status.split('\n').filter(Boolean);
  return {
    modified: lines.filter(l => l.startsWith(' M') || l.startsWith('M ')).map(l => l.slice(3)),
    untracked: lines.filter(l => l.startsWith('??')).map(l => l.slice(3)),
    staged: lines.filter(l => l.startsWith('A ') || l.startsWith('M ')).map(l => l.slice(3))
  };
}

function getRecentCommits(n = 5) {
  const log = git(`log --oneline -${n}`);
  if (!log) return [];
  return log.split('\n').filter(Boolean);
}

function getStashList() {
  const stash = git('stash list');
  if (!stash) return [];
  return stash.split('\n').filter(Boolean);
}

function report() {
  const status = getStatus();
  const commits = getRecentCommits();
  const stashes = getStashList();

  let lines = ['=== Git State ===', ''];
  
  if (status.modified.length || status.untracked.length || status.staged.length) {
    lines.push('Changes:');
    status.staged.forEach(f => lines.push(`  staged: ${f}`));
    status.modified.forEach(f => lines.push(`  modified: ${f}`));
    status.untracked.forEach(f => lines.push(`  untracked: ${f}`));
  } else {
    lines.push('Working directory: clean');
  }
  
  lines.push('');
  lines.push(`Recent commits (${commits.length}):`);
  commits.forEach(c => lines.push(`  ${c}`));
  
  lines.push('');
  lines.push(`Stash entries: ${stashes.length}`);
  if (stashes.length > 10) lines.push('  ⚠️  Large stash stack — consider cleanup');
  stashes.slice(0, 5).forEach(s => lines.push(`  ${s}`));
  if (stashes.length > 5) lines.push(`  ... and ${stashes.length - 5} more`);

  console.log(lines.join('\n'));
}

if (require.main === module) report();
module.exports = { getStatus, getRecentCommits, getStashList, report };

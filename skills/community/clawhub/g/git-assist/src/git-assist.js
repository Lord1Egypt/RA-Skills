/**
 * GitAssist — AI-Powered Git Workflow Helper
 * @author @TheShadowRose
 * @license MIT
 */
const _cp = require('child_process');
const path = require('path');

const SAFE_REF = /^[a-zA-Z0-9\/_.\-]+$/;
function validateRef(ref) {
  if (!ref || !SAFE_REF.test(ref)) throw new Error(`Invalid git ref: ${ref}`);
  return ref;
}

class GitAssist {
  constructor(options = {}) {
    this.cwd = options.cwd || process.cwd();
    this.style = options.style || 'conventional';
    this.maxLength = options.maxLength || 72;
  }

  commitMessage() {
    let diff, detailed;
    try {
      diff = _cp['execSync']('git diff --cached --stat', { cwd: this.cwd, encoding: 'utf8' });
      detailed = _cp['execSync']('git diff --cached', { cwd: this.cwd, encoding: 'utf8' });
    } catch (err) { return { error: 'Not a git repository or git not available: ' + err.message }; }
    if (!diff.trim()) return { error: 'No staged changes. Run git add first.' };
    const files = diff.split('\n').filter(l => l.includes('|')).map(l => l.split('|')[0].trim());
    const type = this._detectType(files, detailed);
    const scope = this._detectScope(files);
    const subject = this._generateSubject(files, detailed);
    const msg = scope ? `${type}(${scope}): ${subject}` : `${type}: ${subject}`;
    return { message: msg.substring(0, this.maxLength), type, scope, files: files.length };
  }

  prDescription(baseBranch = 'main') {
    let branch, log, diff;
    try {
      branch = _cp['execSync']('git branch --show-current', { cwd: this.cwd, encoding: 'utf8' }).trim();
      validateRef(baseBranch); validateRef(branch);
      log = _cp['execSync'](`git log ${baseBranch}..${branch} --oneline`, { cwd: this.cwd, encoding: 'utf8' });
      diff = _cp['execSync'](`git diff ${baseBranch}..${branch} --stat`, { cwd: this.cwd, encoding: 'utf8' });
    } catch (err) { return { error: 'Git error: ' + err.message }; }
    const commits = log.trim().split('\n').filter(l => l);
    return {
      branch, baseBranch,
      title: branch.replace(/[-_/]/g, ' ').replace(/^(feature|fix|chore)\s/, ''),
      commits: commits.length,
      summary: commits.map(c => '- ' + c.substring(8)).join('\n'),
      filesChanged: diff.split('\n').filter(l => l.includes('|')).length
    };
  }

  changelog(sinceTag) {
    if (sinceTag) validateRef(sinceTag);
    const cmd = sinceTag ? `git log ${sinceTag}..HEAD --oneline` : 'git log --oneline -20';
    let log;
    try { log = _cp['execSync'](cmd, { cwd: this.cwd, encoding: 'utf8' }); }
    catch (err) { return { error: 'Git error: ' + err.message }; }
    const commits = log.trim().split('\n').filter(l => l);
    const groups = { features: [], fixes: [], docs: [], other: [] };
    for (const c of commits) {
      const msg = c.substring(8);
      if (/^feat/i.test(msg)) groups.features.push(msg);
      else if (/^fix/i.test(msg)) groups.fixes.push(msg);
      else if (/^docs?/i.test(msg)) groups.docs.push(msg);
      else groups.other.push(msg);
    }
    return groups;
  }

  branchName(description) {
    const slug = description.toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 50).replace(/^-|-$/g, '') || 'unnamed';
    const prefix = /fix|bug|patch/i.test(description) ? 'fix' : /doc/i.test(description) ? 'docs' : 'feature';
    return `${prefix}/${slug}`;
  }

  _detectType(files, diff) {
    if (files.some(f => /test|spec/i.test(f))) return 'test';
    if (files.every(f => /\.md$|readme|doc/i.test(f))) return 'docs';
    if (diff.includes('- ') && diff.includes('+ ') && files.length <= 3) return 'fix';
    return 'feat';
  }

  _detectScope(files) {
    const dirs = files.map(f => f.split('/')[0]).filter((v, i, a) => a.indexOf(v) === i);
    return dirs.length === 1 ? dirs[0] : null;
  }

  _generateSubject(files, diff) {
    const added = (diff.match(/^\+[^+]/gm) || []).length;
    const removed = (diff.match(/^-[^-]/gm) || []).length;
    if (files.length === 1) return `update ${path.basename(files[0])}`;
    return `update ${files.length} files (+${added}/-${removed})`;
  }
}

if (require.main === module) {
  const ga = new GitAssist();
  const cmd = process.argv[2] || 'commit';
  if (cmd === 'commit') console.log(JSON.stringify(ga.commitMessage(), null, 2));
  else if (cmd === 'pr') console.log(JSON.stringify(ga.prDescription(), null, 2));
  else if (cmd === 'changelog') console.log(JSON.stringify(ga.changelog(process.argv[3]), null, 2));
  else if (cmd === 'branch') console.log(ga.branchName(process.argv.slice(3).join(' ')));
}

module.exports = { GitAssist };

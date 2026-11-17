import fs from 'node:fs';
import path from 'node:path';
import { hashFile, platformForTarget, readJson, requireValue, safeName } from './common.js';
import { verifyFeed } from './feed.js';
export async function verifyEvidence({directory, evidence, targets, version, repo, tag, commit, runId, assets, preferNsis = false}) {
  requireValue(evidence.length === targets.length && new Set(evidence.map(item => item.target)).size === targets.length, 'Missing or duplicate target evidence');
  const expected = new Map();
  const platforms = {};
  for (const item of evidence) {
    requireValue(targets.includes(item.target) && item.version === version && item.tag === tag && item.repo === repo &&
      item.commit === commit && String(item.runId) === String(runId), 'Evidence source or version mismatch');
    requireValue(item.files.length > 0 && item.platforms[platformForTarget(item.target)], 'Incomplete target evidence');
    for (const file of item.files) {
      requireValue(safeName(file.name) && /^[a-f0-9]{64}$/.test(file.sha256), 'Invalid evidence file');
      requireValue(!expected.has(file.name), ("Duplicate build asset " + (file.name)));
      expected.set(file.name, file.sha256);
    }
    for (const [key, entry] of Object.entries(item.platforms)) {
      requireValue(!platforms[key], ("Duplicate updater platform " + (key)));
      platforms[key] = entry;
    }
  }
  const actual = fs.readdirSync(directory).sort();
  requireValue(JSON.stringify(actual) === JSON.stringify([...expected.keys(), 'latest.json'].sort()), 'Draft asset set differs from this build');
  for (const [name, sha256] of expected) requireValue(await hashFile(path.join(directory, name)) === sha256, ("Draft digest mismatch: " + (name)));
  const feed = readJson(path.join(directory, 'latest.json'));
  requireValue(JSON.stringify(Object.keys(feed.platforms).sort()) === JSON.stringify(Object.keys(platforms).sort()), 'Updater platform set differs from build evidence');
  for (const [key, entry] of Object.entries(platforms)) requireValue(JSON.stringify(feed.platforms[key]) === JSON.stringify(entry), ("Updater entry changed: " + (key)));
  const signatures = new Map([...expected.keys()].filter(name => name.endsWith('.sig')).map(name => [name, fs.readFileSync(path.join(directory, name), 'utf8')]));
  verifyFeed(feed, {version, repo, tag, assets, files: new Set(expected.keys()), signatures, preferNsis});
}

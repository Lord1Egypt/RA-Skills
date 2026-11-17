import fs from 'node:fs';
import { hashFile, platformForTarget, requireValue, safeName } from './common.js';
import { resolveAsset, verifyFeed } from './feed.js';
export async function recordEvidence({paths, assets, feed, version, repo, tag, commit, runId, target, preferNsis = false}) {
  requireValue(tag === ("v" + (version)), 'Tag and built app version mismatch');
  const files = [];
  const signatures = new Map();
  const localPaths = new Set(paths.map(file => fs.statSync(file).isDirectory() && file.endsWith('.app') ? file + '.tar.gz' : file));
  for (const file of localPaths) {
    requireValue(fs.statSync(file).isFile(), ("Artifact is not a file: " + (file)));
    const sha256 = await hashFile(file);
    const matches = assets.filter(asset => asset.digest === ("sha256:" + (sha256)));
    requireValue(matches.length === 1 && safeName(matches[0].name), ("Built artifact has no unique matching draft digest: " + (file)));
    const name = matches[0].name;
    requireValue(!files.some(entry => entry.name === name), ("Duplicate artifact " + (name)));
    files.push({name, sha256});
    if (name.endsWith('.sig')) signatures.set(name, fs.readFileSync(file, 'utf8'));
  }
  requireValue(files.length > 0, 'No build artifacts');
  const names = new Set(files.map(file => file.name));
  const platforms = Object.fromEntries(Object.entries(feed.platforms ?? {}).filter(([, entry]) => names.has(resolveAsset(entry.url, {repo, tag, assets}))));
  verifyFeed({...feed, platforms}, {version, repo, tag, assets, files: names, signatures, preferNsis});
  const platform = platformForTarget(target);
  requireValue(platforms[platform], ("Build evidence missing " + (platform)));
  return {version, tag, repo, commit, runId, target, files, platforms};
}

import fs from 'node:fs';
import path from 'node:path';
import { hashFile, readJson, requireValue, safeName } from './common.js';
import { verifyFeed } from './feed.js';
// Shared by direct-release verification and central winget consumers. No network writes.
export function releaseReady(release, {tag, requiredAssets, allowPrerelease = false, expectedDraft = false}) {
  requireValue(release.tag_name === tag && release.draft === expectedDraft && (allowPrerelease || release.prerelease === false) &&
    (allowPrerelease || /^v\d+\.\d+\.\d+$/.test(tag)), expectedDraft ? 'Expected an unpublished draft release' : 'Expected the public stable release');
  requireValue(Array.isArray(requiredAssets) && requiredAssets.length > 0, 'Required asset inventory is empty');
  const assets = release.assets ?? [];
  requireValue(new Set(assets.map(asset => asset.name)).size === assets.length, 'Duplicate release asset');
  for (const name of requiredAssets) {
    requireValue(safeName(name), 'Unsafe required asset name');
    const asset = assets.find(asset => asset.name === name);
    requireValue(asset && /^sha256:[a-f0-9]{64}$/i.test(asset.digest ?? ''), ("Missing required asset or digest: " + (name)));
  }
  return assets;
}

async function verifyReleaseAssets({directory, release, requiredAssets, platforms, version, repo, tag}, expectedDraft) {
  requireValue(tag === ("v" + (version)), 'Tag and app version mismatch');
  requireValue(release.prerelease === version.includes('-'), 'Release channel mismatch');
  const assets = releaseReady(release, {tag, requiredAssets, allowPrerelease: version.includes('-'), expectedDraft});
  const payloads = assets.filter(asset => !/^SHA256SUMS(?:\.txt)?$/.test(asset.name));
  requireValue(payloads.length > 0, 'No release payloads');
  const names = new Set();
  for (const asset of payloads) {
    requireValue(safeName(asset.name) && /^sha256:[a-f0-9]{64}$/i.test(asset.digest ?? ''), ("Invalid asset or digest: " + (asset.name)));
    const local = path.join(directory, asset.name);
    requireValue(fs.existsSync(local) && fs.lstatSync(local).isFile(), ("Missing local asset: " + (asset.name)));
    requireValue(await hashFile(local) === asset.digest.slice(7).toLowerCase(), ("Release digest mismatch: " + (asset.name)));
    names.add(asset.name);
  }
  const feed = readJson(path.join(directory, 'latest.json'));
  requireValue(Array.isArray(platforms) && platforms.length > 0, 'Required updater platforms are empty');
  for (const platform of platforms) requireValue(feed.platforms?.[platform], ("Missing updater target: " + (platform)));
  const signatures = new Map([...names].filter(name => name.endsWith('.sig')).map(name => [name, fs.readFileSync(path.join(directory, name), 'utf8')]));
  verifyFeed(feed, {version, repo, tag, assets, files: names, signatures, preferNsis: true});
  // The checksum from a previous run is deliberately excluded from its replacement.
  return payloads.sort((a, b) => a.name.localeCompare(b.name, 'en')).map(asset => ("" + (asset.digest.slice(7).toLowerCase()) + "  " + (asset.name) + "\n")).join('');
}

export const verifyPublicRelease = options => verifyReleaseAssets(options, false);
export const verifyDraftRelease = options => verifyReleaseAssets(options, true);

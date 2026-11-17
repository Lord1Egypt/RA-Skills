import fs from 'node:fs';
import path from 'node:path';
import { readJson, requireValue, safeName } from './common.js';
import { releaseReady, verifyDraftRelease, verifyPublicRelease } from './release.js';
import { recordEvidence } from './record.js';
import { verifyEvidence } from './verify.js';
export async function main() {
  const env = process.env;
  if (process.argv[2] === 'ready') {
    const contract = readJson(process.argv[4]);
    releaseReady(readJson(process.argv[3]), {tag: contract.tag, requiredAssets: contract.requiredAssets});
    return;
  }
  if (['verify-release', 'verify-draft'].includes(process.argv[2])) {
    const verify = process.argv[2] === 'verify-draft' ? verifyDraftRelease : verifyPublicRelease;
    const checksums = await verify({directory: 'dist', release: readJson(path.join(env.RUNNER_TEMP, 'release.json')),
      requiredAssets: ['latest.json'], platforms: env.PLATFORMS?.split(' '), version: env.APP_VERSION, repo: env.REPO, tag: env.TAG});
    fs.writeFileSync('dist/SHA256SUMS', checksums);
    return;
  }
  const common = {version: env.APP_VERSION, tag: env.TAG, repo: env.REPO, commit: env.SOURCE_COMMIT, runId: env.GITHUB_RUN_ID, preferNsis: env.PREFER_NSIS === 'true'};
  requireValue(/^[a-f0-9]{40}$/i.test(common.commit ?? '') && /^\d+$/.test(common.runId ?? ''), 'Missing build source identity');
  const assets = readJson(path.join(env.RUNNER_TEMP, 'draft-assets.json')).flat();
  if (process.argv[2] === 'record') {
    const evidence = await recordEvidence({...common, assets, paths: [...JSON.parse(env.ARTIFACT_PATHS), ...JSON.parse(env.EXTRA_ARTIFACTS || '[]')],
      target: env.TARGET, feed: readJson(path.join(env.RUNNER_TEMP, 'build-feed.json'))});
    requireValue(safeName(env.TARGET), 'Invalid target');
    fs.mkdirSync('release-evidence', {recursive: true});
    fs.writeFileSync(path.join('release-evidence', env.TARGET + '.json'), JSON.stringify(evidence) + '\n');
  } else if (process.argv[2] === 'verify') {
    // SHA256SUMS is regenerated after verification; it is not a build payload.
    fs.rmSync(path.join('dist', 'SHA256SUMS'), {force: true});
    const evidence = fs.readdirSync('release-evidence').filter(file => file.endsWith('.json')).map(file => readJson(path.join('release-evidence', file)));
    await verifyEvidence({...common, assets, directory: 'dist', evidence, targets: env.TARGETS.split(' ')});
  } else throw new Error('Usage: release-assets.mjs record|verify');
}

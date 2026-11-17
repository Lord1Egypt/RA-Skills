// Copy to .github/scripts/release-assets.mjs with the release-assets directory.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { main } from './release-assets/cli.js';
export { hashFile } from './release-assets/common.js';
export { resolveAsset, verifyFeed } from './release-assets/feed.js';
export { recordEvidence } from './release-assets/record.js';
export { verifyEvidence } from './release-assets/verify.js';
export { releaseReady, verifyDraftRelease, verifyPublicRelease } from './release-assets/release.js';

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => { console.error(('release-assets: ' + error.message)); process.exitCode = 1; });
}

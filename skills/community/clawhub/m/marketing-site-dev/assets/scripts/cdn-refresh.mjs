#!/usr/bin/env node
/**
 * CDN cache invalidation via signed Volcengine API call.
 * No `ve` CLI dependency — works in CI runners.
 */
import { callVolc } from './lib/volc-api.mjs';
import config from '../deploy.config.mjs';

const domains = config.cdnDomains ?? [];
if (domains.length === 0) {
  console.log('[cdn] deploy.config.mjs has no cdnDomains, skipping');
  process.exit(0);
}

const urls = domains.map((d) => `https://${d}/`).join('\n');
console.log('[cdn] submitting directory refresh:');
domains.forEach((d) => console.log(`  - https://${d}/`));

const r = await callVolc({
  service: 'cdn',
  region: 'cn-beijing',
  action: 'SubmitRefreshTask',
  version: '2021-03-01',
  body: { Type: 'dir', Urls: urls },
});

const err = r.ResponseMetadata?.Error;
if (err) {
  console.error(`[cdn] FAILED: ${err.Code}: ${err.Message}`);
  process.exit(1);
}

console.log(`[cdn] ✓ task submitted: ${r.Result?.TaskID ?? '(no id)'}`);

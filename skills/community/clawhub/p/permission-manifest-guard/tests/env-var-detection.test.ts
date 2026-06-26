import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { extractJsEnvVars, classifySecret } from '../src/extract.js';

describe('extractEnvVars – env var detection', () => {
  // ── 1. process.env access (dot + bracket notation) ──────────────────
  it('detects process.env in dot notation and bracket notation', () => {
    const source = [
      "const port = process.env.PORT;",
      "const host = process.env['HOSTNAME'];",
      'const db = process.env["DATABASE_URL"];',
    ].join('\n');

    const vars = extractJsEnvVars(source, 'src/config.ts');
    const names = vars.map(v => v.name);

    assert.deepEqual(names, ['PORT', 'HOSTNAME', 'DATABASE_URL']);
    assert.equal(vars[0]!.accessMethod, 'process.env');
    assert.equal(vars[0]!.isSecret, false, 'PORT is safe');
    assert.equal(vars[1]!.isSecret, false, 'HOSTNAME is safe');
    assert.equal(vars[2]!.isSecret, false, 'DATABASE_URL has no secret pattern');
    assert.equal(vars[0]!.line, 1);
    assert.equal(vars[2]!.line, 3);
  });

  // ── 2. dotenv config with referenced vars ───────────────────────────
  it('detects env vars referenced after dotenv.config()', () => {
    const source = [
      "require('dotenv').config();",
      "const key = process.env.STRIPE_SECRET_KEY;",
      "const region = process.env.AWS_REGION;",
    ].join('\n');

    const vars = extractJsEnvVars(source, 'src/init.ts');
    const names = vars.map(v => v.name);

    assert.deepEqual(names, ['STRIPE_SECRET_KEY', 'AWS_REGION']);
    assert.equal(vars[0]!.isSecret, true, 'STRIPE_SECRET_KEY ends with _KEY');
    assert.equal(vars[1]!.isSecret, false, 'AWS_REGION is not a secret');
  });

  // ── 3. Secret true positive: suffix patterns ────────────────────────
  it('flags DB_PASSWORD and REDIS_CREDENTIAL as secrets', () => {
    assert.equal(classifySecret('DB_PASSWORD'), true, '_PASSWORD suffix');
    assert.equal(classifySecret('REDIS_CREDENTIAL'), true, '_CREDENTIAL suffix');
    assert.equal(classifySecret('SESSION_SECRET'), true, '_SECRET suffix');
    assert.equal(classifySecret('REFRESH_TOKEN'), true, '_TOKEN suffix');
  });

  // ── 4. Secret true positive: prefix patterns ────────────────────────
  it('flags API_* and AUTH_* prefixed vars as secrets', () => {
    assert.equal(classifySecret('API_KEY'), true, 'API_ prefix + _KEY suffix');
    assert.equal(classifySecret('API_GATEWAY_URL'), true, 'API_ prefix');
    assert.equal(classifySecret('AUTH_COOKIE'), true, 'AUTH_ prefix');
    assert.equal(classifySecret('AUTH_REDIRECT_URI'), true, 'AUTH_ prefix');
  });

  // ── 5. Secret true negative: not-a-secret despite suspicious substrings
  it('does not flag safe vars or non-secret names', () => {
    assert.equal(classifySecret('BUCKET_NAME'), false, 'no secret pattern');
    assert.equal(classifySecret('LOG_LEVEL'), false, 'safe var LOG_LEVEL');
    assert.equal(classifySecret('NODE_ENV'), false, 'safe var NODE_ENV');
    assert.equal(classifySecret('MAX_RETRY_COUNT'), false, 'no secret pattern');
    assert.equal(classifySecret('FEATURE_FLAG_ENABLED'), false, 'no secret pattern');
  });

  // ── 6. Secret edge cases: ambiguous naming ──────────────────────────
  it('handles edge-case names like GITHUB_PAT and AUTH_TOKEN_EXPIRY', () => {
    // GITHUB_PAT does not match any suffix/prefix/substring — should NOT flag
    assert.equal(classifySecret('GITHUB_PAT'), false, 'PAT is not a recognized pattern');
    // AUTH_TOKEN_EXPIRY starts with AUTH_ — should flag despite _EXPIRY suffix
    assert.equal(classifySecret('AUTH_TOKEN_EXPIRY'), true, 'AUTH_ prefix triggers');
    // TOKEN_EXPIRY_SECONDS contains "token" substring — should flag
    assert.equal(classifySecret('TOKEN_EXPIRY_SECONDS'), true, 'contains "token"');
    // ENCRYPTION_KEY ends with _KEY — should flag
    assert.equal(classifySecret('ENCRYPTION_KEY'), true, '_KEY suffix');
    // KEY_COUNT — does not end with _KEY, no matching pattern
    assert.equal(classifySecret('KEY_COUNT'), false, 'KEY as prefix is not a pattern');
  });
});

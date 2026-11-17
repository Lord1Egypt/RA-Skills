import { randomBytes } from 'node:crypto';
import { join } from 'node:path';
import { openSync, closeSync, fsyncSync } from 'node:fs';
import { readPrivateJson, readPrivateSecret, writeSecretNoClobber, writeJsonNoClobber, replacePrivateJson,
  canonicalOperatorOrigin } from '../../../../services/correspondence/bin/safe-io.mjs';
import { CorrespondenceClient } from '../../../correspondence/client.mjs';
import { readBoundedJson } from '../../../correspondence/response.mjs';
import { BASE, SCHEMA, grantToken, validateAttempt, need, exact } from './contract.mjs';

function syncDirectory(dir) { const fd = openSync(dir, 'r'); try { fsyncSync(fd); } finally { closeSync(fd); } }
export async function entryRequest(baseUrl, path, { body, proof, fetchImpl = globalThis.fetch } = {}) {
  const base = canonicalOperatorOrigin(baseUrl), url = `${base}${BASE}${path}`;
  const controller = new AbortController(); const timer = setTimeout(() => controller.abort(), 10000);
  try {
    const response = await fetchImpl(url, { method: body ? 'POST' : 'GET', redirect: 'manual', signal: controller.signal,
      headers: { accept: 'application/json', ...(proof ? { authorization: `Bearer ${proof}` } : {}),
        ...(body ? { 'content-type': 'application/json', 'idempotency-key': body.requestId } : {}) },
      ...(body ? { body: JSON.stringify(body) } : {}) });
    need(!response.redirected && !(response.status >= 300 && response.status < 400) && (!response.url || response.url === url), 503, 'outcome_unknown', 'reconcile_same_attempt');
    return { status: response.status, body: await readBoundedJson(response, 32768, controller.signal) };
  } finally { clearTimeout(timer); controller.abort(); }
}
export function prepare(directory, baseUrl, profileId, termsHash) {
  const base = canonicalOperatorOrigin(baseUrl);
  const old = readPrivateJson(join(directory, 'attempt.json'));
  if (old) {
    need(old.baseUrl === base && old.body.profileId === profileId && old.body.termsHash === termsHash, 409, 'local_attempt_mismatch');
    return old;
  }
  // Secret is durable before attempt, and both are durable before any mutation.
  // A crash between writes reuses the first secret on the next prepare.
  let proof;
  try { proof = readPrivateSecret(join(directory, 'registration.secret')); }
  catch (e) { if (e.code !== 'ENOENT') throw e; proof = randomBytes(32).toString('base64url'); writeSecretNoClobber(join(directory, 'registration.secret'), proof); }
  const body = { schema: SCHEMA, requestId: randomBytes(24).toString('base64url'), profileId, termsHash };
  validateAttempt(body, body.requestId, proof);
  const attempt = { schema: SCHEMA, baseUrl: base, body };
  writeJsonNoClobber(join(directory, 'attempt.json'), attempt); syncDirectory(directory);
  return attempt;
}
export async function continueEntry(directory, action = 'reconcile', transport) {
  need(['register', 'reconcile', 'renew'].includes(action), 400, 'invalid_action');
  const attempt = readPrivateJson(join(directory, 'attempt.json'));
  need(attempt, 400, 'local_attempt_required');
  const proof = readPrivateSecret(join(directory, 'registration.secret'));
  validateAttempt(attempt.body, attempt.body.requestId, proof);
  const result = await entryRequest(attempt.baseUrl, `/${action}`, { body: attempt.body, proof, fetchImpl: transport });
  if ([200, 202].includes(result.status)) {
    const x = result.body;
    exact(x, ['schema', 'status', 'requestId', 'profileId', 'termsHash', 'registrationId', 'projectId', 'workspaceExpiresAt', 'receiver', 'nextAction', 'grants']);
    exact(x.receiver, ['state']); exact(x.grants, ['reader', 'writer']);
    for (const role of ['reader', 'writer']) exact(x.grants[role], ['role', 'token', 'expiresAt']);
    need(['ready', 'partial'].includes(x.status) && ['disabled', 'pending', 'unknown', 'ready', 'declined'].includes(x.receiver.state) &&
      ['use_private_correspondence', 'reconcile_same_attempt'].includes(x.nextAction) &&
      [x.workspaceExpiresAt, x.grants.reader.expiresAt, x.grants.writer.expiresAt].every(s => typeof s === 'string' && /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/.test(s)),
    503, 'invalid_entry_response', 'reconcile_same_attempt');
    need(result.status === 202
      ? x.status === 'partial' && ['pending', 'unknown'].includes(x.receiver.state) && x.nextAction === 'reconcile_same_attempt'
      : x.status === 'ready' && ['disabled', 'ready', 'declined'].includes(x.receiver.state) && x.nextAction === 'use_private_correspondence',
    503, 'invalid_entry_response', 'reconcile_same_attempt');
    need(x.schema === SCHEMA && x.requestId === attempt.body.requestId && x.profileId === attempt.body.profileId && x.termsHash === attempt.body.termsHash &&
      /^ven_[\w-]{16}$/.test(x.registrationId) && /^prj_[\w-]{16}$/.test(x.projectId) &&
      ['reader', 'writer'].every(role => x.grants?.[role]?.role === role && x.grants[role].token === grantToken(proof, x.registrationId, role)),
    503, 'invalid_entry_response', 'reconcile_same_attempt');
    const prior = readPrivateJson(join(directory, 'continuation.json'));
    need(!prior || prior.requestId === x.requestId && prior.registrationId === x.registrationId && prior.projectId === x.projectId
      && prior.profileId === x.profileId && prior.termsHash === x.termsHash, 503, 'invalid_entry_response', 'reconcile_same_attempt');
    // Tokens are reconstructed from the private proof only when used. No bearer
    // credential is persisted in the continuation or printed by the CLI.
    const { grants, ...safe } = x;
    const receipt = { ...safe, grants: Object.fromEntries(Object.entries(grants).map(([role, g]) => [role, { role, expiresAt: g.expiresAt }])) };
    replacePrivateJson(join(directory, 'continuation.json'), receipt); syncDirectory(directory);
    return { status: result.status, body: receipt };
  }
  // Refusal codes are an allowlisted shape; never reflect server prose or request.
  return { status: result.status, body: { error: {
    code: typeof result.body?.error?.code==='string' && /^[a-z_]{1,80}$/.test(result.body.error.code) ? result.body.error.code : 'entry_refused',
    nextAction: typeof result.body?.error?.nextAction==='string' && /^[a-z_]{1,80}$/.test(result.body.error.nextAction) ? result.body.error.nextAction : 'reconcile_same_attempt' } } };
}
export function resumedCorrespondence(directory, role = 'writer') {
  need(['reader', 'writer'].includes(role), 400, 'invalid_role');
  const attempt = readPrivateJson(join(directory, 'attempt.json'));
  const receipt = readPrivateJson(join(directory, 'continuation.json'));
  const proof = readPrivateSecret(join(directory, 'registration.secret'));
  need(receipt && receipt.requestId === attempt.body.requestId, 400, 'continuation_required');
  return { projectId: receipt.projectId, client: new CorrespondenceClient({ baseUrl: attempt.baseUrl,
    token: grantToken(proof, receipt.registrationId, role), fetch: globalThis.fetch }) };
}
export async function writeCheckpoint(directory, text) {
  const { client, projectId } = resumedCorrespondence(directory);
  const file = join(directory, 'event-intent.json');
  let intent = readPrivateJson(file);
  if (!intent) { intent = { projectId, kind: 'request', text, idempotencyKey: randomBytes(24).toString('base64url') };
    writeJsonNoClobber(file, intent); syncDirectory(directory); }
  need(intent.text === text && intent.projectId === projectId, 409, 'event_intent_mismatch');
  try { const result = await client.postEvent(intent); return { eventId: result.event.id, sequence: result.event.sequence, replayed: result.replayed }; }
  finally { client.dispose(); }
}
export async function resume(directory) {
  const { client, projectId } = resumedCorrespondence(directory, 'reader');
  try { const r = await client.listEvents({ projectId, limit: 100 });
    return { projectId, eventCount: r.events.length, eventIds: r.events.map(e => e.id), nextCursor: r.nextCursor }; }
  finally { client.dispose(); }
}

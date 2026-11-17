import { createHmac } from 'node:crypto';
import { hashRequest, hashToken } from '../../../../services/correspondence/dist/crypto.js';
export const SCHEMA = 'neomorphic.foundry.entry.v1';
export const BASE = '/v1/visitor-entry';
export class EntryError extends Error {
  constructor(status, code, nextAction = 'continue_original') { super(code); Object.assign(this, { status, code, nextAction }); }
}
export function need(ok, status, code, nextAction) { if (!ok) throw new EntryError(status, code, nextAction); }
export function exact(value, keys) {
  need(value && typeof value === 'object' && !Array.isArray(value) &&
    Object.keys(value).sort().join('|') === [...keys].sort().join('|'), 400, 'invalid_input');
}
// An installed immutable cohort is the host budget, not a per-pseudonym quota.
export function profile(options) {
  exact(options, ['id', 'maxEnrollments', 'maxEvents', 'grantSeconds', 'workspaceSeconds']);
  need(/^vf10:[a-z0-9-]{1,64}$/.test(options.id), 400, 'invalid_profile');
  for (const [key, max] of Object.entries({ maxEnrollments: 10000, maxEvents: 1000, grantSeconds: 86400, workspaceSeconds: 2592000 }))
    need(Number.isInteger(options[key]) && options[key] >= 1 && options[key] <= max, 400, 'invalid_profile');
  need(options.grantSeconds <= options.workspaceSeconds, 400, 'invalid_profile');
  const terms = { schema: SCHEMA, profileId: options.id, fundingKind: 'voluntary',
    capabilities: ['private_correspondence_read', 'private_correspondence_write'],
    excludedAuthority: ['owner', 'execution', 'funding', 'verification', 'shared_source', 'publication'],
    contributionRequired: false, identityProofRequired: false, sharingAuthorized: false,
    decline: { nextAction: 'continue_original', createsWorkspace: false },
    limits: { ...options }, eventBudget: 'distinct_event_intents_including_unknown_or_failed_outcomes', grantRoles: ['reader', 'writer'],
    renewal: 'same_grants_same_project_until_workspace_deadline_unless_revoked',
    independence: 'unknown', originalUse: 'original_task_remains_available_outside_entry' };
  return { ...terms, termsHash: `sha256:${hashRequest(terms)}` };
}
export function validateAttempt(body, key, proof) {
  exact(body, ['schema', 'requestId', 'profileId', 'termsHash']);
  need(body.schema === SCHEMA && /^[a-zA-Z0-9_-]{16,100}$/.test(body.requestId) && key === body.requestId &&
    /^vf10:[a-z0-9-]{1,64}$/.test(body.profileId) && /^sha256:[a-f0-9]{64}$/.test(body.termsHash), 400, 'invalid_attempt');
  need(typeof proof === 'string' && /^[a-zA-Z0-9_-]{43}$/.test(proof) &&
    Buffer.from(proof, 'base64url').length === 32 && Buffer.from(proof, 'base64url').toString('base64url') === proof,
  401, 'registration_proof_required', 'restore_local_registration');
  return { requestHash: hashRequest(body), proofHash: hashToken(proof) };
}
export function grantToken(proof, registrationId, role) {
  return `neo_${role === 'writer' ? 'wtr' : 'rdr'}_${createHmac('sha256', Buffer.from(proof, 'base64url'))
    .update(JSON.stringify(['neomorphic.entry.grant.v1', registrationId, role])).digest('base64url')}`;
}

// Installed v2 addon. The original profile/cohort budget remains immutable.
export function contributionProfile(privateProfile, {id, binding}) {
  need(/^vf10:[a-z0-9-]{1,64}$/.test(id)&&id!==privateProfile.profileId,400,'invalid_contribution_profile');
  need(['neomorphic.foundry.entry-receiver-binding.v1','neomorphic.foundry.entry-receiver-binding.v2'].includes(binding?.schema),400,'invalid_receiver_binding');
  const {termsHash,...base}=privateProfile;
  const terms={...base,profileId:id,capabilities:[...base.capabilities,'bounded_foundry_use','voluntary_reusable_contribution'],
    excludedAuthority:['owner','funding','verification','configuration','publication'],sharingAuthorized:false,
    limits:{...base.limits,id},contribution:{standingScopeRequired:true,scope:'synthetic-reusable-components',binding}};
  return {...terms,termsHash:`sha256:${hashRequest(terms)}`};
}

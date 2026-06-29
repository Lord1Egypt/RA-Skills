#!/usr/bin/env node
'use strict';

const fs = require('fs');
const {
  normalizeCompanySearchPayload,
  SUPPORTED_COMPANY_SEARCH_FIELDS
} = require('./lib/company-search-payloads');
const { parseJson, readJsonFile } = require('./lib/okki-api');

const MUTABLE_ALIAS_VALUES = new Set(['latest', 'current', 'previous', 'above', 'recommended', 'these', 'those']);
const OUTPUT_CONTRACT_BY_ACTION = {
  company_discovery: 'company_discovery_table',
  prepare_unlock: 'unlock_plan_summary',
  unlock_companies: 'unlock_details',
  contact_search: 'contact_rows',
  draft_email: 'email_draft',
  send_email: 'email_send_summary',
  status_check: 'email_status_rows',
  profile_update: 'profile_update_summary',
  balance: 'balance_summary'
};
const PAID_ACTIONS = new Set(['unlock_companies', 'contact_search']);
const SEND_ACTIONS = new Set(['send_email']);
const WRITE_ACTIONS = new Set(['profile_update']);
const CONTACT_FIELDS = new Set([
  'name',
  'contact_match',
  'title',
  'title_type',
  'company_name',
  'working_company',
  'description',
  'primary_industry_name',
  'country_codes',
  'industry_codes',
  'has_email',
  'has_phone',
  'has_linkedin',
  'has_facebook',
  'has_company_name',
  'employees_min',
  'employees_max',
  'size',
  'page'
]);
const MAX_CONTACT_SIZE = 100;

function usage() {
  console.error([
    'Usage:',
    '  node scripts/okki-envelope.js validate --file envelope.json --compact',
    '  node scripts/okki-envelope.js validate --json \'<envelope>\' --compact'
  ].join('\n'));
}

function parseArgs(argv) {
  if (argv.length === 0 || argv[0] === '--help' || argv[0] === '-h') {
    usage();
    process.exit(0);
  }
  const args = {
    command: argv[0],
    file: null,
    json: null,
    compact: false
  };
  for (let i = 1; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--file') {
      args.file = argv[++i];
    } else if (arg === '--json') {
      args.json = argv[++i];
    } else if (arg === '--compact') {
      args.compact = true;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else {
      throw validationError('ENVELOPE_USAGE_ERROR', `Unknown argument: ${arg}`, 'Use validate with --file or --json.');
    }
  }
  if (args.command !== 'validate') {
    throw validationError('ENVELOPE_USAGE_ERROR', 'Command must be validate.', 'Run okki-envelope.js validate --file envelope.json --compact.');
  }
  if ((args.file ? 1 : 0) + (args.json ? 1 : 0) !== 1) {
    throw validationError('ENVELOPE_USAGE_ERROR', 'Provide exactly one of --file or --json.', 'Pass one envelope source.');
  }
  return args;
}

function readEnvelope(args) {
  if (args.file) return readJsonFile(args.file);
  return parseJson(args.json, '--json');
}

function validateEnvelope(envelope) {
  assertPlainObject(envelope, 'Envelope');
  assertEqual(envelope.envelope_version, '1.0', 'ENVELOPE_VERSION_UNSUPPORTED', 'envelope_version must be "1.0".');

  const action = cleanString(envelope.action);
  if (!Object.hasOwn(OUTPUT_CONTRACT_BY_ACTION, action)) {
    throw validationError('ENVELOPE_ACTION_UNSUPPORTED', 'Unsupported action.', 'Build an envelope for a supported OKKI Go action.');
  }

  const outputContract = cleanString(envelope.output_contract);
  if (outputContract !== OUTPUT_CONTRACT_BY_ACTION[action]) {
    throw validationError('ENVELOPE_OUTPUT_CONTRACT_INVALID', 'output_contract does not match action.', 'Use the output contract owned by the target wrapper.');
  }

  if (!Array.isArray(envelope.source_refs) || envelope.source_refs.length === 0) {
    throw validationError('ENVELOPE_SOURCE_REFS_REQUIRED', 'source_refs must include at least one source.', 'Attach a digest, selection handle, plan, or current user request source.');
  }
  for (const ref of envelope.source_refs) validateSourceRef(ref);

  if (!cleanString(envelope.scope_summary)) {
    throw validationError('ENVELOPE_SCOPE_REQUIRED', 'scope_summary is required.', 'Summarize the exact current action scope.');
  }
  assertPlainObject(envelope.inputs, 'inputs');
  assertConfirmation(envelope.confirmation);
  assertNotExpired(envelope.expires_at);

  if ((PAID_ACTIONS.has(action) || SEND_ACTIONS.has(action) || WRITE_ACTIONS.has(action)) && hasMutableAlias(envelope)) {
    throw validationError('ENVELOPE_MUTABLE_ALIAS_FORBIDDEN', 'Mutable aliases cannot authorize paid/send/write actions.', 'Replace aliases with a frozen plan, mapping file, or confirmed content reference.');
  }

  validateActionInputs(action, envelope);
  validateConfirmationScope(action, envelope);

  return {
    ok: true,
    action,
    output_contract: outputContract,
    paid_api_allowed: PAID_ACTIONS.has(action),
    send_allowed: SEND_ACTIONS.has(action),
    write_allowed: WRITE_ACTIONS.has(action),
    recovery_suggestion: null
  };
}

function validateActionInputs(action, envelope) {
  const inputs = envelope.inputs;
  if (action === 'company_discovery') {
    validateCompanyDiscoveryInputs(inputs);
  } else if (action === 'prepare_unlock') {
    validatePrepareUnlockInputs(inputs);
  } else if (action === 'unlock_companies') {
    validateUnlockInputs(inputs);
  } else if (action === 'contact_search') {
    validateContactInputs(inputs);
  } else if (action === 'draft_email') {
    requireInput(inputs, 'recipient_refs', 'ENVELOPE_RECIPIENTS_REQUIRED', 'Add recipient or source references for the draft.');
    requireInput(inputs, 'offer_facts_ref', 'ENVELOPE_OFFER_FACTS_REQUIRED', 'Add sourced offer facts for the draft.');
  } else if (action === 'send_email') {
    requireInput(inputs, 'recipients_ref', 'ENVELOPE_RECIPIENTS_REQUIRED', 'Freeze recipients into a mapping file or recipient digest.');
    requireInput(inputs, 'content_ref', 'ENVELOPE_CONTENT_REQUIRED', 'Freeze final content before send confirmation.');
  } else if (action === 'profile_update') {
    requireInput(inputs, 'candidate_fields', 'ENVELOPE_PROFILE_FIELDS_REQUIRED', 'Provide source-labeled candidate fields.');
    validateProfileCandidateFields(inputs.candidate_fields);
  } else if (action === 'status_check') {
    if (!('task_id' in inputs) && !('mail_id' in inputs) && !('status_filter' in inputs) && !('page' in inputs)) {
      throw validationError('ENVELOPE_STATUS_SCOPE_REQUIRED', 'Status check scope is missing.', 'Provide a task id, mail id, status filter, or page scope.');
    }
  }
}

function validateCompanyDiscoveryInputs(inputs) {
  if (inputs.batch_plan_ref) return;
  const payload = inputs.search_payload;
  if (!payload) {
    throw validationError('ENVELOPE_SEARCH_PAYLOAD_REQUIRED', 'company_discovery requires search_payload or batch_plan_ref.', 'Build a supported search payload first.');
  }
  normalizeCompanySearchPayload(payload, { supportedFields: SUPPORTED_COMPANY_SEARCH_FIELDS });
}

function validatePrepareUnlockInputs(inputs) {
  const hasSelection = cleanString(inputs.selection_handle) && cleanString(inputs.rows);
  const hasSelectionSet = hasReadablePath(inputs.selection_set_file);
  if (!hasSelection && !hasSelectionSet) {
    throw validationError('ENVELOPE_UNLOCK_SELECTION_REQUIRED', 'prepare_unlock requires selection_handle + rows or selection_set_file.', 'Select rows from a current script-owned table.');
  }
  rejectRawTargetAuthority(inputs);
}

function validateUnlockInputs(inputs) {
  const planId = cleanString(inputs.unlock_plan_id);
  if (!/^uplan_[a-f0-9]{24}$/.test(planId)) {
    throw validationError('ENVELOPE_UNLOCK_PLAN_REQUIRED', 'unlock_companies requires a frozen unlock_plan_id.', 'Run prepare-unlock-plan.js and confirm that exact target set.');
  }
  rejectRawTargetAuthority(inputs);
}

function validateContactInputs(inputs) {
  const payload = inputs.contact_payload;
  assertPlainObject(payload, 'contact_payload');
  const unsupported = Object.keys(payload).filter((key) => !CONTACT_FIELDS.has(key));
  if (unsupported.length > 0) {
    throw validationError('ENVELOPE_UNSUPPORTED_INPUT_FIELD', `Unsupported contact fields: ${unsupported.join(', ')}`, 'Remove unsupported fields before contact search.');
  }
  if (payload.size !== undefined) {
    const size = Number(payload.size);
    if (!Number.isInteger(size) || size < 1 || size > MAX_CONTACT_SIZE) {
      throw validationError('ENVELOPE_CONTACT_SIZE_INVALID', 'contact_payload.size must be between 1 and 100.', 'Reduce the contact search size.');
    }
  }
}

function validateConfirmationScope(action, envelope) {
  const confirmation = envelope.confirmation;
  if (!requiresConfirmation(action)) {
    if (confirmation.required !== false || confirmation.status !== 'not_required') {
      throw validationError('ENVELOPE_CONFIRMATION_INVALID', 'This action should mark confirmation as not_required.', 'Use not_required for free/non-writing actions.');
    }
    return;
  }
  if (confirmation.required !== true || confirmation.status !== 'confirmed') {
    throw validationError('ENVELOPE_CONFIRMATION_REQUIRED', 'Explicit confirmation is required for this action.', 'Ask the user to confirm the exact paid/send/write scope.');
  }
  assertPlainObject(confirmation.confirmed_scope, 'confirmed_scope');

  if (action === 'unlock_companies') {
    const current = cleanString(envelope.inputs.target_set_fingerprint);
    const confirmed = cleanString(confirmation.confirmed_scope.target_set_fingerprint);
    if (!confirmed) {
      throw validationError('ENVELOPE_CONFIRMATION_MISSING_TARGET', 'Unlock confirmation must include target_set_fingerprint.', 'Prepare the unlock plan and confirm the exact target set.');
    }
    if (current && current !== confirmed) {
      throw validationError('ENVELOPE_TARGET_CHANGED', 'Confirmed target fingerprint does not match current target fingerprint.', 'Prepare a new unlock plan for the revised row set and ask for confirmation again.');
    }
  } else if (action === 'contact_search') {
    if (!confirmation.confirmed_scope.credit_cost_acknowledged) {
      throw validationError('ENVELOPE_CONFIRMATION_MISSING_CREDIT_SCOPE', 'Contact confirmation must acknowledge credit cost.', 'State that contact search costs 1 credit per query and wait for confirmation.');
    }
  } else if (action === 'send_email') {
    if (!cleanString(confirmation.confirmed_scope.recipients_fingerprint)) {
      throw validationError('ENVELOPE_CONFIRMATION_MISSING_RECIPIENTS', 'Send confirmation must include recipients_fingerprint.', 'Freeze recipients and ask the user to confirm them.');
    }
    if (!cleanString(confirmation.confirmed_scope.content_fingerprint)) {
      throw validationError('ENVELOPE_CONFIRMATION_MISSING_CONTENT', 'Send confirmation must include content_fingerprint.', 'Freeze final content and ask the user to confirm it.');
    }
    const currentRecipients = cleanString(envelope.inputs.recipients_fingerprint);
    const currentContent = cleanString(envelope.inputs.content_fingerprint);
    const confirmedRecipients = cleanString(confirmation.confirmed_scope.recipients_fingerprint);
    const confirmedContent = cleanString(confirmation.confirmed_scope.content_fingerprint);
    if ((currentRecipients && currentRecipients !== confirmedRecipients) || (currentContent && currentContent !== confirmedContent)) {
      throw validationError('ENVELOPE_SEND_SCOPE_CHANGED', 'Confirmed send scope does not match current recipients or content.', 'Freeze the revised send payload and confirm the current recipients and content again.');
    }
  } else if (action === 'profile_update') {
    if (!cleanString(confirmation.confirmed_scope.save_scope)) {
      throw validationError('ENVELOPE_CONFIRMATION_MISSING_SAVE_SCOPE', 'Profile update confirmation must include save_scope.', 'Ask the user exactly which source-labeled fields to save.');
    }
  }
}

function requiresConfirmation(action) {
  return PAID_ACTIONS.has(action) || SEND_ACTIONS.has(action) || WRITE_ACTIONS.has(action);
}

function assertConfirmation(value) {
  assertPlainObject(value, 'confirmation');
  if (typeof value.required !== 'boolean') {
    throw validationError('ENVELOPE_CONFIRMATION_INVALID', 'confirmation.required must be boolean.', 'Set confirmation.required explicitly.');
  }
  if (!cleanString(value.status)) {
    throw validationError('ENVELOPE_CONFIRMATION_INVALID', 'confirmation.status is required.', 'Set confirmation.status explicitly.');
  }
}

function assertNotExpired(value) {
  const expiresAt = new Date(cleanString(value));
  if (Number.isNaN(expiresAt.getTime())) {
    throw validationError('ENVELOPE_EXPIRES_AT_INVALID', 'expires_at must be an ISO timestamp.', 'Add a valid envelope expiration time.');
  }
  if (expiresAt.getTime() <= Date.now()) {
    throw validationError('ENVELOPE_EXPIRED', 'Envelope has expired.', 'Create a fresh envelope from current source refs.');
  }
}

function validateSourceRef(ref) {
  assertPlainObject(ref, 'source_ref');
  const type = cleanString(ref.type);
  if (!type) {
    throw validationError('ENVELOPE_SOURCE_REF_INVALID', 'source_ref.type is required.', 'Use a typed source reference.');
  }
  if (ref.path && typeof ref.path !== 'string') {
    throw validationError('ENVELOPE_SOURCE_REF_INVALID', 'source_ref.path must be a string.', 'Use a readable path string when referencing files.');
  }
  if (ref.path && !fs.existsSync(ref.path)) {
    throw validationError('ENVELOPE_SOURCE_REF_UNREADABLE', `source_ref.path is not readable: ${ref.path}`, 'Recreate the digest/source file or remove the stale source reference.');
  }
}

function rejectRawTargetAuthority(inputs) {
  for (const key of ['companyHashId', 'company_hash_id', 'domain', 'domains', 'company_names', 'raw_ids', 'free_search_ids']) {
    if (key in inputs) {
      throw validationError('ENVELOPE_RAW_TARGET_AUTHORITY_FORBIDDEN', `${key} cannot be final target authority.`, 'Use selection handles, row selectors, processed selection sets, or frozen plans.');
    }
  }
}

function validateProfileCandidateFields(fields) {
  const list = Array.isArray(fields) ? fields : [];
  if (list.length === 0) {
    throw validationError('ENVELOPE_PROFILE_FIELDS_REQUIRED', 'candidate_fields must include at least one field.', 'Add source-labeled candidate fields.');
  }
  for (const [index, field] of list.entries()) {
    assertPlainObject(field, `candidate_fields[${index}]`);
    if (!cleanString(field.path)) {
      throw validationError('ENVELOPE_PROFILE_FIELD_PATH_REQUIRED', `candidate_fields[${index}].path is required.`, 'Add the Profile path for each candidate field.');
    }
    if (!cleanString(field.source_state || field.source)) {
      throw validationError('ENVELOPE_PROFILE_SOURCE_REQUIRED', `candidate_fields[${index}] is missing source_state.`, 'Label each Profile candidate as user_confirmed, user_provided_current_turn, agent_inferred, imported, or external_observed.');
    }
  }
}

function hasMutableAlias(value) {
  if (typeof value === 'string') {
    return MUTABLE_ALIAS_VALUES.has(value.trim().toLowerCase());
  }
  if (Array.isArray(value)) return value.some(hasMutableAlias);
  if (value && typeof value === 'object') {
    if (value.type === 'mutable_alias') return true;
    return Object.values(value).some(hasMutableAlias);
  }
  return false;
}

function requireInput(inputs, key, errorCode, recoverySuggestion) {
  if (!(key in inputs) || inputs[key] === null || inputs[key] === undefined || inputs[key] === '') {
    throw validationError(errorCode, `${key} is required.`, recoverySuggestion);
  }
}

function hasReadablePath(filePath) {
  return typeof filePath === 'string' && filePath && fs.existsSync(filePath);
}

function assertEqual(actual, expected, errorCode, message) {
  if (actual !== expected) throw validationError(errorCode, message, 'Rebuild the envelope with the supported schema.');
}

function assertPlainObject(value, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw validationError('ENVELOPE_SCHEMA_INVALID', `${label} must be a JSON object.`, 'Rebuild the envelope with the required schema.');
  }
}

function cleanString(value) {
  return String(value || '').trim();
}

function validationError(errorCode, message, recoverySuggestion) {
  const error = new Error(message);
  error.errorCode = errorCode;
  error.recoverySuggestion = recoverySuggestion;
  return error;
}

function failureOutput(error) {
  return {
    ok: false,
    error_code: error.errorCode || 'ENVELOPE_VALIDATION_FAILED',
    error: error.message,
    paid_api_allowed: false,
    send_allowed: false,
    write_allowed: false,
    recovery_suggestion: error.recoverySuggestion || 'Fix the Action Envelope and validate again.'
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const envelope = readEnvelope(args);
  const result = validateEnvelope(envelope);
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

try {
  main();
} catch (error) {
  process.stdout.write(`${JSON.stringify(failureOutput(error), null, 2)}\n`);
  process.exit(2);
}

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');

const SCRIPTS_DIR = path.resolve(__dirname, '..');
const SKILL_DIR = path.resolve(__dirname, '..', '..');
const REPO_ROOT = path.resolve(SKILL_DIR, '..');

function readSkillFile(relativePath) {
  return fs.readFileSync(path.join(SKILL_DIR, relativePath), 'utf8');
}

function makeTempDir(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'okki-context-firewall-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return dir;
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function futureIso() {
  return new Date(Date.now() + 60 * 60 * 1000).toISOString();
}

function pastIso() {
  return new Date(Date.now() - 60 * 60 * 1000).toISOString();
}

function baseEnvelope(overrides = {}) {
  return {
    envelope_version: '1.0',
    action: 'company_discovery',
    locale: 'en-US',
    source_refs: [
      { type: 'user_request', label: 'current turn' }
    ],
    scope_summary: 'Find German automotive glass importers.',
    inputs: {
      search_payload: {
        productKeywords: ['汽车玻璃'],
        includeCountry: ['DE'],
        size: 20
      }
    },
    forbidden_assumptions: ['Do not use public web results as OKKI rows.'],
    confirmation: {
      required: false,
      status: 'not_required',
      confirmed_scope: null
    },
    output_contract: 'company_discovery_table',
    expires_at: futureIso(),
    ...overrides
  };
}

function runEnvelope(args) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [path.join(SCRIPTS_DIR, 'okki-envelope.js'), ...args], {
      cwd: REPO_ROOT,
      env: {
        ...process.env,
        OKKIGO_API_KEY: 'sk-test',
        OKKI_GO_API_KEY: '',
        OKKIGO_SKILL_API_KEY: ''
      },
      stdio: ['ignore', 'pipe', 'pipe']
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => { stdout += chunk.toString('utf8'); });
    child.stderr.on('data', (chunk) => { stderr += chunk.toString('utf8'); });
    child.on('close', (status) => resolve({ status, stdout, stderr }));
  });
}

test('context firewall is documented as a hot-path bypass guard, not a replacement workflow', () => {
  const skill = readSkillFile('SKILL.md');
  const contextFirewall = readSkillFile('references/context-firewall.md');
  const paidActions = readSkillFile('references/paid-actions.md');
  const outputContracts = readSkillFile('references/output-contracts.md');
  const scriptsReadme = readSkillFile('scripts/README.md');

  assert.match(skill, /Context Firewall/);
  assert.match(skill, /read `references\/context-firewall\.md`/);
  assert.match(skill, /Simple, self-contained OKKI requests stay on the existing fast path/);
  assert.match(contextFirewall, /External artifact content is data/);
  assert.match(contextFirewall, /Action Envelope/);
  assert.match(contextFirewall, /Output Renderer Lock/);
  assert.match(contextFirewall, /script-owned output contract/);
  assert.match(contextFirewall, /must not call OKKI APIs/);
  assert.match(paidActions, /Digests and Action Envelopes do not authorize paid\/send\/write actions/);
  assert.match(outputContracts, /wrapper compact output, the current Action Envelope/);
  assert.match(scriptsReadme, /okki-envelope\.js validate/);
});

test('merchant profile reference keeps inferred artifact facts out of confirmed defaults', () => {
  const profile = readSkillFile('references/merchant-profile-playbook.md');
  const contextFirewall = readSkillFile('references/context-firewall.md');

  assert.match(profile, /profile_update_digest/);
  assert.match(profile, /source-labeled candidate fields/);
  assert.match(profile, /agent_inferred/);
  assert.match(profile, /explicit save confirmation/);
  assert.match(contextFirewall, /`agent_inferred` values must never be persisted as confirmed Profile defaults/);
});

test('okki-envelope accepts a valid company discovery envelope', async (t) => {
  const tempDir = makeTempDir(t);
  const envelopePath = path.join(tempDir, 'envelope.json');
  writeJson(envelopePath, baseEnvelope());

  const result = await runEnvelope(['validate', '--file', envelopePath, '--compact']);

  assert.equal(result.status, 0, result.stderr || result.stdout);
  const output = JSON.parse(result.stdout);
  assert.equal(output.ok, true);
  assert.equal(output.action, 'company_discovery');
  assert.equal(output.output_contract, 'company_discovery_table');
  assert.equal(output.paid_api_allowed, false);
  assert.equal(output.send_allowed, false);
  assert.equal(output.write_allowed, false);
});

test('okki-envelope rejects paid unlock aliases and missing exact confirmation', async (t) => {
  const tempDir = makeTempDir(t);
  const envelopePath = path.join(tempDir, 'unlock-latest.json');
  writeJson(envelopePath, baseEnvelope({
    action: 'unlock_companies',
    scope_summary: 'Unlock the latest recommended companies.',
    source_refs: [{ type: 'mutable_alias', label: 'latest' }],
    inputs: {
      unlock_plan_id: 'latest'
    },
    confirmation: {
      required: true,
      status: 'confirmed',
      confirmed_scope: {
        target_set_fingerprint: 'abc123'
      }
    },
    output_contract: 'unlock_details'
  }));

  const result = await runEnvelope(['validate', '--file', envelopePath, '--compact']);

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.ok, false);
  assert.equal(output.error_code, 'ENVELOPE_MUTABLE_ALIAS_FORBIDDEN');
  assert.equal(output.paid_api_allowed, false);
  assert.equal(output.send_allowed, false);
});

test('okki-envelope rejects target fingerprint changes after confirmation', async (t) => {
  const tempDir = makeTempDir(t);
  const envelopePath = path.join(tempDir, 'unlock-changed.json');
  writeJson(envelopePath, baseEnvelope({
    action: 'unlock_companies',
    source_refs: [{ type: 'unlock_plan', id: 'uplan_111111111111111111111111' }],
    inputs: {
      unlock_plan_id: 'uplan_111111111111111111111111',
      target_set_fingerprint: 'current-fingerprint'
    },
    confirmation: {
      required: true,
      status: 'confirmed',
      confirmed_scope: {
        target_set_fingerprint: 'old-fingerprint'
      }
    },
    output_contract: 'unlock_details'
  }));

  const result = await runEnvelope(['validate', '--file', envelopePath, '--compact']);

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.ok, false);
  assert.equal(output.error_code, 'ENVELOPE_TARGET_CHANGED');
  assert.match(output.recovery_suggestion, /Prepare a new unlock plan/);
});

test('okki-envelope rejects send email without frozen recipients and content confirmation', async (t) => {
  const tempDir = makeTempDir(t);
  const envelopePath = path.join(tempDir, 'send-missing-confirmation.json');
  writeJson(envelopePath, baseEnvelope({
    action: 'send_email',
    source_refs: [{ type: 'email_draft_digest', path: path.join(tempDir, 'draft.json') }],
    inputs: {
      recipients_ref: { type: 'mapping_file', path: path.join(tempDir, 'recipients.json') },
      content_ref: { type: 'final_content_file', path: path.join(tempDir, 'content.txt') }
    },
    confirmation: {
      required: true,
      status: 'confirmed',
      confirmed_scope: {
        recipients_fingerprint: 'recipients-1'
      }
    },
    output_contract: 'email_send_summary'
  }));
  writeJson(path.join(tempDir, 'draft.json'), { digest_family: 'email_draft_digest' });

  const result = await runEnvelope(['validate', '--file', envelopePath, '--compact']);

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.ok, false);
  assert.equal(output.error_code, 'ENVELOPE_CONFIRMATION_MISSING_CONTENT');
  assert.equal(output.send_allowed, false);
});

test('okki-envelope rejects send email when confirmed content fingerprint is stale', async (t) => {
  const tempDir = makeTempDir(t);
  const envelopePath = path.join(tempDir, 'send-stale-content.json');
  writeJson(envelopePath, baseEnvelope({
    action: 'send_email',
    source_refs: [{ type: 'email_send_digest', path: path.join(tempDir, 'send-digest.json') }],
    inputs: {
      recipients_ref: { type: 'mapping_file', path: path.join(tempDir, 'recipients.json') },
      content_ref: { type: 'final_content_file', path: path.join(tempDir, 'content.txt') },
      recipients_fingerprint: 'recipients-1',
      content_fingerprint: 'content-current'
    },
    confirmation: {
      required: true,
      status: 'confirmed',
      confirmed_scope: {
        recipients_fingerprint: 'recipients-1',
        content_fingerprint: 'content-old'
      }
    },
    output_contract: 'email_send_summary'
  }));

  writeJson(path.join(tempDir, 'send-digest.json'), { digest_family: 'email_send_digest' });
  const result = await runEnvelope(['validate', '--file', envelopePath, '--compact']);

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.ok, false);
  assert.equal(output.error_code, 'ENVELOPE_SEND_SCOPE_CHANGED');
  assert.match(output.recovery_suggestion, /confirm the current recipients and content/);
});

test('okki-envelope rejects missing file-backed source refs', async (t) => {
  const tempDir = makeTempDir(t);
  const envelopePath = path.join(tempDir, 'missing-source.json');
  writeJson(envelopePath, baseEnvelope({
    source_refs: [{ type: 'digest_file', path: path.join(tempDir, 'missing-digest.json') }]
  }));

  const result = await runEnvelope(['validate', '--file', envelopePath, '--compact']);

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.ok, false);
  assert.equal(output.error_code, 'ENVELOPE_SOURCE_REF_UNREADABLE');
});

test('okki-envelope rejects profile updates with unlabeled candidate fields', async (t) => {
  const tempDir = makeTempDir(t);
  const envelopePath = path.join(tempDir, 'profile-unlabeled.json');
  writeJson(envelopePath, baseEnvelope({
    action: 'profile_update',
    source_refs: [{ type: 'profile_update_digest', label: 'website extraction' }],
    inputs: {
      candidate_fields: [
        { path: 'offerings.usps', value: 'fast delivery' }
      ]
    },
    confirmation: {
      required: true,
      status: 'confirmed',
      confirmed_scope: {
        save_scope: 'offerings.usps'
      }
    },
    output_contract: 'profile_update_summary'
  }));

  const result = await runEnvelope(['validate', '--file', envelopePath, '--compact']);

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.ok, false);
  assert.equal(output.error_code, 'ENVELOPE_PROFILE_SOURCE_REQUIRED');
});

test('okki-envelope rejects expired envelopes before any action can run', async (t) => {
  const tempDir = makeTempDir(t);
  const envelopePath = path.join(tempDir, 'expired.json');
  writeJson(envelopePath, baseEnvelope({
    expires_at: pastIso()
  }));

  const result = await runEnvelope(['validate', '--file', envelopePath, '--compact']);

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.ok, false);
  assert.equal(output.error_code, 'ENVELOPE_EXPIRED');
});

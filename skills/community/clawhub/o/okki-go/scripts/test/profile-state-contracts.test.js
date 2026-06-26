const test = require('node:test');
const assert = require('node:assert/strict');
const {
  computeCompleteness,
  normalizeProfile,
  redactProfile
} = require('../okki-state');

test('user_provided_current_turn profile source round-trips without becoming agent_inferred', () => {
  const now = new Date('2026-06-17T00:00:00Z');
  const normalized = normalizeProfile({
    version: '1.1',
    offerings: {
      applications: [
        { value: 'fleet maintenance', source: 'user_provided_current_turn', updated_at: '2026-06-17' }
      ]
    }
  }, now, { touch: false });

  const entry = normalized.state.offerings.applications[0];
  assert.equal(entry.source, 'user_provided_current_turn');
  assert.equal(entry.value, 'fleet maintenance');
  assert.equal(computeCompleteness(normalized.state), 0);
});

test('user_provided_current_turn does not count as trusted discovery default completeness', () => {
  const now = new Date('2026-06-17T00:00:00Z');
  const normalized = normalizeProfile({
    version: '1.1',
    target_baseline: {
      regions_primary: [
        { value: 'DE', source: 'user_provided_current_turn', updated_at: '2026-06-17' }
      ],
      decision_roles: [
        { value: 'Procurement Manager', source: 'user_confirmed', updated_at: '2026-06-17' }
      ]
    }
  }, now, { touch: false });

  assert.equal(normalized.state.target_baseline.regions_primary[0].source, 'user_provided_current_turn');
  assert.equal(normalized.state.target_baseline.decision_roles[0].source, 'user_confirmed');
  assert.equal(computeCompleteness(normalized.state), 0.2);
});

test('redactProfile hides sender name and email by default', () => {
  const redacted = redactProfile({
    outreach_identity: {
      sender_name: 'Carrie Zhang',
      sender_email: 'carrie@example.com'
    }
  });

  assert.equal(redacted.outreach_identity.sender_name, 'C***');
  assert.equal(redacted.outreach_identity.sender_email, 'c***@example.com');
});

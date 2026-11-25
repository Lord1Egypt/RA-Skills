'use strict';
// U1 — normalize-then-hash. R18 (TC-S4-2).
//
// The suite's job is the ORDER, not the normalization: a hash taken before
// normalising makes javis-server refuse every single upload (F67), and nothing
// downstream of here can tell that apart from a server fault. So the inversion
// gets its own named test, and the round trip is asserted on bytes.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');

const {
  normalize, hash, checkText, prepare, REFUSALS, MAX_TEXT_BYTES,
} = require('../scripts/normalize.js');

const sha = (s) => crypto.createHash('sha256').update(Buffer.from(s, 'utf8')).digest('hex');

// ---------------------------------------------------------------------------
// R18 — the order
// ---------------------------------------------------------------------------

test('R18 TC-S4-2: body_hash is sha256 over the text as sent, byte for byte', () => {
  const out = prepare('# Study guide\n\nSome body.\n');
  assert.equal(out.ok, true);
  assert.equal(out.body_hash, sha(out.text), 'the hash must be over prepare()\'s own text');
  assert.match(out.body_hash, /^[0-9a-f]{64}$/, '64 lowercase hex, as _HEX64 requires');
  assert.equal(out.bytes, Buffer.byteLength(out.text, 'utf8'));
});

test('R18 TC-S4-2: hashing BEFORE normalising produces a different digest (the F67 inversion)', () => {
  // The exact shape of the bug: CRLF in, hash taken on the raw string, text
  // sent normalised. If these two ever match, the ordering has stopped being
  // observable and this module no longer protects anything.
  const raw = '# Title\r\n\r\nBody line\r\n';
  const text = normalize(raw);
  assert.notEqual(text, raw, 'the fixture must actually be changed by normalising');
  assert.notEqual(
    hash(raw), hash(text),
    'hash(raw) must differ from hash(normalize(raw)), or the inversion is invisible',
  );
  // And the inverted pairing is exactly what the server refuses.
  assert.notEqual(prepare(raw).body_hash, hash(raw));
});

test('R18: hash() refuses a non-string rather than stringifying it', () => {
  assert.throws(() => hash(undefined), TypeError);
  assert.throws(() => hash({ text: 'x' }), TypeError);
});

test('R18: hash() does not normalise on its own behalf', () => {
  // If hash() quietly normalised, a caller that forgot normalize() would still
  // get a passing hash — for text it never sent.
  assert.notEqual(hash('a\r\n'), hash('a\n'));
});

// ---------------------------------------------------------------------------
// Normalization rules
// ---------------------------------------------------------------------------

test('normalize: CRLF and lone CR fold to LF, BOM is stripped', () => {
  assert.equal(normalize('a\r\nb\rc'), 'a\nb\nc\n');
  assert.equal(normalize('﻿hello'), 'hello\n');
});

test('normalize: idempotent, so a re-fetch of an unchanged note hashes the same', () => {
  for (const raw of ['a\r\nb', '﻿x\n\n\n', '  ', '', 'line  \nnext\n']) {
    assert.equal(normalize(normalize(raw)), normalize(raw), JSON.stringify(raw));
  }
});

test('normalize: keeps per-line trailing spaces (two spaces is a markdown line break)', () => {
  assert.equal(normalize('one  \ntwo'), 'one  \ntwo\n');
});

test('normalize: trailing whitespace collapses to exactly one final newline', () => {
  assert.equal(normalize('body\n\n\n  \n'), 'body\n');
  assert.equal(normalize('body'), 'body\n');
});

test('normalize: an all-whitespace note normalises to the empty string', () => {
  assert.equal(normalize('   \n\t\n'), '');
  assert.equal(normalize(null), '');
});

test('R18 TC-S4-2: a CJK note with a markdown table survives byte-identically (F64 note shape)', () => {
  // The real note research pushed through the gates: Chinese study guide, table.
  const raw = [
    '# 新建记事',
    '',
    '| 概念 | 说明 |',
    '| --- | --- |',
    '| 熵 | 系统无序程度的度量 |',
    '| 焓 | 系统的总热含量 |',
    '',
    '结论：两者都是状态函数。',
  ].join('\r\n');
  const out = prepare(raw);
  assert.equal(out.ok, true);
  assert.equal(out.text, `${raw.replace(/\r\n/g, '\n')}\n`);
  assert.equal(out.body_hash, sha(out.text));
  assert.ok(out.text.includes('熵'), 'CJK must not be mangled');
  assert.ok(out.text.includes('| --- | --- |'), 'the table must survive');
});

// ---------------------------------------------------------------------------
// R4 / R5 — the content gates, each one reason plus one next action
// ---------------------------------------------------------------------------

test('R4 R5: the size boundary is exact, and oversize is refused before any hash', () => {
  // normalize() appends the final newline, so the pre-normalised body is one
  // byte shorter than the budget it has to fit.
  const atLimit = `${'a'.repeat(MAX_TEXT_BYTES - 1)}`;
  const ok = prepare(atLimit);
  assert.equal(ok.ok, true, `${MAX_TEXT_BYTES} bytes must pass`);
  assert.equal(ok.bytes, MAX_TEXT_BYTES);

  const over = prepare('a'.repeat(MAX_TEXT_BYTES));
  assert.equal(over.ok, false);
  assert.equal(over.error, 'text_too_large');
  assert.equal(over.body_hash, undefined, 'no hash is computed for an oversize note');
});

test('R4 R5: NUL and an unpaired surrogate are each their own named refusal', () => {
  const nul = prepare('before\u0000after');
  assert.equal(nul.error, 'text_has_nul');

  const lone = prepare(`lead ${String.fromCharCode(0xd800)} trail`);
  assert.equal(lone.error, 'text_not_utf8');

  // A well-formed pair is not a lone surrogate and must pass.
  assert.equal(prepare('emoji 😀 ok').ok, true);
  assert.equal(checkText('𝄞 clef\n'), null);
});

test('R4 R5: an empty note is refused, not pushed as an empty body', () => {
  assert.equal(prepare('').error, 'text_empty');
  assert.equal(prepare('  \n ').error, 'text_empty');
});

test('R4 R5: every refusal carries exactly one reason and one next action', () => {
  const codes = Object.keys(REFUSALS);
  assert.ok(codes.length >= 4);
  for (const code of codes) {
    const r = REFUSALS[code];
    assert.match(code, /^[a-z][a-z0-9_]*$/, `${code} must be a machine-readable code`);
    assert.ok(r.reason && r.reason.length > 10, `${code}.reason`);
    assert.ok(r.next && r.next.length > 10, `${code}.next`);
    assert.doesNotMatch(r.reason, /\n/, `${code}.reason must be one line`);
  }
});

test('a refusal envelope never also carries text (nothing half-prepared is pushable)', () => {
  const out = prepare('\u0000');
  assert.equal(out.ok, false);
  assert.equal(out.text, undefined);
  assert.equal(out.body_hash, undefined);
});

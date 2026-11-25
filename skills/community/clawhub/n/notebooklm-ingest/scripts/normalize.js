'use strict';
/**
 * normalize-then-hash — the one ordering requirement in this bundle (R18).
 *
 * Spec: javis.is/docs/superpowers/specs/2026-10-29-notebooklm-connector-design.md
 *       §Requirements R18, and research F67.
 *
 * A pure module: no I/O, no clock, no CLI, no network — the same rule
 * `javis-obsidian/src/core/` follows, and for the same reason. What is hashed
 * here is the exact string the push sends, so this file is the only place the
 * wire contract can be got wrong, and it must be testable without a container.
 *
 * **THE ORDER IS THE REQUIREMENT.** javis-server's `_check_text_and_hash`
 * (javis_mcp/obsidian_sources.py) takes sha256 over the UTF-8 bytes of the text
 * *as sent*, and its docstring is explicit that the server must never rewrite
 * the text because "rewriting the text here would make every hash mismatch".
 * F67 proved the inversion empirically: normalising the note and keeping the
 * hash taken before normalising produced `body_hash does not match the text` —
 * on every upload, not occasionally. So:
 *
 *     normalize(raw)  →  text        (what travels)
 *     hash(text)      →  body_hash   (taken over exactly that)
 *
 * and never the other way round. `prepare()` composes the two so no caller has
 * to remember, and `test/normalize.test.js` pins the inversion as a failing
 * case rather than trusting the comment.
 *
 * **What normalising does, and what it deliberately does not.** It mirrors the
 * Obsidian plugin's `uploadText()` (javis-obsidian/src/core/note-text.ts):
 * strip a leading BOM, fold CRLF and lone CR to LF, then trim trailing
 * whitespace to a single final newline. It does **not** carry the plugin's
 * other half — the removal of `javis_*` frontmatter keys — because a NotebookLM
 * note has no frontmatter at all: the CLI hands back body text, not a vault
 * file the plugin has stamped. That omission is stated here rather than left to
 * be noticed, because the two normalizers otherwise look like they drifted.
 *
 * Per-line trailing spaces are **kept**. Two trailing spaces are a markdown
 * hard line break, so stripping them would rewrite the note's rendering to win
 * a cosmetic tidy.
 *
 * **The checks are the server's, run early.** Every refusal below is a rule
 * javis-server already enforces; running them here turns a 400 the agent has to
 * interpret into a named refusal with a next action (R4, R5), and keeps an
 * oversize note from spending a request. MAX_TEXT_BYTES is checked BEFORE the
 * hash, matching the server, so an oversize note reports its size rather than
 * its hash whatever else is wrong with it.
 */

const crypto = require('crypto');

/** Mirrors javis-server `MAX_TEXT_BYTES` (javis_mcp/obsidian_sources.py:100). */
const MAX_TEXT_BYTES = 256 * 1024;

const BOM = '﻿';

/**
 * A surrogate code unit with no partner. JSON can carry `"\ud800"` and UTF-8
 * cannot encode it: Node silently substitutes U+FFFD (so the hash would be
 * taken over different bytes than Postgres stores), and psycopg raises a bare
 * `UnicodeEncodeError`. The server's `_storable` refuses such a string, so this
 * refuses it one hop earlier with something the user can act on.
 */
const LONE_SURROGATE_RE =
  /[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/;

/**
 * One machine-readable code per refusal, each with one reason and one next
 * action — R4 and R5 in their wire form. SKILL.md's Errors table carries the
 * same rows, and `test/skill-md.test.js` fails if the two drift.
 */
const REFUSALS = Object.freeze({
  text_empty: {
    reason: 'the note has no text left after normalising',
    next: 'open the note in NotebookLM, check it is not empty, then fetch it again',
  },
  text_has_nul: {
    reason: 'the note text contains a NUL byte, which the wiki store cannot hold',
    next: 'remove the NUL byte in NotebookLM, or ingest the note as hand-fed text',
  },
  text_not_utf8: {
    reason: 'the note text contains an unpaired surrogate, which UTF-8 cannot encode',
    next: 'retype the damaged character in NotebookLM and fetch the note again',
  },
  text_too_large: {
    reason: `the normalised note is over ${MAX_TEXT_BYTES} bytes of UTF-8`,
    next: 'split the note in NotebookLM and fetch the halves as separate notes',
  },
});

/**
 * STEP 1. The text that travels, and the only string `hash` may be given.
 *
 * Idempotent: `normalize(normalize(x)) === normalize(x)` for every input, which
 * is what lets a re-fetch of an unchanged note produce an unchanged hash and so
 * no second wiki write.
 */
function normalize(raw) {
  let s = String(raw == null ? '' : raw);
  if (s.startsWith(BOM)) s = s.slice(1);
  s = s.replace(/\r\n?/g, '\n');
  // Trailing whitespace at the very END only — never per line (see docblock).
  s = s.replace(/\s+$/, '');
  return s === '' ? '' : `${s}\n`;
}

/**
 * The server's content gates, run on the normalised text. `null` means it will
 * pass; a code means it will not and why.
 *
 * Size is checked LAST of the content rules but BEFORE any hash is taken,
 * which is the server's own order (`_check_text_and_hash` raises `_TooLarge`
 * before comparing hashes).
 */
function checkText(text) {
  if (typeof text !== 'string' || text.trim() === '') return 'text_empty';
  if (text.includes('\u0000')) return 'text_has_nul';
  if (LONE_SURROGATE_RE.test(text)) return 'text_not_utf8';
  if (Buffer.byteLength(text, 'utf8') > MAX_TEXT_BYTES) return 'text_too_large';
  return null;
}

/**
 * STEP 2. sha256 over the UTF-8 bytes of the string it is given, lowercase hex.
 *
 * It takes a string and returns a digest; it does NOT normalise, on purpose.
 * A `hash` that normalised first would make the inversion this module exists to
 * prevent invisible — every caller would get a passing hash for text it never
 * sent.
 */
function hash(text) {
  if (typeof text !== 'string') {
    throw new TypeError('hash(text): text must be a string (normalize it first)');
  }
  return crypto.createHash('sha256').update(Buffer.from(text, 'utf8')).digest('hex');
}

/**
 * The two steps in the only order that works, plus the gates.
 *
 * Returns `{ok: true, text, body_hash, bytes}` where `body_hash === hash(text)`
 * and `text` is byte-for-byte what the push must send, or
 * `{ok: false, error, reason, next}` naming one refusal.
 */
function prepare(raw) {
  const text = normalize(raw);
  const bad = checkText(text);
  if (bad) return Object.assign({ ok: false, error: bad }, REFUSALS[bad]);
  return { ok: true, text, body_hash: hash(text), bytes: Buffer.byteLength(text, 'utf8') };
}

module.exports = {
  normalize,
  hash,
  checkText,
  prepare,
  REFUSALS,
  MAX_TEXT_BYTES,
  LONE_SURROGATE_RE,
};

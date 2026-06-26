/**
 * G-02 — PII Leakage Prevention
 * Layer: output | Severity: redact
 *
 * Detects and redacts Australian PII patterns from agent output.
 */

import type { GuardContext, GuardResult } from '../types.js';

// ──────────────────────────────────────────────────────────────────────────────
// Pattern definitions
// ──────────────────────────────────────────────────────────────────────────────

/** AU mobile: 04XX XXX XXX or 04XXXXXXXX (with optional spaces/dashes) */
const AU_MOBILE = /\b04\d{2}[\s-]?\d{3}[\s-]?\d{3}\b/g;

/** AU landline: (0X) XXXX XXXX */
const AU_LANDLINE = /\(0\d\)\s?\d{4}\s?\d{4}/g;

/** Email addresses */
const EMAIL = /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g;

/**
 * AU ABN: 11 digits formatted as XX XXX XXX XXX
 * Must be preceded/followed by word boundary or space to avoid partial matches.
 */
const AU_ABN = /\b\d{2}\s\d{3}\s\d{3}\s\d{3}\b/g;

/**
 * AU BSB: XXX-XXX (6 digits with hyphen, standalone)
 * Word-boundary anchored to avoid matching phone numbers or other digit strings.
 *
 * ⚠️ FP RISK: This pattern can match non-BSB sequences such as date fragments
 * (e.g. "123-456" in a serial number), version strings ("1.2-345" won't match
 * but "012-345" will), or any 3-dash-3 digit token. Downstream consumers
 * should treat [REDACTED-BSB] occurrences as probable rather than certain PII.
 * A future improvement would add a checksum or leading-digit bank-code filter.
 */
// Tightened: exclude when preceded by +, digit, or hyphen (avoids matching US phone fragments like +1-555-867-5309)
const AU_BSB = /(?<![+\d-])\b\d{3}-\d{3}\b(?!\d)/g;

/**
 * AU TFN: 9 consecutive digits.
 * The official TFN checksum uses weights [1,4,3,7,5,8,6,9,10] mod 11.
 * We validate the checksum to avoid false positives on arbitrary 9-digit numbers.
 */
const AU_TFN_RAW = /\b(\d{9})\b/g;

const TFN_WEIGHTS = [1, 4, 3, 7, 5, 8, 6, 9, 10];

function isTfn(digits: string): boolean {
  if (digits.length !== 9) return false;
  const sum = digits
    .split('')
    .reduce((acc, d, i) => acc + parseInt(d, 10) * TFN_WEIGHTS[i], 0);
  return sum % 11 === 0;
}

// ──────────────────────────────────────────────────────────────────────────────
// Evaluator
// ──────────────────────────────────────────────────────────────────────────────

export async function evaluate(ctx: GuardContext): Promise<GuardResult> {
  let text = ctx.content;
  let redacted = false;

  // AU Mobile
  const mobileMatches = text.match(AU_MOBILE);
  if (mobileMatches?.length) {
    text = text.replace(AU_MOBILE, '[REDACTED-PHONE]');
    redacted = true;
  }

  // AU Landline
  const landlineMatches = text.match(AU_LANDLINE);
  if (landlineMatches?.length) {
    text = text.replace(AU_LANDLINE, '[REDACTED-PHONE]');
    redacted = true;
  }

  // Email
  const emailMatches = text.match(EMAIL);
  if (emailMatches?.length) {
    text = text.replace(EMAIL, '[REDACTED-EMAIL]');
    redacted = true;
  }

  // AU ABN (before TFN to avoid overlap — ABN is 11 digits with spaces)
  const abnMatches = text.match(AU_ABN);
  if (abnMatches?.length) {
    text = text.replace(AU_ABN, '[REDACTED-ABN]');
    redacted = true;
  }

  // AU BSB
  const bsbMatches = text.match(AU_BSB);
  if (bsbMatches?.length) {
    text = text.replace(AU_BSB, '[REDACTED-BSB]');
    redacted = true;
  }

  // AU TFN (checksum-validated)
  let tfnFound = false;
  text = text.replace(AU_TFN_RAW, (match, digits) => {
    if (isTfn(digits)) {
      tfnFound = true;
      return '[REDACTED-TFN]';
    }
    return match;
  });
  if (tfnFound) redacted = true;

  if (redacted) {
    return {
      passed: true,
      rule: 'G-02',
      action: 'redact',
      detail: 'PII detected and redacted from output',
      redacted: text,
    };
  }

  return { passed: true, action: 'pass' };
}

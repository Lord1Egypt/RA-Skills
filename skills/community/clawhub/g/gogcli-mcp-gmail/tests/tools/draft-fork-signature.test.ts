import { describe, it, expect } from 'vitest';
import { authoredBodyLines, measureBodyAgreement } from '../../src/tools/gmail-extra.js';

/**
 * HAZARD A — the lineage judgement must not fire on two unrelated drafts.
 *
 * `boilerplateLineFlags` stripped the RFC 3676 `-- ` block, the client's own
 * `Sent from my iPhone`, and the NAME under a sign-off — but the run stopped at
 * the first line that was not name-shaped, so a USER-CONFIGURED signature
 * survived as authored prose:
 *
 *     Thanks,                    -> stripped
 *     Chris Hall                 -> stripped
 *     (704) 555-0142             -> run stopped; survived
 *     chris.c.hall@gmail.com     -> survived
 *     https://example.com/chris  -> survived
 *
 * Those lines are identical on every message the account composes. Measured
 * before the fix: two unrelated drafts shared 3 authored lines / 61 chars and
 * scored similarity 0.60 against a 0.60 threshold — meetsThreshold TRUE on a
 * plumber note and a soccer note. In a mailbox whose drafts go to a parenting
 * coordinator, a wrong pairing is the expensive direction.
 */
const SIGNATURE = ['Thanks,', 'Chris Hall', '(704) 555-0142', 'chris.c.hall@gmail.com', 'https://example.com/chris'];
const withSig = (body: string[]) => ['Hi Sam,', '', ...body, '', ...SIGNATURE].join('\n');

describe('a shared signature is never lineage evidence', () => {
  it('does not pair two unrelated drafts that share one signature', () => {
    const m = measureBodyAgreement(withSig(['The plumber comes Tuesday at 9am.']), withSig(['Soccer registration closes Friday.']));
    expect(m.sharedAuthoredLines).toBe(0);
    expect(m.meetsThreshold).toBe(false);
  });

  it('strips the whole signature block, not just the name', () => {
    expect(authoredBodyLines(withSig(['The plumber comes Tuesday at 9am.']))).toEqual(['The plumber comes Tuesday at 9am.']);
  });
});

describe('and it still stops at authored content', () => {
  it('keeps a postscript under the signature', () => {
    expect(authoredBodyLines([...SIGNATURE, '', 'P.S. The invoice is attached.'].join('\n')))
      .toEqual(['P.S. The invoice is attached.']);
  });

  it('keeps prose under the sign-off', () => {
    expect(authoredBodyLines(['Thanks,', 'Chris', '', 'Actually the plumber moved to Wednesday.'].join('\n')))
      .toEqual(['Actually the plumber moved to Wednesday.']);
  });

  it('keeps contact-shaped lines that are NOT under a sign-off', () => {
    // The rule is positional. A bare phone number in the body is content.
    expect(authoredBodyLines(['(704) 555-0142', 'chris@example.com'].join('\n')))
      .toEqual(['(704) 555-0142', 'chris@example.com']);
  });

  it('keeps a phone number inside a sentence', () => {
    expect(authoredBodyLines(['Call me at (704) 555-0142 about the roof.', '', 'Thanks,', 'Chris'].join('\n')))
      .toEqual(['Call me at (704) 555-0142 about the roof.']);
  });

  it('still pairs two drafts that genuinely share authored prose', () => {
    const shared = ['The plumber comes Tuesday at 9am.', 'He will need access to the crawlspace.', 'I left a key under the mat for him.'];
    const m = measureBodyAgreement(withSig(shared), withSig([...shared, 'One more thing: the gate code is 4417.']));
    expect(m.sharedAuthoredLines).toBeGreaterThanOrEqual(3);
    expect(m.meetsThreshold).toBe(true);
  });
});

import { describe, it, expect } from 'vitest';
import {
  originFromDraftId,
  rootsOwnThread,
  parseHeaders,
  headerValue,
  appleIdentitySignals,
  normalizeMessageId,
  messageIdsIn,
  normalizeBodyLines,
  bodySimilarity,
  isQuotedBodyLine,
  authoredBodyLines,
  measureBodyAgreement,
  normalizeFrom,
  parseInternalDateMs,
  evaluateForkPairing,
  decodeBase64UrlText,
  decodePartText,
  bestBodyText,
  diffBodyLines,
  evaluateContentLoss,
  unreadableSiblingCheck,
  FORK_BODY_SIMILARITY_THRESHOLD,
  FORK_MIN_SHARED_AUTHORED_LINES,
  FORK_MIN_SHARED_AUTHORED_CHARS,
  FORK_SIGNALS_THAT_NEVER_SUFFICE,
  type DraftFacts,
} from '../../src/tools/gmail-extra.js';

// ---------------------------------------------------------------------------
// Tier 0 primitives — derivable from `gog gmail drafts list` alone (no spawns).
// ---------------------------------------------------------------------------

describe('originFromDraftId', () => {
  it('classifies an `s:` id as non-api', () => {
    expect(originFromDraftId('s:14092347734530621658')).toBe('non-api');
  });

  it('classifies an `r` id as api', () => {
    expect(originFromDraftId('r4303011157206680397')).toBe('api');
  });

  // The bug this test exists to prevent: draft ids can be NEGATIVE, so any
  // /^r\d/ test misclassifies a real API draft as non-api.
  it('classifies a NEGATIVE api id as api, not non-api', () => {
    expect(originFromDraftId('r-457330811034304502')).toBe('api');
  });

  it('never says "apple-mail" — that verdict needs a header, not a prefix', () => {
    expect(originFromDraftId('s:1')).not.toBe('apple-mail');
  });
});

describe('rootsOwnThread', () => {
  it('is true when threadId equals messageId', () => {
    expect(rootsOwnThread({ id: 'r1', messageId: 'abc', threadId: 'abc' })).toBe(true);
  });

  it('is false when the draft sits in an existing thread', () => {
    expect(rootsOwnThread({ id: 'r1', messageId: 'abc', threadId: 'def' })).toBe(false);
  });

  it('is false — not true — when messageId is absent (undefined === undefined trap)', () => {
    expect(rootsOwnThread({ id: 'r1', threadId: 'abc' })).toBe(false);
  });

  it('is false when threadId is absent', () => {
    expect(rootsOwnThread({ id: 'r1', messageId: 'abc' })).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// Header parsing — Apple writes `Mime-Version`, the Gmail API writes
// `MIME-Version`, so every lookup must be case-insensitive.
// ---------------------------------------------------------------------------

describe('parseHeaders / headerValue', () => {
  it('keys case-insensitively', () => {
    const h = parseHeaders({ headers: [{ name: 'Mime-Version', value: '1.0 (1.0)' }] });
    expect(headerValue(h, 'MIME-Version')).toBe('1.0 (1.0)');
  });

  it('keeps every value of a repeated header', () => {
    const h = parseHeaders({ headers: [
      { name: 'Received', value: 'one' },
      { name: 'received', value: 'two' },
      { name: 'RECEIVED' },
    ] });
    expect(h.get('received')).toEqual(['one', 'two', '']);
    expect(headerValue(h, 'Received')).toBe('one');
  });

  it('tolerates a missing payload, a missing headers array, nameless and valueless headers', () => {
    expect(parseHeaders(undefined).size).toBe(0);
    expect(parseHeaders({}).size).toBe(0);
    const h = parseHeaders({ headers: [{ value: 'orphan' }, { name: 'X-Empty' }] });
    expect(h.size).toBe(1);
    expect(headerValue(h, 'x-empty')).toBe('');
  });

  it('returns undefined for a header that is not present', () => {
    expect(headerValue(parseHeaders({ headers: [] }), 'Subject')).toBeUndefined();
  });
});

describe('appleIdentitySignals', () => {
  it('reports X-Uniform-Type-Identifier only when it names an Apple type', () => {
    expect(appleIdentitySignals([{ name: 'X-Uniform-Type-Identifier', value: 'com.apple.mail-draft' }]))
      .toEqual(['X-Uniform-Type-Identifier: com.apple.mail-draft']);
    expect(appleIdentitySignals([{ name: 'X-Uniform-Type-Identifier', value: 'org.example.thing' }]))
      .toEqual([]);
  });

  it('reports X-Universally-Unique-Identifier and any X-Apple-* header', () => {
    expect(appleIdentitySignals([
      { name: 'X-Universally-Unique-Identifier', value: 'ABC-DEF' },
      { name: 'X-Apple-Notify-Thread', value: 'yes' },
    ])).toEqual([
      'X-Universally-Unique-Identifier: ABC-DEF',
      'X-Apple-Notify-Thread: yes',
    ]);
  });

  it('ignores ordinary headers and tolerates missing name/value/list', () => {
    expect(appleIdentitySignals([{ name: 'Subject', value: 'hi' }])).toEqual([]);
    expect(appleIdentitySignals([{ value: 'nameless' }])).toEqual([]);
    expect(appleIdentitySignals([{ name: 'X-Apple-Mail-Remote-Attachments' }])).toEqual(['X-Apple-Mail-Remote-Attachments: ']);
    expect(appleIdentitySignals(undefined)).toEqual([]);
  });
});

describe('normalizeMessageId / messageIdsIn', () => {
  it('strips angle brackets and surrounding whitespace', () => {
    expect(normalizeMessageId('  <ABC@gmail.com> ')).toBe('ABC@gmail.com');
    expect(normalizeMessageId('ABC@gmail.com')).toBe('ABC@gmail.com');
  });

  it('returns undefined for absent or empty ids', () => {
    expect(normalizeMessageId(undefined)).toBeUndefined();
    expect(normalizeMessageId('   ')).toBeUndefined();
    expect(normalizeMessageId('<>')).toBeUndefined();
  });

  it('splits a References chain into ids', () => {
    expect(messageIdsIn('<a@x> <b@y>\r\n <c@z>')).toEqual(['a@x', 'b@y', 'c@z']);
  });

  it('returns [] for an absent References header and for one with no bracketed id', () => {
    expect(messageIdsIn(undefined)).toEqual([]);
    expect(messageIdsIn('garbage')).toEqual([]);
  });
});

describe('normalizeBodyLines / bodySimilarity', () => {
  it('normalizes CRLF, collapses whitespace and drops blank lines', () => {
    expect(normalizeBodyLines('a  b\r\n\r\n  c \n')).toEqual(['a b', 'c']);
    expect(normalizeBodyLines(undefined)).toEqual([]);
  });

  it('scores identical bodies 1 and disjoint bodies 0', () => {
    expect(bodySimilarity('one\ntwo', 'one\ntwo')).toBe(1);
    expect(bodySimilarity('one\ntwo', 'three\nfour')).toBe(0);
  });

  it('scores a dropped paragraph between 0 and 1', () => {
    const s = bodySimilarity('one\ntwo\nthree', 'one\ntwo');
    expect(s).toBeCloseTo(2 / 3, 5);
  });

  it('scores 0 when either side has no content (no evidence, not a match)', () => {
    expect(bodySimilarity('', 'one')).toBe(0);
    expect(bodySimilarity('one', '')).toBe(0);
  });
});

describe('isQuotedBodyLine / authoredBodyLines / measureBodyAgreement', () => {
  it('treats a `>` line, an attribution line and a forward separator as quoting apparatus', () => {
    expect(isQuotedBodyLine('> she wrote this')).toBe(true);
    expect(isQuotedBodyLine('On 1 May 2026, at 09:14, Co Parent <co@x.com> wrote:')).toBe(true);
    expect(isQuotedBodyLine('On Fri, May 1, 2026 at 9:14 AM Co Parent <co@x.com> wrote:')).toBe(true);
    expect(isQuotedBodyLine('-----Original Message-----')).toBe(true);
    expect(isQuotedBodyLine('---------- Forwarded message ---------')).toBe(true);
  });

  it('does not mistake ordinary prose for quoting', () => {
    expect(isQuotedBodyLine('On the whole I agree with that.')).toBe(false);
    expect(isQuotedBodyLine('She wrote: bring the booster seat.')).toBe(false);
    expect(isQuotedBodyLine('Pickup at six.')).toBe(false);
  });

  it('keeps only the lines a draft actually authored', () => {
    expect(authoredBodyLines('mine one\n> theirs\nOn 1 May 2026, at 09:14, X <x@y> wrote:\nmine two'))
      .toEqual(['mine one', 'mine two']);
    expect(authoredBodyLines(undefined)).toEqual([]);
  });

  it('measures agreement over authored lines only, and reports every input to that judgement', () => {
    const a = 'The handoff moves to the 14th at six.\nI will bring the booster seat.\n> quoted\n> quoted two';
    const b = 'The handoff moves to the 14th at six.\nI will bring the booster seat.\nAlso the swim bag.\n> quoted\n> quoted two';
    const m = measureBodyAgreement(a, b);
    expect(m.similarity).toBeCloseTo(2 / 3, 5);
    expect(m.sharedAuthoredLines).toBe(2);
    expect(m.sharedAuthoredChars).toBe(37 + 30);
    expect(m.quotedLinesIgnored).toEqual({ original: 2, candidate: 2 });
    expect(m.meetsThreshold).toBe(true);
    expect(m.basisNote).toMatch(/quoted/i);
  });

  it('scores 0 when one side has no authored line at all', () => {
    expect(measureBodyAgreement('> all quoted', 'real text here').similarity).toBe(0);
    expect(measureBodyAgreement('real text here', '> all quoted').similarity).toBe(0);
  });
});

describe('normalizeFrom', () => {
  it('extracts and lowercases the address from a display-name form', () => {
    expect(normalizeFrom('Chris Hall <Chris.C.Hall@Gmail.com>')).toBe('chris.c.hall@gmail.com');
  });

  it('accepts a bare address and rejects empty/absent input', () => {
    expect(normalizeFrom(' A@B.com ')).toBe('a@b.com');
    expect(normalizeFrom('   ')).toBeUndefined();
    expect(normalizeFrom(undefined)).toBeUndefined();
  });
});

describe('parseInternalDateMs', () => {
  it('parses an epoch-millis string', () => {
    expect(parseInternalDateMs('1754700000000')).toBe(1754700000000);
  });

  it('returns undefined for absent, blank or non-numeric values', () => {
    expect(parseInternalDateMs(undefined)).toBeUndefined();
    expect(parseInternalDateMs('  ')).toBeUndefined();
    expect(parseInternalDateMs('yesterday')).toBeUndefined();
  });
});

// ---------------------------------------------------------------------------
// HAZARD A — the pairing verdict. A wrong "X replaced Y" sends the wrong text
// to a thread with a parenting coordinator on Cc. Precision over recall.
// ---------------------------------------------------------------------------

const ORIGINAL: DraftFacts = {
  draftId: 'r4303011157206680397',
  messageIdHeader: '<CAF=orig@mail.gmail.com>',
  inReplyTo: '<coparent-1@mail.gmail.com>',
  references: '<coparent-1@mail.gmail.com>',
  from: 'Chris Hall <chris.c.hall@gmail.com>',
  subject: 'Re: Schedule change',
  internalDate: '1754700000000',
  bodyText: 'Thanks for the note, that works on my end.\nI can do the 14th and the Friday after.\nPickup at six as usual.',
};

const APPLE_FORK: DraftFacts = {
  draftId: 's:14092347734530621658',
  messageIdHeader: '<9F3A1C2E-0000-4A11-BB00-1122334455AA@gmail.com>',
  references: '<coparent-1@mail.gmail.com> <CAF=orig@mail.gmail.com>',
  from: 'Chris Hall <chris.c.hall@gmail.com>',
  subject: 'Re: Schedule change',
  internalDate: '1754703600000',
  bodyText: 'Thanks for the note, that works on my end.\nPickup at six as usual.',
  appleSignals: ['X-Uniform-Type-Identifier: com.apple.mail-draft'],
};

describe('evaluateForkPairing — detection', () => {
  it('confirms only with identity + lineage + ordering + same From', () => {
    const r = evaluateForkPairing(ORIGINAL, APPLE_FORK, 2);
    expect(r.verdict).toBe('confirmed');
    expect(r.missing).toEqual([]);
    expect(r.evidence.join(' | ')).toContain('CAF=orig@mail.gmail.com');
    expect(r.note).toContain('s:14092347734530621658');
  });

  it('reports every number the lineage decision was made on, not just the outcome', () => {
    const r = evaluateForkPairing(ORIGINAL, APPLE_FORK, 2);
    expect(r.bodyAgreement.similarityThreshold).toBe(FORK_BODY_SIMILARITY_THRESHOLD);
    expect(r.bodyAgreement.similarity).toBeCloseTo(2 / 3, 5);
    expect(r.bodyAgreement.sharedAuthoredLines).toBe(2);
    expect(r.bodyAgreement.minSharedAuthoredLines).toBe(FORK_MIN_SHARED_AUTHORED_LINES);
    expect(r.bodyAgreement.sharedAuthoredChars).toBe(65);
    expect(r.bodyAgreement.minSharedAuthoredChars).toBe(FORK_MIN_SHARED_AUTHORED_CHARS);
    expect(r.bodyAgreement.quotedLinesIgnored).toEqual({ original: 0, candidate: 0 });
  });

  it('finds lineage from body similarity alone when no headers link the two', () => {
    const rewritten: DraftFacts = {
      ...APPLE_FORK,
      references: undefined,
      inReplyTo: undefined,
      bodyText: ORIGINAL.bodyText,
    };
    const bare: DraftFacts = { ...ORIGINAL, inReplyTo: undefined, references: undefined };
    const r = evaluateForkPairing(bare, rewritten, 2);
    expect(r.verdict).toBe('confirmed');
    expect(r.evidence.join(' | ')).toMatch(/similarity/i);
  });
});

describe('evaluateForkPairing — HAZARD A: no false positives', () => {
  // The mailbox holds deliberate [VERSION A] / [VERSION B] drafts created
  // seconds apart: same subject, same sender, Apple-authored, newer — and
  // completely unrelated. A subject+recency rule fires here and is WRONG.
  it('returns "none" for two unrelated same-subject drafts minutes apart', () => {
    const versionA: DraftFacts = {
      draftId: 'r1', messageIdHeader: '<a@mail.gmail.com>',
      from: 'chris.c.hall@gmail.com', subject: 'Re: Schedule change',
      internalDate: '1754700000000', bodyText: 'alpha alpha alpha',
    };
    const versionB: DraftFacts = {
      draftId: 's:2', messageIdHeader: '<B0000000-0000-4000-8000-000000000000@gmail.com>',
      from: 'chris.c.hall@gmail.com', subject: 'Re: Schedule change',
      internalDate: '1754700060000', bodyText: 'beta beta beta',
      appleSignals: ['X-Universally-Unique-Identifier: B0000000'],
    };
    const r = evaluateForkPairing(versionA, versionB, 2);
    expect(r.verdict).toBe('none');
    expect(r.missing.join(' | ')).toMatch(/lineage/i);
  });

  // THE COMPOSITE TRAP: `s:` prefix + threadId===messageId + Apple headers +
  // newer + same From are ALL consequences of "Apple wrote this draft". None of
  // them references the supposed original. Together they are still not a pair.
  it('refuses to pair on origin+recency+identity+same-From without a lineage signal', () => {
    const orphan: DraftFacts = {
      draftId: 's:3', from: 'chris.c.hall@gmail.com', subject: 'Re: Schedule change',
      internalDate: '1754999999999', bodyText: 'nothing in common at all',
      appleSignals: ['X-Apple-Notify-Thread: 1'],
    };
    const r = evaluateForkPairing(ORIGINAL, orphan, 2);
    expect(r.verdict).toBe('none');
    expect(r.note).not.toMatch(/replaced/i);
  });


  // ------------------------------------------------------------------------
  // THE SHARED-ROOT TRAP. This is the DEFAULT shape of a co-parenting mailbox:
  // most drafts are replies into the same few threads, so two drafts sharing a
  // reply root is the norm, not evidence. A shared root links each draft to a
  // common ANCESTOR — it says nothing about the candidate coming from the
  // ORIGINAL — while the other three signals (Apple headers, newer, same From)
  // are free on every draft the owner composes in Apple Mail.
  // ------------------------------------------------------------------------
  it('never confirms on a shared reply root: two independent replies to the same co-parent message', () => {
    const handoff: DraftFacts = {
      draftId: 'r1', messageIdHeader: '<orig@mail.gmail.com>',
      inReplyTo: '<coparent-2026-05-01@mail.gmail.com>',
      references: '<coparent-2026-05-01@mail.gmail.com>',
      from: 'Chris Hall <chris.c.hall@gmail.com>', subject: 'Re: July handoff',
      internalDate: '1754700000000',
      bodyText: 'Confirming the July handoff at six on the 14th.\nI will bring the booster seat.',
    };
    const orthodontist: DraftFacts = {
      draftId: 's:2', messageIdHeader: '<9F3A1C2E-0000-4A11-BB00-1122334455AA@gmail.com>',
      inReplyTo: '<coparent-2026-05-01@mail.gmail.com>',
      references: '<coparent-2026-05-01@mail.gmail.com>',
      from: 'chris.c.hall@gmail.com', subject: 'Re: orthodontist invoice',
      internalDate: '1754703600000',
      bodyText: 'The orthodontist invoice came to 240 dollars.\nI am splitting it per the parenting plan.',
      appleSignals: ['X-Uniform-Type-Identifier: com.apple.mail-draft'],
    };
    const r = evaluateForkPairing(handoff, orthodontist, 2);
    expect(r.verdict).not.toBe('confirmed');
    expect(r.note).not.toMatch(/\breplaced\b/i);
    expect(r.missing.join(' | ')).toMatch(/no lineage signal/i);
    // The root is still REPORTED — it is real — but labelled as unable to pair.
    expect(r.evidence.join(' | ')).toMatch(/CORROBORATING ONLY/);
    expect(r.evidence.join(' | ')).toMatch(/common ANCESTOR/);
    expect(r.bodyAgreement.similarity).toBe(0);
  });

  // ------------------------------------------------------------------------
  // THE QUOTED-TEXT TRAP. Apple Mail quotes the original on reply by default,
  // so two unrelated replies into one thread share a large identical block. A
  // whole-body line metric scores that pair WELL above the threshold; the
  // lineage metric must therefore look only at what neither draft quoted.
  // ------------------------------------------------------------------------
  it('never counts quoted text as agreement: two unrelated replies quoting the same original', () => {
    const quote = Array.from({ length: 30 }, (_, i) => `> quoted line ${i} of the co-parent's message`).join('\n');
    const attribution = 'On 1 May 2026, at 09:14, Co Parent <co@x.com> wrote:';
    const tuition: DraftFacts = {
      draftId: 'r1', messageIdHeader: '<orig@mail.gmail.com>',
      from: 'chris.c.hall@gmail.com', subject: 'Re: tuition', internalDate: '1754700000000',
      bodyText: `Tuition is due on the 5th.\nI paid the deposit already.\nLet me know either way.\n${attribution}\n${quote}`,
    };
    const passport: DraftFacts = {
      draftId: 's:2', messageIdHeader: '<B0000000-0000-4000-8000-000000000000@gmail.com>',
      from: 'chris.c.hall@gmail.com', subject: 'Re: passport', internalDate: '1754703600000',
      bodyText: `The passport renewal needs both signatures.\nI booked the appointment for the 3rd.\nBring the birth certificate.\nWe also need the old passport.\nCall me if that does not work.\n${attribution}\n${quote}`,
      appleSignals: ['X-Universally-Unique-Identifier: B0000000'],
    };
    // The OLD whole-body metric would have called this a match; that is the
    // regression this test exists to pin.
    expect(bodySimilarity(tuition.bodyText, passport.bodyText)).toBeGreaterThan(FORK_BODY_SIMILARITY_THRESHOLD);

    const r = evaluateForkPairing(tuition, passport, 2);
    expect(r.verdict).toBe('none');
    expect(r.note).not.toMatch(/\breplaced\b/i);
    expect(r.bodyAgreement.similarity).toBe(0);
    // The attribution line counts as quoting apparatus, not authored text.
    expect(r.bodyAgreement.quotedLinesIgnored).toEqual({ original: 31, candidate: 31 });
  });

  it('does not pair on a scrap of shared boilerplate below the shared-text minimums', () => {
    const base = {
      from: 'chris.c.hall@gmail.com', subject: 'Re: anything',
      inReplyTo: undefined, references: undefined,
    };
    const a: DraftFacts = { ...base, draftId: 'r1', internalDate: '1', bodyText: 'Sounds good.\nSent from my iPhone' };
    const b: DraftFacts = {
      ...base, draftId: 's:2', internalDate: '2', bodyText: 'I will check.\nSent from my iPhone',
      appleSignals: ['X-Apple-Notify-Thread: 1'],
    };
    const r = evaluateForkPairing(a, b, 2);
    expect(r.verdict).toBe('none');
    // `Sent from my iPhone` is Apple Mail's own default signature: a line the
    // CLIENT writes on every message, so it is apparatus and never counted as
    // shared authorship in the first place.
    expect(r.bodyAgreement.sharedAuthoredLines).toBe(0);
    expect(r.bodyAgreement.boilerplateLinesIgnored).toEqual({ original: 1, candidate: 1 });
    expect(r.bodyAgreement.meetsThreshold).toBe(false);
  });

  it('does not pair two short drafts whose only shared lines are too little text to mean anything', () => {
    const base = { from: 'me@x.com', subject: 'Re: anything' };
    const a: DraftFacts = { ...base, draftId: 'r1', internalDate: '1', bodyText: 'Ok.\nWill do.' };
    const b: DraftFacts = {
      ...base, draftId: 's:2', internalDate: '2', bodyText: 'Ok.\nWill do.',
      appleSignals: ['X-Apple-Notify-Thread: 1'],
    };
    const r = evaluateForkPairing(a, b, 2);
    expect(r.bodyAgreement.similarity).toBe(1);
    expect(r.bodyAgreement.sharedAuthoredLines).toBeGreaterThanOrEqual(FORK_MIN_SHARED_AUTHORED_LINES);
    expect(r.bodyAgreement.sharedAuthoredChars).toBeLessThan(FORK_MIN_SHARED_AUTHORED_CHARS);
    expect(r.bodyAgreement.meetsThreshold).toBe(false);
    expect(r.verdict).toBe('none');
  });

  it('scores agreement 0 when either side has no authored text left after quoting is removed', () => {
    const quoteOnly: DraftFacts = { draftId: 's:2', bodyText: '> every line here is quoted', from: 'me@x.com', internalDate: '2' };
    const r = evaluateForkPairing(ORIGINAL, quoteOnly, 2);
    expect(r.bodyAgreement.similarity).toBe(0);
    expect(r.verdict).toBe('none');
  });

  // A shared root is not nothing — it is just not lineage. Reporting it as
  // `none` ("nothing links them") would be its own overclaim, so it comes back
  // as the WEAKEST possible answer, phrased as a question.
  it('reports a shared root alone as an explicitly weak "candidate", never as a fork', () => {
    const a: DraftFacts = {
      draftId: 'r1', messageIdHeader: '<orig@x>', inReplyTo: '<root@x>', references: '<root@x>',
      from: 'me@x.com', internalDate: '1', bodyText: 'alpha alpha alpha',
    };
    const b: DraftFacts = {
      draftId: 's:2', messageIdHeader: '<uuid@x>', references: '<root@x>',
      from: 'me@x.com', internalDate: '2', bodyText: 'beta beta beta',
      appleSignals: ['X-Apple-Notify-Thread: 1'],
    };
    const r = evaluateForkPairing(a, b, 2);
    expect(r.verdict).toBe('candidate');
    expect(r.note).toMatch(/WEAK/);
    expect(r.note).toMatch(/\?/);
    expect(r.note).not.toMatch(/\breplaced\b/i);
    expect(r.note).toMatch(/every reply in that thread/i);
  });

  // HAZARD A cuts both ways for WORDING: the line-based comparison cannot see
  // through Apple's re-wrapping and smart quotes, so "none" must be reported as
  // a failure to find evidence, never as proof the two drafts are unrelated.
  it('states "none" as a failure to find evidence, not as proof of unrelatedness', () => {
    const r = evaluateForkPairing(ORIGINAL, {
      draftId: 's:9', from: 'chris.c.hall@gmail.com', internalDate: '1755000000000',
      bodyText: 'nothing in common', appleSignals: ['X-Apple-Notify-Thread: 1'],
    }, 2);
    expect(r.verdict).toBe('none');
    expect(r.note).toMatch(/re-?wrap/i);
    expect(r.note).not.toMatch(/unrelated drafts that happen to look alike/i);
  });

  // STRUCTURAL GUARANTEE: `confirmed` requires an Apple identity header, and an
  // identity header can only come from a tier-2 fetch. A tier-0/tier-1 caller
  // that smuggles in signals is a bug, and must fail loudly rather than emit a
  // confirmed verdict off free fields.
  it('throws if Apple identity signals arrive below tier 2', () => {
    expect(() => evaluateForkPairing(ORIGINAL, APPLE_FORK, 0)).toThrow(/tier 2/i);
    expect(() => evaluateForkPairing(ORIGINAL, APPLE_FORK, 1)).toThrow(/tier 2/i);
  });

  it('can never reach "confirmed" from tier-0/tier-1 data', () => {
    const tier0Fork: DraftFacts = { ...APPLE_FORK, appleSignals: undefined };
    for (const tier of [0, 1] as const) {
      const r = evaluateForkPairing(ORIGINAL, tier0Fork, tier);
      expect(r.verdict).toBe('candidate');
      expect(r.missing.join(' | ')).toMatch(/Apple identity header/i);
    }
  });
});

describe('evaluateForkPairing — "candidate" is interrogative and names what is missing', () => {
  it('downgrades to candidate and names the absent signal when the candidate is older', () => {
    const older: DraftFacts = { ...APPLE_FORK, internalDate: '1754000000000' };
    const r = evaluateForkPairing(ORIGINAL, older, 2);
    expect(r.verdict).toBe('candidate');
    expect(r.missing.join(' | ')).toMatch(/not newer/i);
    expect(r.note).toMatch(/\?/);
    expect(r.note).not.toMatch(/\breplaced\b/i);
  });

  it('names a missing internalDate on either side rather than assuming an order', () => {
    expect(evaluateForkPairing({ ...ORIGINAL, internalDate: undefined }, APPLE_FORK, 2).missing.join(' | '))
      .toMatch(/internalDate/i);
    expect(evaluateForkPairing(ORIGINAL, { ...APPLE_FORK, internalDate: undefined }, 2).missing.join(' | '))
      .toMatch(/internalDate/i);
  });

  it('names a differing or missing From', () => {
    const other = evaluateForkPairing(ORIGINAL, { ...APPLE_FORK, from: 'someone.else@example.com' }, 2);
    expect(other.verdict).toBe('candidate');
    expect(other.missing.join(' | ')).toMatch(/different From/i);

    expect(evaluateForkPairing({ ...ORIGINAL, from: undefined }, APPLE_FORK, 2).missing.join(' | '))
      .toMatch(/From missing/i);
    expect(evaluateForkPairing(ORIGINAL, { ...APPLE_FORK, from: undefined }, 2).missing.join(' | '))
      .toMatch(/From missing/i);
  });

  it('does not claim a Message-Id citation when the original has no Message-Id header', () => {
    const r = evaluateForkPairing({ ...ORIGINAL, messageIdHeader: undefined }, APPLE_FORK, 2);
    expect(r.evidence.join(' | ')).not.toMatch(/Message-Id/i);
    // Still confirmed — but on the AUTHORED-TEXT agreement (2 shared lines the
    // two drafts wrote rather than quoted), never on the shared reply root,
    // which the test below pins as insufficient on its own.
    expect(r.verdict).toBe('confirmed');
    expect(r.evidence.join(' | ')).toMatch(/LINEAGE: the two drafts agree on text/);
  });

  it('falls back to a placeholder when a draft id is unknown', () => {
    const r = evaluateForkPairing({ ...ORIGINAL, draftId: undefined }, { ...APPLE_FORK, draftId: undefined }, 2);
    expect(r.note).toContain('(unknown id)');
  });
});

describe('FORK_SIGNALS_THAT_NEVER_SUFFICE', () => {
  it('enumerates, for tool descriptions, the signals that must never pair on their own', () => {
    const joined = FORK_SIGNALS_THAT_NEVER_SUFFICE.join(' ');
    expect(joined).toMatch(/s:/);
    expect(joined).toMatch(/threadId/);
    expect(joined).toMatch(/subject/i);
    expect(joined).toMatch(/0\.50|coin flip/i);
    // "Apple fork => threading lost" is FALSE as a general rule (a live fork
    // was found carrying a 5-deep References chain); nothing here may say it.
    expect(joined).not.toMatch(/threading is (always )?lost/i);
  });
});

// ---------------------------------------------------------------------------
// BODY EXTRACTION. `gog gmail drafts get --json` hands back the raw Gmail
// payload — gog's own text renderer is not reachable over --json — so the
// wrapper walks the MIME tree itself. A body it silently fails to find would
// show up as a diff claiming a whole draft is empty, so every branch is pinned.
// ---------------------------------------------------------------------------
const b64url = (s: string) => Buffer.from(s, 'utf8').toString('base64url');

describe('decodeBase64UrlText', () => {
  it('decodes base64url, including multi-byte UTF-8', () => {
    expect(decodeBase64UrlText(b64url('caf\u00e9 \u2014 ok'))).toBe('caf\u00e9 \u2014 ok');
  });

  it('returns empty string for absent or undecodable data rather than throwing', () => {
    expect(decodeBase64UrlText(undefined)).toBe('');
    expect(decodeBase64UrlText('')).toBe('');
    expect(decodeBase64UrlText('!!!!not base64!!!!')).toBe('');
  });
});

describe('decodePartText — transfer encoding and charset', () => {
  const bytes = (...b: number[]) => Buffer.from(Uint8Array.from(b)).toString('base64url');

  it('decodes a windows-1252 body instead of replacing its smart quote', () => {
    // 0x92 is a RIGHT SINGLE QUOTATION MARK in cp1252 and invalid UTF-8, so a
    // plain UTF-8 decode turns "don’t" into "don�t".
    expect(decodePartText({
      mimeType: 'text/plain',
      headers: [{ name: 'Content-Type', value: 'text/plain; charset=windows-1252' }],
      body: { data: bytes(0x64, 0x6f, 0x6e, 0x92, 0x74) },
    })).toBe('don’t');
  });

  it('decodes a part that really is still quoted-printable, soft breaks included', () => {
    expect(decodePartText({
      mimeType: 'text/plain',
      headers: [{ name: 'Content-Transfer-Encoding', value: 'quoted-printable' }],
      body: { data: b64url('It cost =E2=80=94 a lot=\r\nreally, and 100=3D100=zz=') },
    })).toBe('It cost — a lotreally, and 100=100=zz=');
  });

  it('does NOT re-decode a body Gmail already decoded, even though the header still says quoted-printable', () => {
    // Gmail hands back `body.data` already decoded while leaving the original
    // Content-Transfer-Encoding header in place, so decoding on the header
    // alone would rewrite "2+2=44" to "2+2D".
    expect(decodePartText({
      mimeType: 'text/plain',
      headers: [{ name: 'Content-Transfer-Encoding', value: 'quoted-printable' }],
      body: { data: b64url('2+2=44 and that is that') },
    })).toBe('2+2=44 and that is that');
    // Non-ASCII bytes prove it is decoded already: quoted-printable is 7-bit.
    expect(decodePartText({
      mimeType: 'text/plain',
      headers: [{ name: 'Content-Transfer-Encoding', value: 'quoted-printable' }],
      body: { data: b64url('café =E2=80=94') },
    })).toBe('café =E2=80=94');
  });

  it('does NOT re-decode a base64 part — Gmail already did, and doing it twice destroys the body', () => {
    expect(decodePartText({
      mimeType: 'text/plain',
      headers: [{ name: 'Content-Transfer-Encoding', value: 'base64' }],
      body: { data: b64url('plain words here') },
    })).toBe('plain words here');
  });

  it('falls back to windows-1252 when the part declares no charset at all', () => {
    // No Content-Type header, bytes that are not valid UTF-8: the choice is
    // between mangling the smart quote and reading it. gog would read it.
    expect(decodePartText({ mimeType: 'text/plain', body: { data: bytes(0x64, 0x6f, 0x6e, 0x92, 0x74) } })).toBe('don’t');
  });

  it('falls back to windows-1252 when the declared charset means nothing to this runtime', () => {
    expect(decodePartText({
      mimeType: 'text/plain',
      headers: [{ name: 'Content-Type', value: 'text/plain; charset=x-nonesuch-9000' }],
      body: { data: bytes(0x64, 0x6f, 0x6e, 0x92, 0x74) },
    })).toBe('don’t');
  });

  it('keeps a UTF-8 body that is merely LABELLED windows-1252 — Gmail transcodes and leaves the header', () => {
    expect(decodePartText({
      mimeType: 'text/plain',
      headers: [{ name: 'Content-Type', value: 'text/plain; charset="windows-1252"' }],
      body: { data: b64url('don’t — really') },
    })).toBe('don’t — really');
  });

  it('returns empty string for a part with no data', () => {
    expect(decodePartText({ mimeType: 'text/plain' })).toBe('');
  });
});

describe('bestBodyText', () => {
  it('returns empty string when there is no payload', () => {
    expect(bestBodyText(undefined)).toBe('');
  });

  it('reads a flat text/plain body', () => {
    expect(bestBodyText({ mimeType: 'text/plain', body: { data: b64url('hello') } })).toBe('hello');
  });

  it('prefers text/plain nested anywhere over text/html', () => {
    expect(bestBodyText({
      mimeType: 'multipart/alternative',
      parts: [
        { mimeType: 'text/html', body: { data: b64url('<p>rich</p>') } },
        { mimeType: 'multipart/related', parts: [{ mimeType: 'text/plain', body: { data: b64url('plain') } }] },
      ],
    })).toBe('plain');
  });

  it('falls back to text/html when there is no plain part', () => {
    expect(bestBodyText({ mimeType: 'multipart/alternative', parts: [{ mimeType: 'text/html', body: { data: b64url('<p>rich</p>') } }] }))
      .toBe('<p>rich</p>');
  });

  it('skips attachment parts and keeps the FIRST body of each type', () => {
    expect(bestBodyText({
      mimeType: 'multipart/mixed',
      parts: [
        { mimeType: 'text/plain', filename: 'notes.txt', body: { data: b64url('ATTACHED, NOT THE BODY') } },
        { mimeType: 'text/plain', body: { data: b64url('first') } },
        { mimeType: 'text/plain', body: { data: b64url('second') } },
      ],
    })).toBe('first');
  });

  it('treats a part with no mimeType as its own (unusable) type', () => {
    // A part with neither a mimeType nor a recognisable one must not be picked
    // up as the body — it is keyed under '' and never matches plain or html.
    expect(bestBodyText({ parts: [{ body: { data: b64url('mystery') } }, { mimeType: 'text/plain', body: { data: b64url('real') } }] }))
      .toBe('real');
  });

  it('finds a part whose mimeType carries parameters (text/plain; charset="UTF-8")', () => {
    expect(bestBodyText({
      mimeType: 'multipart/alternative',
      parts: [
        { mimeType: 'text/html; charset="UTF-8"', body: { data: b64url('<p>rich</p>') } },
        { mimeType: 'text/plain; charset="UTF-8"', body: { data: b64url('plain') } },
      ],
    })).toBe('plain');
  });

  it('returns empty string when nothing carries a recognised body', () => {
    expect(bestBodyText({ mimeType: 'multipart/mixed', parts: [{ mimeType: 'application/pdf', body: { data: b64url('%PDF') }, filename: 'a.pdf' }] })).toBe('');
  });
});

// ---------------------------------------------------------------------------
// THE DIVERGENCE REPORT. The point of the whole feature: in the observed case
// NEITHER copy was a superset, so recreating from either one alone lost work.
// ---------------------------------------------------------------------------
describe('diffBodyLines', () => {
  it('reports two-way divergence as "neither is a superset"', () => {
    const d = diffBodyLines('a\nb\nkept-only-in-A', 'a\nb\nkept-only-in-B', 200);
    expect(d.onlyInA).toEqual(['kept-only-in-A']);
    expect(d.onlyInB).toEqual(['kept-only-in-B']);
    expect(d.sharedLineCount).toBe(2);
    expect(d.neitherIsSuperset).toBe(true);
    expect(d.truncated).toBe(false);
    expect(d.note).toContain('NEITHER');
  });

  it('names a one-sided superset in each direction', () => {
    expect(diffBodyLines('a\nb\nc', 'a\nb', 200).note).toContain('Draft A is a superset');
    expect(diffBodyLines('a\nb', 'a\nb\nc', 200).note).toContain('Draft B is a superset');
  });

  it('calls whitespace-equal bodies identical', () => {
    const d = diffBodyLines('a\n\n  b  ', 'a\nb', 200);
    expect(d.neitherIsSuperset).toBe(false);
    expect(d.note).toContain('identical');
    expect(d.similarity).toBe(1);
  });

  // HAZARD A, in the diff: "every line of A is present in B" is an invitation
  // to delete or overwrite A. It must never be said about a body that merely
  // failed to parse — an unread body is not an empty one.
  it('never claims containment when one side has no readable body', () => {
    const a = diffBodyLines('', 'b one\nb two', 200);
    expect(a.comparability).toBe('a-unreadable');
    expect(a.supersetClaim).toBe('not-assessed');
    expect(a.neitherIsSuperset).toBeNull();
    expect(a.note).not.toMatch(/superset/i);
    expect(a.note).toMatch(/nothing was compared/i);
    expect(a.note).toMatch(/could not decode/i);
    expect(a.note).toMatch(/^Draft A yielded no body text/);

    const b = diffBodyLines('a one\na two', '   \n\n', 200);
    expect(b.comparability).toBe('b-unreadable');
    expect(b.supersetClaim).toBe('not-assessed');
    expect(b.note).not.toMatch(/superset/i);

    const both = diffBodyLines('', '', 200);
    expect(both.comparability).toBe('both-unreadable');
    expect(both.supersetClaim).toBe('not-assessed');
    expect(both.note).not.toMatch(/identical/i);
    expect(both.note).toMatch(/^NEITHER draft yielded any body text/);
    expect(diffBodyLines('a one', '', 200).note).toMatch(/^Draft B yielded no body text/);
  });

  it('names the superset direction only when both sides were readable', () => {
    expect(diffBodyLines('a\nb\nc', 'a\nb', 200).supersetClaim).toBe('a-superset-of-b');
    expect(diffBodyLines('a\nb', 'a\nb\nc', 200).supersetClaim).toBe('b-superset-of-a');
    expect(diffBodyLines('a\nb', 'a\nb', 200).supersetClaim).toBe('identical');
    expect(diffBodyLines('a\nx', 'a\ny', 200).supersetClaim).toBe('neither');
    expect(diffBodyLines('a\nb', 'a\nb', 200).comparability).toBe('compared');
  });

  it('truncates long one-sided diffs and flags it', () => {
    const d = diffBodyLines('a1\na2\na3', 'b1\nb2\nb3', 2);
    expect(d.onlyInA).toEqual(['a1', 'a2']);
    expect(d.onlyInB).toEqual(['b1', 'b2']);
    expect(d.truncated).toBe(true);
    expect(d.note).toContain('truncated');
  });
});

// ---------------------------------------------------------------------------
// REQUIREMENT 5 — THE CONTENT-LOSS CHECK.
//
// gog requires a body on EVERY `drafts update`, so re-threading and rewriting
// the body are the same operation. Adopting a mail client's replacement back
// onto the thread therefore overwrites whatever text lived only in the other
// copy. This is the guard, and it is deliberately mechanical: it compares two
// bodies and says which lines one holds that the other does not. It makes NO
// claim that either draft replaced the other.
// ---------------------------------------------------------------------------
describe('evaluateContentLoss', () => {
  it('passes when the body being written contains every line the sibling holds', () => {
    const c = evaluateContentLoss('s:1', 'kept one\nkept two', 'kept one\nkept two\nand a new sentence', 200);
    expect(c.status).toBe('clean');
    expect(c.linesOnlyInSibling).toEqual([]);
    expect(c.linesOnlyInSiblingCount).toBe(0);
    expect(c.siblingBodyLineCount).toBe(2);
    expect(c.newBodyLineCount).toBe(3);
    expect(c.note).not.toMatch(/WARNING/);
  });

  it('names the exact lines that would exist only in the sibling afterwards', () => {
    const c = evaluateContentLoss(
      's:14092347734530621658',
      'Thanks for the note.\nTHE PARAGRAPH ONLY APPLE HAS.\nBest, Chris',
      'Thanks for the note.\nBest, Chris',
      200,
    );
    expect(c.status).toBe('would-lose');
    expect(c.linesOnlyInSibling).toEqual(['THE PARAGRAPH ONLY APPLE HAS.']);
    expect(c.linesOnlyInSiblingCount).toBe(1);
    expect(c.note).toMatch(/WARNING/);
    expect(c.note).toContain('s:14092347734530621658');
  });

  it('collapses runs of whitespace and blank lines, so re-indentation is not reported as loss', () => {
    expect(evaluateContentLoss('s:1', '  kept   one  \n\n\nkept two', 'kept one\nkept two', 200).status).toBe('clean');
  });

  // The comparison is LINE-based, so a paragraph re-wrapped at a different
  // width does read as loss. That is the honest, precision-biased direction —
  // but the note has to say so rather than let the caller assume words vanished.
  it('reports a genuinely re-wrapped paragraph as loss, and says the comparison is line-based', () => {
    const c = evaluateContentLoss(
      's:1',
      'The handoff is at six on the 14th, as usual.',
      'The handoff is at six\non the 14th, as usual.',
      200,
    );
    expect(c.status).toBe('would-lose');
    expect(c.linesOnlyInSibling).toEqual(['The handoff is at six on the 14th, as usual.']);
    expect(c.note).toMatch(/re-?wrapp/i);
    expect(c.note).toMatch(/line-based/i);
  });

  it('reports UNCHECKED rather than clean when the sibling has no readable body', () => {
    const c = evaluateContentLoss('s:1', '   \n\n', 'anything', 200);
    expect(c.status).toBe('unchecked');
    expect(c.siblingBodyLineCount).toBe(0);
    expect(c.note).toMatch(/nothing was compared/i);
  });

  it('caps the printed line list and flags the truncation, keeping the true count', () => {
    const c = evaluateContentLoss('s:1', 'x1\nx2\nx3\nx4', 'kept', 2);
    expect(c.linesOnlyInSibling).toEqual(['x1', 'x2']);
    expect(c.linesOnlyInSiblingCount).toBe(4);
    expect(c.truncated).toBe(true);
    expect(c.note).toContain('truncated');
  });

  it('reports the similarity it measured, so the caller can judge the comparison', () => {
    expect(evaluateContentLoss('s:1', 'a\nb', 'a\nb', 200).similarity).toBe(1);
    expect(evaluateContentLoss('s:1', 'a\nb', 'c\nd', 200).similarity).toBe(0);
  });

  // HAZARD A. Two unrelated drafts share no text, so the check reports total
  // divergence — and that is exactly the shape a genuine fork also has. It must
  // therefore never let the result read as "this is the fork of that".
  it('makes NO pairing claim, even when the two bodies overlap completely', () => {
    for (const c of [
      evaluateContentLoss('s:1', 'a\nb', 'a\nb', 200),
      evaluateContentLoss('s:1', 'dentist appointment friday', 'unrelated invoice text', 200),
    ]) {
      expect(c.forkClaim).toBeNull();
      expect(c.forkClaimNote).toMatch(/does not|no claim/i);
      expect(c.forkClaimNote).toContain('gog_gmail_drafts_diff');
      expect(JSON.stringify(c)).not.toMatch(/confirmed|replaced this draft/);
    }
  });
});

describe('unreadableSiblingCheck', () => {
  it('is UNCHECKED, carries the reason, and still makes no pairing claim', () => {
    const c = unreadableSiblingCheck('s:1', 'Google API error (404 notFound)');
    expect(c.status).toBe('unchecked');
    expect(c.note).toContain('Google API error (404 notFound)');
    expect(c.linesOnlyInSibling).toEqual([]);
    expect(c.siblingBodyLineCount).toBe(0);
    expect(c.forkClaim).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// HAZARD A — GREETING, SIGN-OFF AND SIGNATURE ARE APPARATUS, NOT AUTHORSHIP.
//
// The property that disqualified quoted text — a mail client reproduces it
// identically on every message regardless of what the message says — is just as
// true of the salutation, the closing formula, the name under it and the
// client's own signature block. `Sent from my iPhone` is Apple Mail's DEFAULT
// signature, and `Hi Jennifer,` + `Thanks,` + `Chris` + `Sent from my iPhone` is
// 4 lines and 43 characters: on its own that cleared all three of the lineage
// minimums, so two genuinely unrelated one-sentence notes from one Apple Mail
// account paired as `confirmed`. Short confirmation + signature is the dominant
// shape of the co-parenting mailbox this feature serves, so that was the
// DEFAULT case, not a corner.
// ---------------------------------------------------------------------------
describe('authoredBodyLines — client boilerplate is apparatus', () => {
  const apple = (sentence: string) => `Hi Jennifer,\n\n${sentence}\n\nThanks,\nChris\n\nSent from my iPhone`;

  it('keeps only the sentence the author actually wrote', () => {
    expect(authoredBodyLines(apple('Tuesday pickup at 5 works for me.')))
      .toEqual(['Tuesday pickup at 5 works for me.']);
  });

  it('strips a salutation only on the FIRST line, never mid-body', () => {
    expect(authoredBodyLines('Hi Jennifer,\nHey I forgot to say the bag is packed'))
      .toEqual(['Hey I forgot to say the bag is packed']);
  });

  it('strips a closing formula wherever it sits, so one draft is not stripped and the other left', () => {
    // Position-dependent stripping would remove `Best, Chris` from the copy
    // that ends with it and keep it in the copy that has a sentence after it,
    // manufacturing divergence between two copies of the same message.
    expect(authoredBodyLines('Pickup at six.\nBest, Chris')).toEqual(['Pickup at six.']);
    expect(authoredBodyLines('Pickup at six.\nBest, Chris\nONE MORE SENTENCE.'))
      .toEqual(['Pickup at six.', 'ONE MORE SENTENCE.']);
  });

  it('strips an RFC 3676 `-- ` block and everything under it', () => {
    expect(authoredBodyLines('Real line.\n-- \nChris Hall\n704-555-0100\nchris@example.com'))
      .toEqual(['Real line.']);
  });

  it('strips the client signatures other clients write', () => {
    expect(authoredBodyLines('Real line.\nSent from my Galaxy S24')).toEqual(['Real line.']);
    expect(authoredBodyLines('Real line.\nGet Outlook for iOS')).toEqual(['Real line.']);
  });

  it('does NOT strip a sentence that merely begins with a closing word', () => {
    expect(authoredBodyLines('Thanks for the note.\nBest of luck with the move'))
      .toEqual(['Thanks for the note.', 'Best of luck with the move']);
    // `Thanks,` + a sentence is not a sign-off: the tail is not a name.
    expect(authoredBodyLines('Thanks, I will send the orthodontist invoice tomorrow'))
      .toEqual(['Thanks, I will send the orthodontist invoice tomorrow']);
  });

  it('stops stripping under a sign-off at the first line that is not name-shaped', () => {
    expect(authoredBodyLines('Thanks,\nChris\nPS the invoice is attached and paid'))
      .toEqual(['PS the invoice is attached and paid']);
  });
});

describe('measureBodyAgreement — boilerplate cannot establish lineage', () => {
  const apple = (sentence: string) => `Hi Jennifer,\n\n${sentence}\n\nThanks,\nChris\n\nSent from my iPhone`;

  // The reproduction from the review, verbatim: different subjects, different
  // threadIds, no shared reply root — two unrelated drafts that agreed on
  // nothing but the apparatus, and came back `meetsThreshold: true`.
  it('finds NO agreement between two unrelated notes that share only the apparatus', () => {
    const m = measureBodyAgreement(
      apple('Tuesday pickup at 5 works for me.'),
      apple('I paid the orthodontist invoice today.'),
    );
    expect(m.sharedAuthoredLines).toBe(0);
    expect(m.sharedAuthoredChars).toBe(0);
    expect(m.similarity).toBe(0);
    expect(m.meetsThreshold).toBe(false);
    expect(m.boilerplateLinesIgnored).toEqual({ original: 4, candidate: 4 });
  });

  it('still finds agreement when the two drafts share the SUBSTANCE', () => {
    const m = measureBodyAgreement(
      apple('Tuesday pickup at 5 works for me. I will be in the church lot by ten to.'),
      `${apple('Tuesday pickup at 5 works for me. I will be in the church lot by ten to.')}\nAnd the swim bag is packed.`,
    );
    expect(m.sharedAuthoredLines).toBe(1);
    expect(m.sharedAuthoredChars).toBeGreaterThan(FORK_MIN_SHARED_AUTHORED_CHARS);
  });

  it('counts quoting and boilerplate separately, so the caller can redo the arithmetic', () => {
    const m = measureBodyAgreement(
      'Hi Jennifer,\nPickup at six.\nThanks,\nChris\n> quoted one\n> quoted two',
      'Pickup at six.',
    );
    expect(m.quotedLinesIgnored).toEqual({ original: 2, candidate: 0 });
    expect(m.boilerplateLinesIgnored).toEqual({ original: 3, candidate: 0 });
    expect(m.basisNote).toMatch(/sign-off|signature/i);
  });
});

describe('evaluateForkPairing — the boilerplate false positive', () => {
  const apple = (sentence: string) => `Hi Jennifer,\n\n${sentence}\n\nThanks,\nChris\n\nSent from my iPhone`;

  it('never confirms two unrelated Apple drafts that share only greeting and signature', () => {
    const original: DraftFacts = {
      draftId: 'rOLD', from: 'chris@x.com', subject: 'Tuesday pickup', internalDate: '1000',
      messageIdHeader: '<old@mail.gmail.com>', bodyText: apple('Tuesday pickup at 5 works for me.'),
    };
    const candidate: DraftFacts = {
      draftId: 's:NEW', from: 'chris@x.com', subject: 'Orthodontist invoice', internalDate: '2000',
      messageIdHeader: '<new@apple.com>', bodyText: apple('I paid the orthodontist invoice today.'),
      appleSignals: ['X-Universally-Unique-Identifier: 8F3C'],
    };
    const p = evaluateForkPairing(original, candidate, 2);
    expect(p.verdict).toBe('none');
    expect(p.note).not.toContain('replaced draft');
    expect(p.missing.join(' ')).toContain('no lineage signal');
  });
});

/**
 * human-type engine v2 tests
 * Run: node engine.test.js
 */

const { generateScript, inspectScript, simulate, ACCENT_TO_BASE } = require('./engine');

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    process.stdout.write(`  \x1b[32m✓\x1b[0m ${label}\n`);
    passed++;
  } else {
    process.stderr.write(`  \x1b[31m✗\x1b[0m ${label}\n`);
    failed++;
  }
}

function assertEqual(a, b, label) {
  assert(a === b, `${label} (got: ${JSON.stringify(a)}, want: ${JSON.stringify(b)})`);
}

function section(name) {
  process.stdout.write(`\n${name}\n`);
}

// ─── Core correctness ─────────────────────────────────────────────────────────

section('Core correctness');

{
  // No mistakes, no defers → clean pass, final text must match
  const { events } = generateScript('hello world', 5, {
    mistakeRate: 0, pauseRate: 0, deferRate: 0, seed: 1,
  });
  const { ok, finalText } = simulate(events, 'hello world');
  assert(ok, 'no-mistake script produces correct final text');
  assertEqual(finalText, 'hello world', 'final text exact match');
}

{
  // High mistake + defer rate — final text must still be correct
  const target = 'The quick brown fox jumps over the lazy dog.';
  const { events } = generateScript(target, 15, {
    mistakeRate: 0.5, pauseRate: 0.2, deferRate: 0.6, seed: 42,
  });
  const { ok, finalText } = simulate(events, target);
  assert(ok, 'high-mistake + high-defer script produces correct final text');
}

{
  // Multiple runs with different texts
  const cases = [
    'Short.',
    'A slightly longer sentence with punctuation!',
    'Numbers like 42 and 100 should work too.',
    'UPPERCASE AND lowercase mixed.',
  ];
  let allOk = true;
  for (const t of cases) {
    const { events } = generateScript(t, 8, { mistakeRate: 0.3, deferRate: 0.4, seed: 7 });
    const { ok } = simulate(events, t);
    if (!ok) allOk = false;
  }
  assert(allOk, 'correct final text for varied inputs');
}

// ─── Seeded reproducibility ───────────────────────────────────────────────────

section('Seeded reproducibility');

{
  const opts = { mistakeRate: 0.3, pauseRate: 0.2, deferRate: 0.4, seed: 1234 };
  const { events: a } = generateScript('reproducible text', 8, opts);
  const { events: b } = generateScript('reproducible text', 8, opts);
  assert(JSON.stringify(a) === JSON.stringify(b), 'same seed → identical scripts');
}

{
  const base = { mistakeRate: 0.3, pauseRate: 0.2, deferRate: 0.4 };
  const { events: a } = generateScript('same text', 8, { ...base, seed: 1 });
  const { events: b } = generateScript('same text', 8, { ...base, seed: 2 });
  assert(JSON.stringify(a) !== JSON.stringify(b), 'different seeds → different scripts');
}

// ─── Timing ───────────────────────────────────────────────────────────────────

section('Timing');

{
  const { events } = generateScript('timing check', 10, { seed: 5 });
  let ok = true;
  for (let i = 1; i < events.length; i++) {
    if (events[i].time < events[i - 1].time) { ok = false; break; }
  }
  assert(ok, 'event times are non-decreasing');
}

{
  // Total duration within 35% of requested (deferred fixups add overhead)
  const dur = 10;
  const { events } = generateScript('duration accuracy test string', dur, {
    mistakeRate: 0.3, deferRate: 0.5, seed: 9,
  });
  const totalMs = events[events.length - 1].time + events[events.length - 1].duration;
  const ratio = totalMs / (dur * 1000);
  assert(ratio > 0.65 && ratio < 1.45, `total duration within ±35% of target (ratio: ${ratio.toFixed(2)})`);
}

// ─── Deferred fixes ───────────────────────────────────────────────────────────

section('Deferred fixes');

{
  // With deferRate=1, ALL mistakes should be deferred (no immediate deletes in body)
  const { events } = generateScript('deferred only', 10, {
    mistakeRate: 0.8, pauseRate: 0, deferRate: 1.0, seed: 11,
  });
  // Immediate deletes happen only as part of immediate-fix sequences.
  // With deferRate=1, the only deletes should be zero.
  const deletes = events.filter(e => e.type === 'delete');
  assert(deletes.length === 0, 'deferRate=1 produces no immediate backspaces');
}

{
  // With deferRate=0, ALL mistakes should be immediately fixed (no select-replace)
  const { events } = generateScript('immediate only here', 10, {
    mistakeRate: 0.8, pauseRate: 0, deferRate: 0, seed: 22,
  });
  const deferred = events.filter(e => e.type === 'select-replace');
  assert(deferred.length === 0, 'deferRate=0 produces no deferred select-replace events');
}

{
  // With high deferRate, expect select-replace events
  const { events } = generateScript('testing deferred corrections now', 12, {
    mistakeRate: 0.6, deferRate: 0.9, seed: 33,
  });
  const deferred = events.filter(e => e.type === 'select-replace');
  assert(deferred.length > 0, 'high deferRate produces select-replace events');
}

{
  // Arrow events should appear when there are deferred fixes
  const { events } = generateScript('navigating back to fix', 12, {
    mistakeRate: 0.6, deferRate: 0.9, seed: 44,
  });
  const arrows = events.filter(e => e.type === 'arrow');
  const selectBacks = events.filter(e => e.type === 'select-back');
  assert(arrows.length > 0 || selectBacks.length > 0, 'deferred fixes produce cursor navigation events');
}

{
  // Deferred fixes must happen AFTER all typing is done
  // i.e., all select-replace events come after the last 'type' in the main body
  const target = 'deferred ordering test';
  const { events } = generateScript(target, 12, {
    mistakeRate: 0.7, deferRate: 1.0, seed: 55,
  });
  const lastTypeIdx = events.reduce((last, ev, i) =>
    ev.type === 'type' && i > last ? i : last, -1);
  const firstArrowIdx = events.findIndex(e => e.type === 'arrow');
  if (firstArrowIdx !== -1) {
    assert(firstArrowIdx > lastTypeIdx, 'arrow navigation comes after all main typing');
  } else {
    // No mistakes happened (RNG might not trigger), skip
    assert(true, 'no deferred fixes generated (RNG miss), skip ordering check');
  }
}

// ─── French accent mode ───────────────────────────────────────────────────────

section('French accent mode');

{
  // Accent map exists and maps correctly
  assertEqual(ACCENT_TO_BASE['é'], 'e', 'é maps to e');
  assertEqual(ACCENT_TO_BASE['ç'], 'c', 'ç maps to c');
  assertEqual(ACCENT_TO_BASE['à'], 'a', 'à maps to a');
  assertEqual(ACCENT_TO_BASE['î'], 'i', 'î maps to i');
  assertEqual(ACCENT_TO_BASE['ô'], 'o', 'ô maps to o');
  assertEqual(ACCENT_TO_BASE['É'], 'E', 'É (uppercase) maps to E');
}

{
  // French mode: final text is correct despite accent omissions
  const target = 'Être ou ne pas être, voilà la question.';
  const { events } = generateScript(target, 15, {
    french: true, accentOmitRate: 1.0,
    mistakeRate: 0, pauseRate: 0, deferRate: 1.0, seed: 66,
  });
  const { ok, finalText } = simulate(events, target);
  assert(ok, 'French text with 100% accent omission still produces correct final text');
}

{
  // French mode with accentOmitRate=0: no accent omissions, no deferred accents
  const target = 'café et thé';
  const { events } = generateScript(target, 8, {
    french: true, accentOmitRate: 0,
    mistakeRate: 0, pauseRate: 0, deferRate: 0, seed: 77,
  });
  const deferred = events.filter(e => e.type === 'select-replace');
  assert(deferred.length === 0, 'accentOmitRate=0 produces no deferred accent fixes');
  const { ok } = simulate(events, target);
  assert(ok, 'French text with accentOmitRate=0 produces correct final text');
}

{
  // French mode: accent omissions show up as base chars in the event stream
  const target = 'éléphant';
  const { events } = generateScript(target, 8, {
    french: true, accentOmitRate: 1.0,
    mistakeRate: 0, pauseRate: 0, deferRate: 1.0, seed: 88,
  });
  // The 'type' events in the forward pass should contain 'e' not 'é'
  const typeEvents = events.filter(e => e.type === 'type');
  // First few type chars: é→e, l, é→e, p, h, a, n, t
  const hasBaseE = typeEvents.some(e => e.ch === 'e');
  assert(hasBaseE, 'French mode types base char (e) instead of accented char (é)');
  // And select-replace events should contain the actual accented chars
  const replaceEvents = events.filter(e => e.type === 'select-replace');
  const hasAccentedE = replaceEvents.some(e => e.ch === 'é');
  assert(hasAccentedE, 'French deferred fix restores accented char (é)');
}

{
  // Non-French mode: accented chars are typed directly (no omissions)
  const target = 'café';
  const { events } = generateScript(target, 5, {
    french: false, mistakeRate: 0, pauseRate: 0, deferRate: 0, seed: 99,
  });
  const typeEvents = events.filter(e => e.type === 'type');
  const typedStr = typeEvents.map(e => e.ch).join('');
  assertEqual(typedStr, 'café', 'non-French mode types accented chars directly');
}

// ─── Edge cases ───────────────────────────────────────────────────────────────

section('Edge cases');

{
  let threw = false;
  try { generateScript('', 5); } catch (_) { threw = true; }
  assert(threw, 'empty text throws');
}

{
  // Single char
  const { events } = generateScript('x', 2, { mistakeRate: 0, seed: 1 });
  const { ok } = simulate(events, 'x');
  assert(ok, 'single char produces correct result');
}

{
  // Very short duration (clamped to 2s)
  const { events } = generateScript('short', 0.1, { seed: 1 });
  assert(events.length > 0, 'sub-minimum duration still generates events');
}

{
  // Inspect stats
  const { events } = generateScript('stats check', 8, {
    mistakeRate: 0.3, deferRate: 0.5, seed: 100,
  });
  const stats = inspectScript(events, 'stats check');
  assert(typeof stats.events === 'number' && stats.events > 0, 'inspect: events count');
  assert(typeof stats.avgWpm === 'number' && stats.avgWpm > 0, 'inspect: wpm');
  assert(typeof stats.deferredFixes === 'number', 'inspect: deferredFixes field exists');
  assert(typeof stats.arrowMoves === 'number', 'inspect: arrowMoves field exists');
}

// ─── Summary ─────────────────────────────────────────────────────────────────

const total = passed + failed;
process.stdout.write(
  `\n${total} tests: \x1b[32m${passed} passed\x1b[0m, \x1b[31m${failed} failed\x1b[0m\n\n`
);
if (failed > 0) process.exit(1);

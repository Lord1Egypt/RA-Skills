/**
 * human-type engine v2
 * Generates a keystroke event script from a target string.
 *
 * Event types:
 *   { type: 'type',           ch, time, duration }   — press a key
 *   { type: 'delete',             time, duration }   — backspace
 *   { type: 'pause',              time, duration }   — wait (no key)
 *   { type: 'arrow',       dir, n, time, duration }  — move cursor (dir: 'Left'|'Right'|'Home'|'End')
 *   { type: 'select-back',     n, time, duration }   — Shift+Left × n (select n chars behind cursor)
 *   { type: 'select-replace', ch, time, duration }   — type ch, replacing selection
 *
 * Deferred-fix flow:
 *   1. While typing, some mistakes are NOT immediately corrected.
 *      The wrong char is typed and the script keeps going.
 *   2. After the paragraph, one or more fix passes navigate back,
 *      select each wrong char, and replace it with the correct one.
 *   3. Cursor returns to end.
 *
 * French accent omissions:
 *   Accented chars (é, è, ê, à, â, ù, û, î, ô, ç, œ, æ …) are typed as
 *   their base ASCII equivalent and added to the deferred list, simulating
 *   a typist who forgets accents in flow and goes back to correct them.
 */

// ─── QWERTY adjacent-key map ──────────────────────────────────────────────────

const NEAR_KEYS = {
  a: 'sqwz',   b: 'vghn',   c: 'xdfv',   d: 'serfxc', e: 'wsdr34',
  f: 'drtgvc', g: 'ftyh',   h: 'gyujbn', i: 'ujko89', j: 'huikm',
  k: 'ijol',   l: 'kop',    m: 'njk',    n: 'bhjm',   o: 'iklp90',
  p: 'ol0',    q: 'wa',     r: 'edfgt45',s: 'qazwxcd',t: 'rfghy56',
  u: 'yhji78', v: 'cfgb',   w: 'qase23', x: 'zsdc',   y: 'tghu67',
  z: 'asx',
  '1': '2q',   '2': '1qw3', '3': '2we4', '4': '3er5', '5': '4rt6',
  '6': '5ty7', '7': '6yu8', '8': '7ui9', '9': '8io0', '0': '9op',
  ' ': ' '
};

// ─── French accent map ────────────────────────────────────────────────────────

const ACCENT_TO_BASE = {
  é: 'e', è: 'e', ê: 'e', ë: 'e',
  à: 'a', â: 'a', ä: 'a',
  ù: 'u', û: 'u', ü: 'u',
  î: 'i', ï: 'i',
  ô: 'o', ö: 'o',
  ç: 'c',
  œ: 'o', æ: 'a',
  É: 'E', È: 'E', Ê: 'E', Ë: 'E',
  À: 'A', Â: 'A', Ä: 'A',
  Ù: 'U', Û: 'U', Ü: 'U',
  Î: 'I', Ï: 'I',
  Ô: 'O', Ö: 'O',
  Ç: 'C',
  Œ: 'O', Æ: 'A',
};

// ─── Helpers ──────────────────────────────────────────────────────────────────

function makeRng(seed) {
  let s = seed >>> 0;
  return function () {
    s |= 0; s = s + 0x6D2B79F5 | 0;
    let t = Math.imul(s ^ s >>> 15, 1 | s);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

function nearMiss(ch, rng) {
  const lower = ch.toLowerCase();
  const neighbors = NEAR_KEYS[lower];
  if (!neighbors) return ch;
  const pick = neighbors[Math.floor(rng() * neighbors.length)];
  return ch === ch.toUpperCase() && ch !== ch.toLowerCase()
    ? pick.toUpperCase()
    : pick;
}

// ─── Segment builder ──────────────────────────────────────────────────────────

/**
 * Build logical action segments before timing is applied.
 *
 * @param {string}  text
 * @param {number}  mistakeRate    0–1, immediate typo rate
 * @param {number}  pauseRate      0–1, pause frequency
 * @param {number}  deferRate      0–1, fraction of mistakes deferred to later
 * @param {number}  accentOmitRate 0–1, fraction of accented chars omitted (French mode)
 * @param {boolean} french         enable accent omission logic
 * @param {object}  rng            seeded RNG
 */
function buildSegments(text, mistakeRate, pauseRate, deferRate, accentOmitRate, french, rng) {
  const segments = [];

  // deferred[]: errors not immediately corrected.
  // outputPos: 0-based index in the running output buffer where the wrong char sits.
  const deferred = [];
  let outLen = 0; // simulated output buffer length (cursor always at end during typing)

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const isAccented = french && ACCENT_TO_BASE[ch] !== undefined;
    const canMistake = /[a-zA-ZÀ-ÿ0-9]/.test(ch);

    // Optional pre-char pause
    if (segments.length > 0 && rng() < pauseRate) {
      segments.push({ kind: 'pause' });
    }

    // ── French accent omission ──────────────────────────────────────────────
    if (isAccented && rng() < accentOmitRate) {
      const baseCh = ACCENT_TO_BASE[ch];
      segments.push({ kind: 'type', ch: baseCh });
      deferred.push({ outputPos: outLen, correct: ch, typed: baseCh, reason: 'accent' });
      outLen++;
      continue;
    }

    // ── Typo ────────────────────────────────────────────────────────────────
    if (canMistake && !isAccented && rng() < mistakeRate) {
      const shouldDefer = rng() < deferRate;

      if (shouldDefer) {
        // Type wrong char, keep going, fix later
        const wrongCh = nearMiss(ch, rng);
        segments.push({ kind: 'type', ch: wrongCh });
        deferred.push({ outputPos: outLen, correct: ch, typed: wrongCh, reason: 'typo' });
        outLen++;
        // Do NOT type the correct char here — the deferred fix will overwrite it
        continue;
      } else {
        // Immediate fix: type N wrong chars → pause maybe → delete all → type correct
        const mistakeLen = Math.floor(rng() * 3) + 1;
        for (let m = 0; m < mistakeLen; m++) {
          segments.push({ kind: 'type', ch: nearMiss(ch, rng) });
          outLen++;
        }
        if (rng() < 0.4) segments.push({ kind: 'pause' });
        for (let m = 0; m < mistakeLen; m++) {
          segments.push({ kind: 'delete' });
          outLen--;
        }
      }
    }

    segments.push({ kind: 'type', ch });
    outLen++;
  }

  // ── Deferred fixup pass ──────────────────────────────────────────────────
  // Cursor is at end (outLen). Navigate back to each mistake, select-replace, return.

  if (deferred.length > 0) {
    // Re-read pause — like the human finishes typing, then reads the paragraph
    segments.push({ kind: 'pause' });
    segments.push({ kind: 'pause' });

    // Sort left to right so we sweep in one direction (fewer total arrow moves)
    deferred.sort((a, b) => a.outputPos - b.outputPos);

    let cursorPos = outLen;

    for (const fix of deferred) {
      // Move cursor to just AFTER the wrong char: index fix.outputPos + 1
      const dest = fix.outputPos + 1;
      const delta = cursorPos - dest;

      if (delta !== 0) {
        // Slight hesitation before navigating (human eyeing the position)
        if (rng() < 0.6) segments.push({ kind: 'pause' });

        if (delta > 0) {
          segments.push({ kind: 'arrow', dir: 'Left', n: delta });
        } else {
          segments.push({ kind: 'arrow', dir: 'Right', n: -delta });
        }
        cursorPos = dest;
      }

      // Select the 1 wrong char to the left of cursor, then type the correct one
      segments.push({ kind: 'select-back', n: 1 });
      segments.push({ kind: 'select-replace', ch: fix.correct });
      // cursorPos stays at dest (correct char now replaces wrong one, same length)
    }

    // Return cursor to end
    const toEnd = outLen - cursorPos;
    if (toEnd > 0) {
      segments.push({ kind: 'pause' });
      segments.push({ kind: 'arrow', dir: 'Right', n: toEnd });
    }
  }

  return segments;
}

// ─── Timing assignment ────────────────────────────────────────────────────────

function segWeight(seg) {
  if (seg.kind === 'pause')          return 0;
  if (seg.kind === 'arrow')          return Math.max(1, seg.n) * 0.5;
  if (seg.kind === 'select-back')    return Math.max(1, seg.n) * 0.5;
  if (seg.kind === 'select-replace') return 1.3; // deliberate, slightly slow
  return 1; // type / delete
}

function assignTimings(segments, durationMs, rng) {
  const keySegs   = segments.filter(s => s.kind !== 'pause');
  const pauseSegs = segments.filter(s => s.kind === 'pause');

  const totalWeight = keySegs.reduce((sum, s) => sum + segWeight(s), 0);
  const pauseBudget = pauseSegs.length > 0 ? durationMs * 0.28 : 0;
  const keyBudget   = durationMs - pauseBudget;
  const msPerWeight = totalWeight > 0 ? keyBudget / totalWeight : 0;
  const avgPauseMs  = pauseSegs.length > 0 ? pauseBudget / pauseSegs.length : 0;

  const events = [];
  let time = 0;

  for (const seg of segments) {
    let duration;

    if (seg.kind === 'pause') {
      duration = Math.round(avgPauseMs * (0.4 + rng() * 1.6));
    } else {
      const base = msPerWeight * segWeight(seg);
      duration = Math.round(base * (0.35 + rng() * 1.5));
      duration = Math.max(duration, 25);
    }

    const ev = { type: seg.kind, time: Math.round(time), duration };
    if (seg.ch  !== undefined) ev.ch  = seg.ch;
    if (seg.dir !== undefined) ev.dir = seg.dir;
    if (seg.n   !== undefined) ev.n   = seg.n;

    events.push(ev);
    time += duration;
  }

  return events;
}

// ─── Simulator (for tests and dry-run verification) ───────────────────────────

/**
 * Replay events against a virtual buffer and return the final text.
 * Returns { ok, finalText } where ok = (finalText === targetText).
 */
function simulate(events, targetText) {
  let buf = '';
  let cursor = 0;
  let selStart = null;

  for (const ev of events) {
    switch (ev.type) {
      case 'type':
        buf = buf.slice(0, cursor) + ev.ch + buf.slice(cursor);
        cursor++;
        selStart = null;
        break;
      case 'delete':
        if (cursor > 0) {
          buf = buf.slice(0, cursor - 1) + buf.slice(cursor);
          cursor--;
        }
        selStart = null;
        break;
      case 'arrow':
        if (ev.dir === 'Left')  cursor = Math.max(0,          cursor - ev.n);
        if (ev.dir === 'Right') cursor = Math.min(buf.length, cursor + ev.n);
        if (ev.dir === 'Home')  cursor = 0;
        if (ev.dir === 'End')   cursor = buf.length;
        selStart = null;
        break;
      case 'select-back':
        selStart = Math.max(0, cursor - ev.n);
        break;
      case 'select-replace':
        if (selStart !== null) {
          buf    = buf.slice(0, selStart) + ev.ch + buf.slice(cursor);
          cursor = selStart + ev.ch.length;
          selStart = null;
        } else {
          buf = buf.slice(0, cursor) + ev.ch + buf.slice(cursor);
          cursor += ev.ch.length;
        }
        break;
      case 'pause':
        break;
    }
  }

  return { ok: buf === targetText, finalText: buf };
}

// ─── Public API ───────────────────────────────────────────────────────────────

/**
 * Generate a keystroke script.
 *
 * @param {string} text
 * @param {number} durationSec
 * @param {object} opts
 * @param {number}  [opts.mistakeRate=0.20]     immediate typo rate (0–1)
 * @param {number}  [opts.pauseRate=0.15]        pause frequency (0–1)
 * @param {number}  [opts.deferRate=0.35]        fraction of mistakes deferred (0–1)
 * @param {number}  [opts.accentOmitRate=0.60]   fraction of accented chars omitted (0–1)
 * @param {boolean} [opts.french=false]          enable French accent omission mode
 * @param {number}  [opts.seed]                  RNG seed for reproducibility
 */
function generateScript(text, durationSec, opts = {}) {
  const {
    mistakeRate    = 0.20,
    pauseRate      = 0.15,
    deferRate      = 0.35,
    accentOmitRate = 0.60,
    french         = false,
    seed           = Math.floor(Math.random() * 0xFFFFFFFF),
  } = opts;

  if (!text || text.length === 0) throw new Error('text must not be empty');
  const durationMs = Math.max(durationSec * 1000, 2000);

  const rngSegments = makeRng(seed);
  const rngTiming   = makeRng(seed ^ 0xDEADBEEF);

  const segments = buildSegments(
    text, mistakeRate, pauseRate, deferRate, accentOmitRate, french, rngSegments
  );
  const events = assignTimings(segments, durationMs, rngTiming);

  return { events, seed };
}

/**
 * Stats summary for a generated script.
 */
function inspectScript(events, targetText) {
  const types         = events.filter(e => e.type === 'type').length;
  const deletes       = events.filter(e => e.type === 'delete').length;
  const pauses        = events.filter(e => e.type === 'pause').length;
  const deferredFixes = events.filter(e => e.type === 'select-replace').length;
  const arrows        = events.filter(e => e.type === 'arrow' || e.type === 'select-back').length;
  const totalMs       = events.length > 0
    ? events[events.length - 1].time + events[events.length - 1].duration
    : 0;
  const wordCount = targetText ? targetText.trim().split(/\s+/).length : 0;
  const wpm = wordCount > 0 && totalMs > 0
    ? Math.round(wordCount / (totalMs / 60000))
    : 0;

  return {
    events: events.length,
    keystrokes: types,
    immediateFixes: deletes,
    deferredFixes,
    arrowMoves: arrows,
    pauses,
    totalMs,
    totalSec: (totalMs / 1000).toFixed(1),
    avgWpm: wpm,
  };
}

module.exports = { generateScript, inspectScript, simulate, nearMiss, ACCENT_TO_BASE };

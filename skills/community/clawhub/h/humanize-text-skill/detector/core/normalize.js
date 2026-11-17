/**
 * core/normalize — bypass-trick normalization (language-agnostic).
 *
 * Migrated verbatim from avoid-ai-writing's normalizeText. Strips invisible /
 * lookalike chars that humanizer tools inject to defeat exact-string detectors,
 * BEFORE pattern matching. Tracks what was stripped so the trinary classifier
 * can use "normalization triggered" as a corroborating AI signal.
 *
 * Unicode ranges sourced from It-s-AI/llm-detection/detection/attacks/.
 */
'use strict';

const CYRILLIC_LOOKALIKES = {
  'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'х': 'x',
  'у': 'y', 'к': 'k', 'м': 'm', 'н': 'h', 'в': 'b', 'т': 't',
  'А': 'A', 'Е': 'E', 'О': 'O', 'Р': 'P', 'С': 'C', 'Х': 'X',
  'У': 'Y', 'К': 'K', 'М': 'M', 'Н': 'H', 'В': 'B', 'Т': 'T',
};
const GREEK_LOOKALIKES = { 'ο': 'o', 'Ο': 'O', 'α': 'a', 'Α': 'A', 'ρ': 'p', 'Ρ': 'P' };

const ROLEPLAY_VERBS = /^(?:nods|sighs|laughs|smiles|frowns|shrugs|grins|winks|chuckles|gasps|pauses|thinks|wonders|whispers|shouts|gestures|raises|leans|turns|looks|glances|smirks|blinks|nodding|sighing|laughing|smiling|thinking|gesturing)\b/i;

function normalizeText(text) {
  const flags = { zeroWidth: 0, homoglyph: 0, roleplay: 0 };
  let out = text;

  // 1. Strip zero-width chars (ZWSP U+200B, ZWNJ U+200C, ZWJ U+200D,
  //    BOM U+FEFF, word joiner U+2060).
  out = out.replace(/[​-‍﻿⁠]/g, () => { flags.zeroWidth++; return ''; });

  // 2. Swap Cyrillic / Greek Latin-lookalike chars back to Latin.
  out = out.replace(/[Ѐ-ӿͰ-Ͽ]/g, (m) => {
    const swap = CYRILLIC_LOOKALIKES[m] ?? GREEK_LOOKALIKES[m];
    if (swap) { flags.homoglyph++; return swap; }
    return m;
  });

  // 3. Strip *roleplay-action* markers — paired *...* containing an action
  //    verb anchored to the start of the inner phrase. Markdown **bold** is
  //    rejected by the lookbehind/lookahead; legitimate *italic* preserved.
  out = out.replace(/(?<!\*)\*([^*\n]{1,80}?)\*(?!\*)/gu, (m, inner) => {
    if (ROLEPLAY_VERBS.test(inner)) { flags.roleplay++; return ''; }
    return m;
  });

  return { text: out, flags };
}

module.exports = { normalizeText };

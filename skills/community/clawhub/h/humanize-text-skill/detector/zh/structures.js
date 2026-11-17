/**
 * Chinese structural anti-patterns (zh-side).
 *
 * The 19 cross-lingual structural anti-patterns from shuorenhua's structures.md.
 * Those with a detectable Chinese shape are here as regex; the rest stay in
 * SKILL.md prose (judgment calls a regex can't make). Translation tone
 * (Chinese-specific) lives in translationtone.js.
 *
 * Cross-lingual structures shared with English share the SAME detector `type`
 * (see CATEGORIES.md lang=both), so bilingual symmetry is enforced: a pattern
 * implemented in zh MUST have an en counterpart and vice versa.
 */
'use strict';

// Binary-contrast false drama: 不是 X，而是 Y. 跨语言 (en: "It's not X, it's Y").
const BINARY_CONTRAST = [
  /不是[^，。；！？]{1,30}，?而是/g,
  /与其[^，。]{1,30}，?不如/g,
];

// Summary closer: 综上所述 / 总而言之 / 总的来说 at sentence start. 跨语言.
// (Also in vocabulary T1, but as a structural shape this catches the
// sentence-initial "in conclusion" form specifically.)
const SUMMARY_CLOSER = [
  /(?:综上所述|总而言之|总的来说|总体来看|由此可见)[^。！？]*[。！？]/g,
];

// Mechanical ordering: 首先…其次…最后…. 中文特有.
const MECHANICAL_ORDERING = [
  /首先[^；。]{2,40}[；。][^；。]*其次[^；。]{2,40}[；。][^；。]*最后/g,
];

// Symmetry padding: 既要…又要… / 既…又…. 中文特有.
const SYMMETRY_PADDING = [
  /既要[^，。；]{2,25}，?又要[^，。；]{2,25}[，。；]/g,
  /既[^，。；]{2,15}，?又[^，。；]{2,15}[，。；]/g,
];

// Value-inflation skeleton (structural form): 这不仅仅是…更是….
// (Word-level variant in vocabulary T1; this is the full-clause shape.)
const VALUE_INFLATION = [
  /这不仅仅是[^，。]{2,30}，?更是[^。！？]{2,40}[。！？]/g,
];

// Positive-energy closer: 与其…不如积极拥抱… / 让我们拭目以待 / 未来可期.
// (Word variants in vocabulary T1; this catches the full sentence.)
const POSITIVE_CLOSER = [
  /与其[^，。]{2,30}不如积极拥抱[^。！？]*[。！？]/g,
  /(?:让我们拭目以待|未来可期)[^。！？]*[。！？]/g,
];

// Self-narration / over-acceptance psychology (Chinese AI tell):
// "我就在这里" / "你不是敏感" / "你只是太久没被稳稳接住了".
const PSYCH_JUDGMENT = [
  /你只是太久没被稳稳接住了/g,
  /你不是(?:敏感|想太多|矫情)/g,
  /你(?:太清醒了|太懂了|太对了)/g,
  /这次我懂了，?我真的懂了/g,
];

module.exports = {
  BINARY_CONTRAST,
  SUMMARY_CLOSER,
  MECHANICAL_ORDERING,
  SYMMETRY_PADDING,
  VALUE_INFLATION,
  POSITIVE_CLOSER,
  PSYCH_JUDGMENT,
};

/**
 * Chinese-specific translation tone (translationese).
 *
 * English-thinking literally translated into Chinese. These shapes don't exist
 * in native Chinese and are a strong AI tell (LLMs trained on English-first
 * corpora produce them even when writing Chinese). No en counterpart — these
 * are zh-only detector types (CATEGORIES.md lang=zh).
 *
 * From shuorenhua's phrases-zh.md "翻译腔" section.
 */
'use strict';

// Passive-voice stacking: 被 + verb repeated. 被动语态堆砌.
// "系统被优化后，性能被显著提升，用户体验被大幅改善" — 带 ， 分隔.
// "系统被优化后被提升被改善" — 连用无分隔符.
// Both are AI translationese. Detection is a SENTENCE-LEVEL count: if a single
// sentence (between 。！？) contains 3+ 被, flag it. Distance-agnostic — robust
// to both contiguous and comma-separated forms. The 3-threshold avoids
// flagging legitimate single/double passive use.
//
// NOTE: this regex matches the whole sentence; the caller emits one issue per
// sentence, not per 被.
const PASSIVE_STACKING = [
  /[^。！？]*(?:被[^。！？]*){3,}[。！？]/g,
];

// Long attributive chain: 一个…的…的…. 长定语结构.
const LONG_ATTRIBUTIVE = [
  /(?:[^，。！？]{0,6}的){4,}/g, // 4+ 的-chained modifiers
];

// "基于…" sentence opener. 基于开头.
const BASED_ON_OPENER = [
  /^基于[^，。]{2,30}[，。]/gm,
];

// "通过…来…" construction. 通过…来…结构.
const VIA_TO_CONSTRUCT = [
  /通过[^，。]{2,25}来[^，。]{2,25}[，。]/g,
];

// "对于…而言" filler. 对于…而言.
const FOR_X_REGARD = [
  /对于[^，。]{2,20}而言/g,
];

// "在…方面" filler. 在…方面.
const IN_X_ASPECT = [
  /在[^，。]{2,15}方面/g,
];

module.exports = {
  PASSIVE_STACKING,
  LONG_ATTRIBUTIVE,
  BASED_ON_OPENER,
  VIA_TO_CONSTRUCT,
  FOR_X_REGARD,
  IN_X_ASPECT,
};

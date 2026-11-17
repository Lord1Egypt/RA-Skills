/**
 * core/voice — the ADDITION layer (humanize-text-skill's soul).
 *
 * Both parent projects explicitly disclaim fitting a specific person's writing
 * voice: avoid-ai-writing stops at "sound human"; shuorenhua says it doesn't
 * fit a named individual. humanize-text-skill goes one step further — "活人感" (alive)
 * means pulling the rewrite toward a *target* human voice, not just away from
 * AI tone. This module is that step.
 *
 * It works in three moves:
 *   1. EXTRACT a fingerprint from the text (sentence-length mean/std, connector
 *      set, punctuation rate, contraction/first-person tendency).
 *   2. COMPARE against a target profile (from voice.toml, or calibrated from a
 *      user sample). Produce a `drift` score 0-100 (0 = on-target, 100 = far).
 *   3. SUGGEST concrete pulls: "split sentence 3 (28 chars) into 12+16",
 *      "swap 'furthermore' for 'but'", "raise contraction rate".
 *
 * Independence contract: `voice.drift` is its OWN dimension. It never touches
 * `score` (AI density) or `fidelity` (protected spans). The three are reported
 * separately and the consumer decides how to combine them.
 */
'use strict';

const policy = require('./policy');

// Extract a stylometric fingerprint from text. Language-aware: zh counts
// chars per sentence, en counts words.
function extractFingerprint(text, lang) {
  const isZh = lang === 'zh';
  const sentenceSep = isZh ? /[。！？]/ : /[.!?]+/;
  const raw = text.split(sentenceSep).map((s) => s.trim()).filter((s) => s.length > 1);
  if (raw.length === 0) {
    return { sentenceLenMean: 0, sentenceLenStd: 0, sentenceCount: 0, punctRate: 0, connectorHits: [], contractionRate: 0, firstPerson: false };
  }
  const lengths = raw.map((s) => (isZh ? s.replace(/\s/g, '').length : (s.match(/\S+/g) || []).length));
  const mean = lengths.reduce((a, b) => a + b, 0) / lengths.length;
  const variance = lengths.reduce((s, l) => s + (l - mean) ** 2, 0) / lengths.length;
  const std = Math.sqrt(variance);
  const cv = mean > 0 ? std / mean : 0;

  // Punctuation density: commas/semicolons/colons/dashes per char-or-word.
  const unitCount = isZh ? text.replace(/\s/g, '').length : (text.match(/\S+/g) || []).length;
  const puncts = (text.match(isZh ? /[，；：、——]/g : /[,;:—]/g) || []).length;
  const punctRate = unitCount > 0 ? puncts / unitCount : 0;

  // Connector set: which preferred connectives appear (en contraction-aware).
  const enConnectors = ['and', 'but', 'so', 'however', 'therefore', 'thus', 'since', 'or'];
  const zhConnectors = ['其实', '不过', '反正', '同时', '因此', '所以', '由于', '但是', '所以'];
  const connectorSet = isZh ? zhConnectors : enConnectors;
  const lower = isZh ? text : text.toLowerCase();
  const connectorHits = connectorSet.filter((c) => lower.includes(c));

  // Contraction rate (en only) + first-person presence.
  let contractionRate = 0;
  let firstPerson = false;
  if (!isZh) {
    const contractions = (text.match(/\b(?:don't|can't|won't|isn't|it's|I'm|you're|we're|that's|let's)\b/gi) || []).length;
    const wordCount = (text.match(/\S+/g) || []).length;
    contractionRate = wordCount > 0 ? contractions / wordCount : 0;
    firstPerson = /\b(?:i|i'm|i've|i'll|my|me|we|our)\b/i.test(text);
  } else {
    firstPerson = /[我我]/.test(text) || text.includes('咱们') || text.includes('我们');
  }

  return { sentenceLenMean: mean, sentenceLenStd: std, sentenceLenCv: cv, sentenceCount: raw.length, punctRate, connectorHits, contractionRate, firstPerson };
}

// Calibrate a target profile from a user-supplied sample (voiceMode='custom').
function calibrateFromSample(sampleText, lang) {
  const fp = extractFingerprint(sampleText, lang);
  return {
    sentence_len_target: Math.round(fp.sentenceLenMean),
    sentence_len_cv: +(fp.sentenceLenCv.toFixed(2)),
    contraction_rate: +(fp.contractionRate.toFixed(2)),
    first_person_ok: fp.firstPerson,
    connector_set: fp.connectorHits,
    _calibrated: true,
  };
}

// Compute drift (0-100) between detected fingerprint and target profile.
// Weighted: sentence-length mean is the dominant signal (rhythm is the #1
// human-vs-AI stylometric cue per aaw's notes), then CV (rhythm spread),
// then punctuation rate, then connector overlap.
function computeDrift(detected, target, lang = 'en') {
  if (!target) return { drift: 0, deltas: {} };
  const deltas = {};
  const lowSignal = detected.sentenceCount < 2;

  // Sentence-length mean: relative difference, clamped.
  const targetLen = target.sentence_len_target || 0;
  if (targetLen > 0) {
    const diff = Math.abs(detected.sentenceLenMean - targetLen) / targetLen;
    deltas.sentenceLen = Math.min(100, diff * 100);
  } else {
    deltas.sentenceLen = 0;
  }

  // CV (rhythm spread): absolute difference scaled.
  const targetCv = target.sentence_len_cv || 0;
  deltas.rhythmCv = lowSignal || targetCv <= 0
    ? 0
    : Math.min(100, Math.abs(detected.sentenceLenCv - targetCv) * 200);

  // Punctuation rate: relative difference (en only meaningful).
  deltas.punctRate = 0; // target rarely specifies; neutral weight

  // Connector overlap: fraction of target connectors present (inverted to drift).
  const targetConn = target.connector_set || [];
  if (targetConn.length > 0) {
    const overlap = targetConn.filter((c) => detected.connectorHits.includes(c)).length;
    deltas.connectors = Math.round((1 - overlap / targetConn.length) * 100);
  } else {
    deltas.connectors = 0;
  }

  // Weighted sum. Weights reflect stylometric research: length > rhythm > connectors.
  let drift = Math.round(
    deltas.sentenceLen * 0.45 +
    deltas.rhythmCv * 0.30 +
    deltas.connectors * 0.25
  );

  // Chinese single-sentence snippets do not contain enough rhythm evidence for
  // a reliable voice-distance estimate. Keep the signal, but damp it so short
  // status updates do not look maximally off-target by construction.
  if (lang === 'zh' && lowSignal) drift = Math.round(drift * 0.65);

  return { drift: Math.min(100, drift), deltas, confidence: lowSignal ? 'low' : 'normal' };
}

// Produce concrete, actionable pull suggestions. These are what make the
// addition layer useful — not just "your drift is 47" but "split sentence 3".
function suggestPulls(detected, target, sentences, lang) {
  const suggestions = [];
  if (!target || !sentences || sentences.length === 0) return suggestions;
  const isZh = lang === 'zh';

  // 1. Sentences far above target length → split suggestion.
  const targetLen = target.sentence_len_target || 0;
  if (targetLen > 0) {
    const lenFn = isZh
      ? (s) => s.replace(/\s/g, '').length
      : (s) => (s.match(/\S+/g) || []).length;
    sentences.forEach((s, i) => {
      const len = lenFn(s);
      if (len > targetLen * 1.8) {
        suggestions.push({
          kind: 'split',
          sentence: i + 1,
          current: Math.round(len),
          target: Math.round(targetLen),
          hint: isZh
            ? `第 ${i + 1} 句约 ${Math.round(len)} 字，目标 ${Math.round(targetLen)} 字左右——考虑在第 ${Math.round(len / 2)} 字处断开`
            : `Sentence ${i + 1} is ~${Math.round(len)} words vs target ${Math.round(targetLen)} — consider splitting around word ${Math.round(len / 2)}`,
        });
      }
    });
  }

  // 2. CV too low (metronomic) → vary length.
  const targetCv = target.sentence_len_cv || 0;
  if (targetCv > 0 && detected.sentenceLenCv < targetCv * 0.6) {
    suggestions.push({
      kind: 'vary',
      hint: isZh
        ? `句长变化小（CV ${detected.sentenceLenCv.toFixed(2)}，目标 ${targetCv.toFixed(2)}）——混入 3-8 字短句制造呼吸感`
        : `Sentence lengths too uniform (CV ${detected.sentenceLenCv.toFixed(2)} vs target ${targetCv.toFixed(2)}) — mix in 3-8 word punchy sentences`,
    });
  }

  // 3. Missing target connectors.
  const targetConn = target.connector_set || [];
  const missing = targetConn.filter((c) => !detected.connectorHits.includes(c));
  if (missing.length > 0 && targetConn.length > 0) {
    suggestions.push({
      kind: 'connectors',
      hint: isZh
        ? `目标 voice 偏好连接词：${missing.join('、')}——当前未出现，可酌情替换现有过渡`
        : `Target voice prefers: ${missing.join(', ')} — try swapping in for current transitions`,
    });
  }

  return suggestions;
}

// Top-level: given text + voiceMode + optional sample, return the voice block.
// Returns null when voiceMode === 'none' (pure subtraction, no addition layer).
function analyzeVoice(text, lang, options = {}) {
  const voiceMode = options.voiceMode || 'none';
  if (voiceMode === 'none') return null;

  let target;
  if (voiceMode === 'custom') {
    if (!options.sample) return null; // custom needs a sample
    target = calibrateFromSample(options.sample, lang);
  } else {
    target = policy.VOICE[voiceMode];
    if (!target) {
      throw new Error(
        `Unknown or unavailable voice profile "${voiceMode}". ` +
        'Check that policy/voice.toml is installed and contains this profile.'
      );
    }
  }

  const detected = extractFingerprint(text, lang);
  // Select the language-appropriate connector set before drift computation.
  const isZh = lang === 'zh';
  const targetWithLang = {
    ...target,
    connector_set: isZh ? (target.connector_set_zh || []) : (target.connector_set_en || target.connector_set || []),
  };
  const { drift, deltas, confidence } = computeDrift(detected, targetWithLang, lang);
  const sentenceSep = isZh ? /[。！？]/ : /[.!?]+/;
  const sentences = text.split(sentenceSep).map((s) => s.trim()).filter((s) => s.length > 1);
  const suggestions = suggestPulls(detected, targetWithLang, sentences, lang);

  return { detected, target: targetWithLang, drift, deltas, suggestions, voiceMode, confidence };
}

module.exports = {
  extractFingerprint,
  calibrateFromSample,
  computeDrift,
  suggestPulls,
  analyzeVoice,
};

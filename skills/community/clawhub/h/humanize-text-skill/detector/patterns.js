/**
 * humanize-text-skill — detection + voice engine entry point (canonical source of truth).
 *
 * Bilingual (zh/en) successor to avoid-ai-writing's single-file engine. The
 * language-agnostic logic lives in core/; per-language data + tokenizers live
 * in zh/ and en/. Stage 1 migrates the English side verbatim — behavioral
 * parity with aaw is the regression contract (humanize-text-skill's English output must
 * match avoid-ai-writing on the same input). Chinese side lands in stage 2.
 *
 * Three-dimension contract (AGENTS.md):
 *   - score      : AI density 0-100  (computed ONLY in core/scoring.js)
 *   - fidelity   : protected-spans gate (NOT a score)         [stage 2+]
 *   - voice.drift: distance from target voice (own dimension)  [stage 4]
 * Never fold one into another.
 */
'use strict';

const enVocab = require('./en/vocabulary');
const enStruct = require('./en/structures');
const enTok = require('./en/tokenizer');
const zhVocab = require('./zh/vocabulary');
const zhStruct = require('./zh/structures');
const zhTone = require('./zh/translationtone');
const zhTok = require('./zh/tokenizer');
const { normalizeText } = require('./core/normalize');
const fingerprints = require('./core/fingerprints');
const scoring = require('./core/scoring');
const { buildSentenceRegions, classifyTrinary } = require('./core/trinary');
const policy = require('./core/policy');
const { analyzeVoice } = require('./core/voice');

const MAX_WORDS = 10000;
const VALID_CONTEXT_MODES = new Set(['general', 'technical', 'marketing', 'personal']);
const VALID_SCENE_MODES = new Set(['chat', 'status', 'docs', 'public-writing']);

// Apply the scene×tier matrix to the issue list: suppress tiers the policy
// marks 'suppress' for the given scene. Pure filter — does not change scoring
// of surviving issues, so the one-scorer contract holds.
function applyScenePolicy(issues, sceneMode) {
  if (!sceneMode) return issues;
  return issues.filter((i) => {
    if (i.type === 'tier1') return policy.shouldSurfaceTier(sceneMode, 'T1');
    if (i.type === 'tier2') return policy.shouldSurfaceTier(sceneMode, 'T2');
    if (i.type === 'tier3') return policy.shouldSurfaceTier(sceneMode, 'T3');
    return true; // non-tier issues always surface
  });
}

function buildV2Defaults(classification, confidence) {
  const probs = classification === 'HUMAN_ONLY'
    ? { human: 1, mixed: 0, ai: 0 }
    : classification === 'AI_ONLY'
      ? { human: 0, mixed: 0, ai: 1 }
      : { human: 0.333, mixed: 0.334, ai: 0.333 };
  return {
    document_classification: classification,
    class_probabilities: probs,
    confidence_category: confidence,
    highlight_sentence_for_ai: [],
  };
}

function shouldSkipZhTier2Literal(para, literal) {
  if (literal !== '有效') return false;
  return (
    /有效\s*\d+(?:\.\d+)?(?:倍|%|个|次|x)?/i.test(para) ||
    /有效(?:解决|降低|提升|缓解|减少|避免|控制|改善)/.test(para)
  );
}

// Language router: dispatch to the English or Chinese analyzer based on the
// dominant script of the text. Mixed text routes by the majority span; the
// chosen analyzer still runs its shared detectors (fingerprints, stylometry)
// over the whole text. This is the bilingual symmetry point — see
// bilingual.test.js for cross-lingual structural parity.
function analyzeText(text, options = {}) {
  if (!text || text.trim().length === 0) {
    return { ...buildV2Defaults('UNSCORED', 'low'), score: 0, label: 'Empty', issues: [], stats: {}, tooShort: true };
  }
  const isZh = zhTok.isChineseText(text);
  return isZh ? analyzeChinese(text, options) : analyzeEnglish(text, options);
}

function analyzeEnglish(text, options = {}) {
  const requestedMode = options.contextMode || 'general';
  const contextMode = VALID_CONTEXT_MODES.has(requestedMode) ? requestedMode : 'general';
  const contextModeFallback = requestedMode !== contextMode ? requestedMode : null;
  const sceneMode = VALID_SCENE_MODES.has(options.sceneMode) ? options.sceneMode : null;

  // Pre-pass: strip Markdown blockquotes before scoring.
  let quotedLines = 0;
  const rawLines = text.split(/\r?\n/);
  const isQuote = rawLines.map((l) => /^\s*>\s/.test(l));
  const stripIdx = new Set();
  for (let i = 0; i < rawLines.length; i++) {
    if (isQuote[i] && ((isQuote[i - 1] && i > 0) || isQuote[i + 1])) {
      stripIdx.add(i);
      quotedLines++;
    }
  }
  text = rawLines.filter((_, i) => !stripIdx.has(i)).join('\n');

  // Pre-pass: strip bypass-trick chars before pattern matching.
  const norm = normalizeText(text);
  text = norm.text;

  const wordCount = enTok.countWords(text);
  if (wordCount < 10) {
    return { ...buildV2Defaults('UNSCORED', 'low'), score: 0, label: 'Too short', issues: [], stats: { wordCount, contextMode, contextModeFallback }, tooShort: true };
  }
  if (wordCount > MAX_WORDS) {
    return {
      ...buildV2Defaults('UNSCORED', 'low'),
      score: 0, label: 'Text too long', issues: [],
      stats: { wordCount, contextMode, contextModeFallback }, tooLong: true,
    };
  }

  const tokens = enTok.tokenize(text);
  const paragraphs = enTok.getParagraphs(text);
  const sentences = enTok.getSentences(text);
  const issues = [];

  // ── 1. Tier 1 words ──────────────────────────────────────────
  const tier1Found = new Set();
  for (const token of tokens) {
    if (enVocab.TIER1[token] && !tier1Found.has(token)) {
      tier1Found.add(token);
      issues.push({ type: 'tier1', text: token, severity: 'high', suggestion: enVocab.TIER1[token] });
    }
  }
  for (const phrase of enVocab.TIER1_PHRASES) {
    const regex = new RegExp(phrase.pattern.source, phrase.pattern.flags);
    let match;
    while ((match = regex.exec(text)) !== null) {
      const lower = match[0].toLowerCase();
      if (tier1Found.has(lower)) continue;
      tier1Found.add(lower);
      issues.push({ type: 'tier1', text: match[0], severity: 'high', suggestion: phrase.replace });
    }
  }

  // ── 2. Tier 2 clusters ───────────────────────────────────────
  let tier2Clusters = 0;
  for (const para of paragraphs) {
    const paraTokens = enTok.tokenize(para);
    const found = [];
    for (const token of paraTokens) {
      if (enVocab.TIER2[token] && !found.includes(token)) found.push(token);
    }
    if (found.length >= 2) {
      tier2Clusters++;
      for (const word of found) {
        issues.push({ type: 'tier2', text: word, severity: 'medium', suggestion: enVocab.TIER2[word] });
      }
    }
  }

  // ── 3. Tier 3 density ────────────────────────────────────────
  const tier3Counts = {};
  for (const token of tokens) {
    const canonical = enVocab.TIER3_LOOKUP.get(token);
    if (canonical) tier3Counts[canonical] = (tier3Counts[canonical] || 0) + 1;
  }
  const densityThreshold = Math.max(3, Math.floor(wordCount * 0.03));
  let tier3Flags = 0;
  for (const [word, count] of Object.entries(tier3Counts)) {
    if (count >= densityThreshold) {
      tier3Flags++;
      issues.push({ type: 'tier3', text: `"${word}" x${count}`, severity: 'low', suggestion: `Overused (${count} times in ${wordCount} words)` });
    }
  }

  // ── 4–21. Pattern categories ─────────────────────────────────
  const mp = enTok.matchPatterns;
  issues.push(...mp(text, enStruct.TRANSITIONS, 'transition', 'medium'));
  issues.push(...mp(text, enStruct.CHATBOT_ARTIFACTS, 'chatbot', 'critical'));
  issues.push(...mp(text, enStruct.SYCOPHANTIC, 'sycophantic', 'critical'));
  issues.push(...mp(text, enStruct.FILLERS, 'filler', 'medium'));
  issues.push(...mp(text, enStruct.GENERIC_CONCLUSIONS, 'generic-conclusion', 'medium'));
  issues.push(...mp(text, enStruct.LETS_PATTERNS, 'lets-construction', 'medium'));
  issues.push(...mp(text, enStruct.REASONING_ARTIFACTS, 'reasoning-artifact', 'critical'));
  issues.push(...mp(text, enStruct.ACKNOWLEDGMENT_LOOPS, 'acknowledgment-loop', 'medium'));
  issues.push(...mp(text, enStruct.SIGNIFICANCE_INFLATION, 'significance-inflation', 'high'));
  issues.push(...mp(text, enStruct.VAGUE_ATTRIBUTIONS, 'vague-attribution', 'critical'));
  issues.push(...mp(text, enStruct.HOLLOW_INTENSIFIERS, 'hollow-intensifier', 'medium'));
  issues.push(...mp(text, enStruct.EMOTIONAL_FLATLINE, 'emotional-flatline', 'low'));
  issues.push(...mp(text, enStruct.NOVELTY_INFLATION, 'novelty-inflation', 'medium'));
  issues.push(...mp(text, enStruct.CUTOFF_DISCLAIMERS, 'cutoff-disclaimer', 'critical'));
  issues.push(...mp(text, fingerprints.AI_PLACEHOLDERS, 'ai-placeholder', 'critical'));
  issues.push(...mp(text, fingerprints.AI_CITATION_MARKUP, 'ai-citation-markup', 'critical'));
  issues.push(...mp(text, fingerprints.AI_UTM_SOURCE, 'ai-utm-source', 'critical'));
  issues.push(...mp(text, enStruct.TEMPLATE_PHRASES, 'template-phrase', 'high'));
  issues.push(...mp(text, enStruct.FALSE_CONCESSION, 'false-concession', 'medium'));
  issues.push(...mp(text, enStruct.RHETORICAL_QUESTIONS, 'rhetorical-question', 'medium'));
  issues.push(...mp(text, enStruct.HEDGE_STACK, 'hedge-stack', 'high'));
  issues.push(...mp(text, enStruct.FUTURE_NARRATIVE, 'future-narrative', 'high'));
  issues.push(...mp(text, enStruct.REAL_ACTUAL_INFLATION, 'real-actual-inflation', 'medium'));
  issues.push(...mp(text, enStruct.SOCIAL_CTA_CLOSER, 'social-cta-closer', 'high'));
  issues.push(...mp(text, enStruct.FORMULAIC_OPENERS, 'formulaic-opener', 'high'));
  issues.push(...mp(text, enStruct.PARENTHETICAL_HEDGE, 'parenthetical-hedge', 'medium'));

  // ── Cross-lingual structural symmetry (en counterparts of zh/structures.js) ──
  // Same `type` as the zh side so bilingual symmetry holds.
  issues.push(...mp(text, enStruct.BINARY_CONTRAST, 'false-concession', 'medium'));
  issues.push(...mp(text, enStruct.MECHANICAL_ORDERING, 'template-phrase', 'medium'));
  issues.push(...mp(text, enStruct.SYMMETRY_PADDING, 'template-phrase', 'medium'));
  issues.push(...mp(text, enStruct.VALUE_INFLATION, 'significance-inflation', 'high'));
  issues.push(...mp(text, enStruct.SUMMARY_CLOSER, 'generic-conclusion', 'medium'));

  if (contextMode !== 'technical') {
    const titleHits = mp(text, [enStruct.TITLE_CASE_HEADER], 'title-case-header', 'medium');
    const filtered = titleHits.filter((h) => {
      const toks = h.text.split(/\s+/);
      return toks.length >= 4 && /\b(?:And|Or|Of|The|In|For|To|A|An)\b/.test(h.text);
    });
    issues.push(...filtered);
  }

  // ── Normalization-trigger flag ───────────────────────────────────
  if (norm.flags.zeroWidth > 0 || norm.flags.homoglyph >= 2) {
    issues.push({
      type: 'normalization-flag',
      text: `${norm.flags.zeroWidth} zero-width + ${norm.flags.homoglyph} homoglyph swap${norm.flags.homoglyph === 1 ? '' : 's'}`,
      severity: 'critical',
      suggestion: 'Text contains invisible/lookalike chars typical of AI-humanizer bypass tools. Re-type from your own keyboard.',
    });
  }
  if (norm.flags.roleplay >= 2) {
    issues.push({ type: 'normalization-flag', text: `${norm.flags.roleplay} *roleplay-action* markers stripped`, severity: 'high', suggestion: 'Paired *action* markers are a chat-model artifact.' });
  }

  // ── Smart-punctuation co-occurrence signature ────────────────────
  {
    const hasCurly = /[“”‘’]/.test(text);
    const hasEmDash = /—/.test(text);
    const oxfordHit = text.match(/\b\w+,\s+\w+,\s+and\s+\w+/g);
    const hasOxford = (oxfordHit?.length || 0) >= 1;
    const doubleSpaces = (text.match(/[^.!?]  +/g) || []).length;
    const missingApos = /\b(?:dont|wont|cant|isnt|wasnt|shouldnt|wouldnt|couldnt|youre|theyre|its\s+a\s+\w+ing)\b/i.test(text);
    const clean = doubleSpaces === 0 && !missingApos;
    const signals = [hasCurly, hasEmDash, hasOxford, clean].filter(Boolean).length;
    if (signals >= 4 && wordCount >= 80) {
      issues.push({ type: 'smart-punct-signature', text: 'curly-quotes + em-dash + Oxford comma + zero typos', severity: 'high', suggestion: 'Smart-punctuation signature consistent with LLM output. Humans typing into textareas rarely produce all four.' });
    }
  }

  // ── Punctuation distribution mode ────────────────────────────────
  if (paragraphs.length >= 4) {
    const densities = paragraphs.map((p) => {
      const words = (p.match(/\S+/g) || []).length;
      if (words < 5) return null;
      const puncts = (p.match(/[,;:—()]/g) || []).length;
      return puncts / words;
    }).filter((d) => d !== null);
    if (densities.length >= 4) {
      const mean = densities.reduce((a, b) => a + b, 0) / densities.length;
      const variance = densities.reduce((s, d) => s + (d - mean) ** 2, 0) / densities.length;
      const cv = mean > 0 ? Math.sqrt(variance) / mean : 0;
      if (cv < 0.25 && mean >= 0.04) {
        issues.push({ type: 'punct-distribution', text: `Punctuation density uniform across paragraphs (CV=${cv.toFixed(2)})`, severity: 'medium', suggestion: 'AI text holds punctuation density steady; human writers swing between dense and sparse paragraphs.' });
      }
    }
  }

  // ── Function-word trigram entropy ────────────────────────────────
  if (wordCount >= 150) {
    const FUNC_WORDS = new Set(['the','a','an','and','or','but','of','to','in','on','at','by','for','with','from','as','is','was','are','were','be','been','being','have','has','had','do','does','did','will','would','should','could','may','might','must','can','this','that','these','those','it','its','they','them','their','there','here','we','our','us','i','you','your','he','she','his','her','him','not','no','so','if','then','than','when','where','which','who','what','how','why','because']);
    const seq = tokens.map((t) => FUNC_WORDS.has(t) ? t : '_').filter((_, i, arr) => arr[i] !== '_' || (i > 0 && arr[i - 1] !== '_'));
    if (seq.length >= 50) {
      const trigrams = {};
      for (let i = 0; i < seq.length - 2; i++) {
        const tg = `${seq[i]}|${seq[i + 1]}|${seq[i + 2]}`;
        trigrams[tg] = (trigrams[tg] || 0) + 1;
      }
      const total = seq.length - 2;
      let entropy = 0;
      for (const c of Object.values(trigrams)) {
        const p = c / total;
        entropy -= p * Math.log2(p);
      }
      const distinctCount = Object.keys(trigrams).length;
      const normalized = distinctCount > 1 ? entropy / Math.log2(distinctCount) : 1;
      if (normalized < 0.82 && total >= 50) {
        issues.push({ type: 'fnword-trigram-entropy', text: `Function-word trigram entropy ${normalized.toFixed(2)} (low)`, severity: 'medium', suggestion: 'Grammatical structure is unusually repetitive. AI sampling collapses onto narrower templates than human writing.' });
      }
      if (distinctCount === 1 && total >= 50) {
        issues.push({ type: 'fnword-trigram-entropy', text: 'Single function-word trigram repeated across document', severity: 'high', suggestion: 'Grammatical structure is fully degenerate — every clause uses the same function-word skeleton.' });
      }
    }
  }

  // ── Cross-paragraph burstiness ───────────────────────────────────
  if (paragraphs.length >= 4) {
    const cvs = paragraphs.map((p) => {
      const sents = enTok.getSentences(p);
      if (sents.length < 3) return null;
      const lens = sents.map(enTok.countWords);
      const m = lens.reduce((a, b) => a + b, 0) / lens.length;
      if (m === 0) return null;
      const v = lens.reduce((s, l) => s + (l - m) ** 2, 0) / lens.length;
      return Math.sqrt(v) / m;
    }).filter((c) => c !== null);
    if (cvs.length >= 4) {
      const cvMean = cvs.reduce((a, b) => a + b, 0) / cvs.length;
      const cvVar = cvs.reduce((s, c) => s + (c - cvMean) ** 2, 0) / cvs.length;
      const cvStd = Math.sqrt(cvVar);
      if (cvStd < 0.08 && cvMean < 0.45) {
        issues.push({ type: 'cross-para-burstiness', text: `Sentence-rhythm uniform across paragraphs (σCV=${cvStd.toFixed(2)})`, severity: 'medium', suggestion: 'Every paragraph has the same internal rhythm. Humans vary cadence between terse and discursive paragraphs.' });
      }
    }
  }

  // ── Tier 3 multi-word phrase density ─────────────────────────
  const claimedSpans = [];
  function spanOverlaps(start, end) {
    for (const [s, e] of claimedSpans) {
      if (start < e && end > s) return true;
    }
    return false;
  }
  let distinctPhrasesHit = 0;
  for (const phrase of enVocab.TIER3_PHRASES) {
    const regex = new RegExp(phrase.source, phrase.flags);
    const phraseSpans = [];
    let phraseMatch;
    while ((phraseMatch = regex.exec(text)) !== null) {
      const start = phraseMatch.index;
      const end = start + phraseMatch[0].length;
      if (!spanOverlaps(start, end)) phraseSpans.push([start, end, phraseMatch[0]]);
    }
    if (phraseSpans.length === 0) continue;
    for (const [s, e] of phraseSpans) claimedSpans.push([s, e]);
    distinctPhrasesHit++;
    if (phraseSpans.length >= 2) {
      issues.push({ type: 'tier3-phrase', text: `"${phraseSpans[0][2].toLowerCase()}" x${phraseSpans.length}`, severity: 'medium', suggestion: `Boilerplate phrase repeated ${phraseSpans.length}× — replace at least one with specifics` });
    }
  }
  if (distinctPhrasesHit >= 3) {
    issues.push({ type: 'tier3-phrase-cluster', text: `${distinctPhrasesHit} distinct boilerplate phrases`, severity: 'high', suggestion: 'Several stock crypto/web3 phrases stacked in one piece. Rewrite around one specific claim or observation.' });
  }

  // ── Hashtag stuffing ─────────────────────────────────────────
  const hashtagMatches = text.match(/(?:^|\W)#\w[\w-]*/g) || [];
  if (hashtagMatches.length >= 6) {
    issues.push({ type: 'hashtag-stuff', text: `${hashtagMatches.length} hashtags`, severity: 'medium', suggestion: 'Cut to 2-3 specific tags or none. Long hashtag blocks read as bot output.' });
  }

  // ── Bullet list of bare noun phrases ─────────────────────────
  const lines = text.split(/\r?\n/);
  const bulletRe = /^\s*(?:\*|-|•|\+)\s+(.+)$/;
  const verbRe = /\b(?:is|are|was|were|has|have|had|will|would|should|must|do|does|did|can|could|may|might|am|been|being)\b/i;
  const fenceRe = /^\s*(?:```|~~~)/;
  let run = [];
  let blankStreak = 0;
  let inFence = false;
  function flushRun() {
    if (run.length >= 5) {
      const bareNP = run.filter((it) => {
        const wc = (it.match(/\S+/g) || []).length;
        return wc > 0 && wc <= 6 && !verbRe.test(it);
      });
      if (bareNP.length >= 5 && bareNP.length / run.length >= 0.75) {
        issues.push({ type: 'bullet-np-list', text: `${run.length}-item bullet list of bare noun phrases`, severity: 'high', suggestion: 'Convert to a prose paragraph or merge items. Long lists of bare adj+noun pairs read as AI scaffolding.' });
      }
    }
    run = [];
    blankStreak = 0;
  }
  for (const line of lines) {
    if (fenceRe.test(line)) { flushRun(); inFence = !inFence; continue; }
    if (inFence) continue;
    const m = line.match(bulletRe);
    if (m) { run.push(m[1].trim()); blankStreak = 0; }
    else if (line.trim() === '') { blankStreak++; if (blankStreak >= 2) flushRun(); }
    else flushRun();
  }
  flushRun();

  // Confidence calibration — only flagged when it stacks (3+ instances).
  const confIssues = mp(text, enStruct.CONFIDENCE_CALIBRATION, 'confidence-calibration', 'low');
  if (confIssues.length >= 3) issues.push(...confIssues);

  // ── Em dash frequency ────────────────────────────────────────
  const emDashCount = (text.match(/—|(?<=\s)--(?=\s|$)|(?<=^|\s)--(?=\s)/gm) || []).length;
  const emDashRate = emDashCount / (wordCount / 1000);
  const hasTechnicalAnchors = /`[^`]+`|[A-Z_]{2,}=\S+|\/[A-Za-z0-9._-]+|\b\d+(?:\.\d+)?(?:ms|s|MB|GB|%|QPS)\b/.test(text);
  const emDashThreshold = hasTechnicalAnchors ? 6 : 3;
  if (emDashRate > 1 && emDashCount >= emDashThreshold) {
    issues.push({ type: 'em-dash', text: `${emDashCount} em dashes in ${wordCount} words`, severity: 'medium', suggestion: 'Replace with commas, periods, or rewrite' });
  }

  // ── Sentence length uniformity ───────────────────────────────
  if (sentences.length >= 5) {
    const lengths = sentences.map((s) => enTok.countWords(s));
    const avg = lengths.reduce((a, b) => a + b, 0) / lengths.length;
    const variance = lengths.reduce((sum, l) => sum + Math.pow(l - avg, 2), 0) / lengths.length;
    const stdDev = Math.sqrt(variance);
    const cv = avg > 0 ? stdDev / avg : 0;
    if (cv < 0.25 && avg > 10) {
      issues.push({ type: 'uniformity', text: `Sentence lengths cluster around ${Math.round(avg)} words (low variation)`, severity: 'medium', suggestion: 'Mix short punchy sentences with longer flowing ones' });
    }
  }

  // ── Type-token ratio (stylometric — vocabulary diversity) ────
  if (tokens.length >= 200) {
    const unique = new Set(tokens).size;
    const ttr = unique / tokens.length;
    if (ttr < 0.4) {
      issues.push({ type: 'low-ttr', text: `Vocabulary diversity ${(ttr * 100).toFixed(1)}% (${unique} unique / ${tokens.length} tokens)`, severity: 'low', suggestion: 'Text reuses a narrow word set. Vary nouns and verbs deliberately, or check if the topic genuinely warrants the repetition.' });
    }
  }

  // ── Paragraph length uniformity ──────────────────────────────
  if (paragraphs.length >= 4) {
    const paraLengths = paragraphs.map((p) => enTok.getSentences(p).length);
    const avg = paraLengths.reduce((a, b) => a + b, 0) / paraLengths.length;
    const allSimilar = paraLengths.every((l) => Math.abs(l - avg) <= 1);
    if (allSimilar && avg >= 3) {
      issues.push({ type: 'uniformity', text: `All paragraphs are ~${Math.round(avg)} sentences`, severity: 'low', suggestion: 'Vary paragraph length deliberately' });
    }
  }

  // ── Bold overuse ─────────────────────────────────────────────
  const boldMatches = text.match(/\*\*[^*]+\*\*/g) || [];
  if (boldMatches.length > 3) {
    issues.push({ type: 'formatting', text: `${boldMatches.length} bold phrases`, severity: 'medium', suggestion: 'Strip bold from most; restructure to lead with key info' });
  }

  // ── Score from the deduped issue list ───────────────────────
  let deduped = scoring.deduplicateIssues(issues);
  // Apply scene×tier matrix: suppress tiers the policy marks 'suppress' for
  // the active scene. Done after dedup, before scoring, so suppressed issues
  // neither surface nor contribute to the score.
  if (sceneMode) deduped = applyScenePolicy(deduped, sceneMode);
  let rawScore = 0;
  for (const issue of deduped) {
    rawScore += scoring.ISSUE_WEIGHTS[issue.type] ?? 2;
  }
  const normalizedScore = scoring.normalizeScore(rawScore, wordCount);
  const label = scoring.getLabel(normalizedScore);

  const regions = buildSentenceRegions(text, deduped);

  const tier1Count = deduped.filter((i) => i.type === 'tier1').length;
  const tier2Count = deduped.filter((i) => i.type === 'tier2').length;
  const tier3Count = deduped.filter((i) => i.type === 'tier3').length;

  const tier1Distinct = new Set(deduped.filter((i) => i.type === 'tier1').map((i) => (i.text || '').toLowerCase())).size;
  const hasTier2Cluster = tier2Clusters >= 2;
  const hasTransition = deduped.some((i) => i.type === 'transition');
  const denseAIVocab = wordCount >= 150 && tier1Distinct >= 5 && hasTier2Cluster && hasTransition;

  const trinary = classifyTrinary({
    score: normalizedScore, issues: deduped, regions, normFlags: norm.flags,
    wordCount, denseAIVocab,
  });

  return {
    score: normalizedScore,
    label,
    issues: deduped,
    stats: {
      wordCount, tier1Count, tier2Count, tier2Clusters, tier3Count, tier3Flags,
      patternCount: deduped.length - tier1Count - tier2Count - tier3Count,
      contextMode, contextModeFallback, sceneMode,
      normalization: norm.flags, quotedLines,
      unmappedHighlights: regions._unmapped ?? 0,
      denseAIVocab, tier1Distinct, voiceMode: options.voiceMode || 'none',
    },
    document_classification: trinary.classification,
    class_probabilities: trinary.probabilities,
    confidence_category: trinary.confidence,
    highlight_sentence_for_ai: regions,
    // ★ Addition layer: null when voiceMode==='none' (pure subtraction).
    // Independent dimension — never folded into score or fidelity.
    voice: analyzeVoice(text, 'en', options),
  };
}

// ─── Chinese analyzer ───────────────────────────────────────────────
// Mirrors analyzeEnglish's structure but uses zh tokenizers + substring/n-gram
// matching (Chinese has no whitespace, so tier vocab is matched as substrings,
// not tokens). Shares core/ scoring, normalize, fingerprints, trinary so the
// one-scorer + FN-bias contracts hold identically across languages.
function analyzeChinese(text, options = {}) {
  const requestedMode = options.contextMode || 'general';
  const contextMode = VALID_CONTEXT_MODES.has(requestedMode) ? requestedMode : 'general';
  const contextModeFallback = requestedMode !== contextMode ? requestedMode : null;
  const sceneMode = VALID_SCENE_MODES.has(options.sceneMode) ? options.sceneMode : null;

  // Pre-pass: strip Markdown blockquotes.
  let quotedLines = 0;
  const rawLines = text.split(/\r?\n/);
  const isQuote = rawLines.map((l) => /^\s*>\s/.test(l));
  const stripIdx = new Set();
  for (let i = 0; i < rawLines.length; i++) {
    if (isQuote[i] && ((isQuote[i - 1] && i > 0) || isQuote[i + 1])) {
      stripIdx.add(i);
      quotedLines++;
    }
  }
  text = rawLines.filter((_, i) => !stripIdx.has(i)).join('\n');

  const norm = normalizeText(text);
  text = norm.text;

  const wordCount = zhTok.countWords(text);
  if (wordCount < 10) {
    return { ...buildV2Defaults('UNSCORED', 'low'), score: 0, label: 'Too short', issues: [], stats: { wordCount, contextMode, contextModeFallback }, tooShort: true };
  }
  if (wordCount > MAX_WORDS) {
    return { ...buildV2Defaults('UNSCORED', 'low'), score: 0, label: 'Text too long', issues: [], stats: { wordCount, contextMode, contextModeFallback }, tooLong: true };
  }

  const paragraphs = zhTok.getParagraphs(text);
  const sentences = zhTok.getSentences(text);
  const issues = [];

  // ── Tier 1 Chinese vocab (substring match) ─────────────────────
  const tier1Found = new Set();
  for (const entry of zhVocab.T1) {
    const regex = new RegExp(entry.pattern.source, 'g');
    let match;
    while ((match = regex.exec(text)) !== null) {
      const key = match[0];
      if (tier1Found.has(key)) continue;
      tier1Found.add(key);
      issues.push({ type: 'tier1', text: match[0], severity: 'high', suggestion: entry.replace, lang: 'zh' });
    }
  }

  // ── Tier 2 Chinese clusters (2+ per paragraph) ─────────────────
  let tier2Clusters = 0;
  for (const para of paragraphs) {
    const found = new Set();
    for (const entry of zhVocab.T2) {
      if (!entry.literal || !para.includes(entry.literal)) continue;
      if (shouldSkipZhTier2Literal(para, entry.literal)) continue;
      found.add(entry.literal);
    }
    if (found.size >= 2) {
      tier2Clusters++;
      for (const w of found) {
        issues.push({ type: 'tier2', text: w, severity: 'medium', suggestion: '聚集出现时替换', lang: 'zh' });
      }
    }
  }

  // ── Tier 3 Chinese density ─────────────────────────────────────
  const tier3Counts = {};
  for (const entry of zhVocab.T3) {
    if (!entry.literal) continue;
    const count = (text.match(new RegExp(entry.literal, 'g')) || []).length;
    if (count > 0) tier3Counts[entry.literal] = count;
  }
  const densityThreshold = Math.max(3, Math.floor(wordCount * 0.03));
  let tier3Flags = 0;
  for (const [word, count] of Object.entries(tier3Counts)) {
    if (count >= densityThreshold) {
      tier3Flags++;
      issues.push({ type: 'tier3', text: `"${word}" x${count}`, severity: 'low', suggestion: `Overused (${count} times in ${wordCount} units)`, lang: 'zh' });
    }
  }

  // ── Chinese structural anti-patterns ───────────────────────────
  // Cross-lingual types share the en type so bilingual symmetry holds.
  issues.push(...zhTok.matchPatterns(text, zhStruct.BINARY_CONTRAST, 'false-concession', 'medium').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhStruct.SUMMARY_CLOSER, 'generic-conclusion', 'medium').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhStruct.MECHANICAL_ORDERING, 'template-phrase', 'medium').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhStruct.SYMMETRY_PADDING, 'template-phrase', 'medium').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhStruct.VALUE_INFLATION, 'significance-inflation', 'high').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhStruct.POSITIVE_CLOSER, 'future-narrative', 'medium').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhStruct.PSYCH_JUDGMENT, 'emotional-flatline', 'high').map((i) => ({ ...i, lang: 'zh' })));

  // ── Chinese translation tone (zh-only types) ───────────────────
  issues.push(...zhTok.matchPatterns(text, zhTone.PASSIVE_STACKING, 'zh-passive-stack', 'medium').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhTone.LONG_ATTRIBUTIVE, 'zh-long-attributive', 'low').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhTone.BASED_ON_OPENER, 'zh-translation-opener', 'low').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhTone.VIA_TO_CONSTRUCT, 'zh-via-to', 'low').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhTone.FOR_X_REGARD, 'zh-for-x-regard', 'low').map((i) => ({ ...i, lang: 'zh' })));
  issues.push(...zhTok.matchPatterns(text, zhTone.IN_X_ASPECT, 'zh-in-x-aspect', 'low').map((i) => ({ ...i, lang: 'zh' })));

  // ── Shared: AI-tool fingerprints (language-agnostic) ───────────
  issues.push(...zhTok.matchPatterns(text, fingerprints.AI_PLACEHOLDERS, 'ai-placeholder', 'critical'));
  issues.push(...zhTok.matchPatterns(text, fingerprints.AI_CITATION_MARKUP, 'ai-citation-markup', 'critical'));
  issues.push(...zhTok.matchPatterns(text, fingerprints.AI_UTM_SOURCE, 'ai-utm-source', 'critical'));

  // ── Normalization-trigger flag ─────────────────────────────────
  if (norm.flags.zeroWidth > 0 || norm.flags.homoglyph >= 2) {
    issues.push({ type: 'normalization-flag', text: `${norm.flags.zeroWidth} zero-width + ${norm.flags.homoglyph} homoglyph swap${norm.flags.homoglyph === 1 ? '' : 's'}`, severity: 'critical', suggestion: '文本含不可见/形近字符，疑似 humanizer 绕过工具。请自行重新输入。' });
  }

  // ── Chinese sentence-length uniformity (stylometric) ───────────
  if (sentences.length >= 5) {
    const lengths = sentences.map((s) => s.replace(/\s/g, '').length);
    const avg = lengths.reduce((a, b) => a + b, 0) / lengths.length;
    const variance = lengths.reduce((sum, l) => sum + Math.pow(l - avg, 2), 0) / lengths.length;
    const stdDev = Math.sqrt(variance);
    const cv = avg > 0 ? stdDev / avg : 0;
    if (cv < 0.25 && avg > 8) {
      issues.push({ type: 'uniformity', text: `句长集中在 ${Math.round(avg)} 字（变化小）`, severity: 'medium', suggestion: '长短句交替，加入短句或碎片句', lang: 'zh' });
    }
  }

  // ── Score from the deduped issue list (same scorer as en) ──────
  let deduped = scoring.deduplicateIssues(issues);
  // Apply scene×tier matrix (same as en — shared core/policy).
  if (sceneMode) deduped = applyScenePolicy(deduped, sceneMode);
  let rawScore = 0;
  for (const issue of deduped) {
    rawScore += scoring.ISSUE_WEIGHTS[issue.type] ?? 2;
  }
  const normalizedScore = scoring.normalizeScore(rawScore, wordCount);
  const label = scoring.getLabel(normalizedScore);
  const regions = buildSentenceRegions(text, deduped);

  const tier1Count = deduped.filter((i) => i.type === 'tier1').length;
  const tier2Count = deduped.filter((i) => i.type === 'tier2').length;
  const tier3Count = deduped.filter((i) => i.type === 'tier3').length;
  const tier1Distinct = new Set(deduped.filter((i) => i.type === 'tier1').map((i) => (i.text || '').toLowerCase())).size;

  // denseAIVocab for Chinese: tier1-heavy + tier2 clusters. No English
  // "transition" type in zh, so use generic-conclusion as the structural
  // corroborator instead.
  const hasStructural = deduped.some((i) => i.type === 'generic-conclusion' || i.type === 'significance-inflation');
  const denseAIVocab = wordCount >= 100 && tier1Distinct >= 5 && tier2Clusters >= 2 && hasStructural;

  const trinary = classifyTrinary({
    score: normalizedScore, issues: deduped, regions, normFlags: norm.flags,
    wordCount, denseAIVocab,
  });

  return {
    score: normalizedScore,
    label,
    issues: deduped,
    stats: {
      wordCount, charCountZh: zhTok.countCjkChars(text),
      tier1Count, tier2Count, tier2Clusters, tier3Count, tier3Flags,
      patternCount: deduped.length - tier1Count - tier2Count - tier3Count,
      contextMode, contextModeFallback, sceneMode,
      normalization: norm.flags, quotedLines,
      unmappedHighlights: regions._unmapped ?? 0,
      denseAIVocab, tier1Distinct, lang: 'zh', voiceMode: options.voiceMode || 'none',
    },
    document_classification: trinary.classification,
    class_probabilities: trinary.probabilities,
    confidence_category: trinary.confidence,
    highlight_sentence_for_ai: regions,
    // ★ Addition layer (zh): same contract as en — independent dimension.
    voice: analyzeVoice(text, 'zh', options),
  };
}

module.exports = {
  analyzeText,
  normalizeText,
  getLabel: scoring.getLabel,
  getColor: scoring.getColor,
  SEVERITY_LABELS: { critical: 'P0', high: 'P1', medium: 'P2', low: 'P3' },
  TYPE_LABELS: {
    tier1: 'AI vocabulary', tier2: 'Word cluster', tier3: 'Overused word',
    transition: 'AI transition', chatbot: 'Chatbot artifact', sycophantic: 'Sycophantic tone',
    filler: 'Filler phrase', 'generic-conclusion': 'Generic conclusion',
    'lets-construction': '"Let\'s" opener', 'reasoning-artifact': 'Reasoning artifact',
    'acknowledgment-loop': 'Acknowledgment loop', 'significance-inflation': 'Significance inflation',
    'vague-attribution': 'Vague attribution', 'hollow-intensifier': 'Hollow intensifier',
    'emotional-flatline': 'Emotional flatline', 'novelty-inflation': 'Novelty inflation',
    'cutoff-disclaimer': 'Cutoff disclaimer', 'template-phrase': 'Template phrase',
    'false-concession': 'False concession', 'rhetorical-question': 'Rhetorical question',
    'confidence-calibration': 'Confidence stacking', 'em-dash': 'Em dash overuse',
    uniformity: 'Rhythm uniformity', formatting: 'Formatting',
    'tier3-phrase': 'Boilerplate phrase', 'tier3-phrase-cluster': 'Boilerplate cluster',
    'hashtag-stuff': 'Hashtag stuffing', 'bullet-np-list': 'Bullet-NP list',
    'hedge-stack': 'Hedge-stacked prediction', 'future-narrative': 'Generic future narrative',
    'real-actual-inflation': '"Real/actual" inflation', 'social-cta-closer': 'Engagement-bait closer',
    'formulaic-opener': 'Formulaic opener', 'title-case-header': 'Title Case header',
    'parenthetical-hedge': 'Parenthetical hedge', 'smart-punct-signature': 'Smart-punct signature',
    'punct-distribution': 'Punctuation distribution', 'fnword-trigram-entropy': 'Grammar repetition',
    'cross-para-burstiness': 'Cross-paragraph rhythm', 'normalization-flag': 'Bypass-trick chars',
    'low-ttr': 'Low vocabulary diversity', 'ai-placeholder': 'Unfilled placeholder',
    'ai-citation-markup': 'Chatbot citation markup leak', 'ai-utm-source': 'AI-tool URL parameter',
    // zh-only translation-tone types (CATEGORIES.md lang=zh)
    'zh-passive-stack': '被动语态堆砌', 'zh-long-attributive': '长定语结构',
    'zh-translation-opener': '基于/通过开头', 'zh-via-to': '通过…来…结构',
    'zh-for-x-regard': '对于…而言', 'zh-in-x-aspect': '在…方面',
  },
};

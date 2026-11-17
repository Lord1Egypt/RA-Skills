const parentDirectory = '..';
const utilityModule = (...segments) => new URL([parentDirectory, 'utils', ...segments].join('/'), import.meta.url);
const { sanitizeMarkdown } = await import(utilityModule('sanitizer.mjs'));
const { mean, punctuationRates } = await import(utilityModule('metrics-core.mjs'));
const { isCJKText, tokenizeText } = await import(utilityModule('tokenizer.mjs'));

const HAN = /[\u4e00-\u9fff]/gu;
const KANA = /[\u3040-\u30ff]/u;
const ARABIC = /[\u0600-\u06ff]/u;
const ID_EXCLUSIVE_WORDS = new Set(['tidak', 'karena', 'bisa', 'seperti', 'dari', 'bahwa']);
const MS_EXCLUSIVE_WORDS = new Set(['tak', 'kerana', 'boleh', 'bagi', 'daripada', 'bahawa', 'beliau']);

function round(value, places = 4) {
  const factor = 10 ** places;
  return Math.round(value * factor) / factor;
}

function detectLanguage(text, words, rules) {
  if (KANA.test(text)) return 'ja';
  if (ARABIC.test(text)) return 'ar';
  const hanCount = (text.match(HAN) ?? []).length;
  if (hanCount > 0 && isCJKText(text)) return 'zh';

  const scores = new Map();
  for (const [language, rule] of Object.entries(rules)) {
    let score = 0;
    const stopwords = new Set(rule.stopwords ?? []);
    for (const word of words) if (stopwords.has(word)) score += 1;
    scores.set(language, score);
  }
  if (scores.has('id') && scores.has('ms')) {
    const idExclusive = words.filter((word) => ID_EXCLUSIVE_WORDS.has(word)).length;
    const msExclusive = words.filter((word) => MS_EXCLUSIVE_WORDS.has(word)).length;
    scores.set('id', scores.get('id') + idExclusive * 2);
    scores.set('ms', scores.get('ms') + msExclusive * 2);
  }

  const [language, score] = [...scores.entries()].sort((left, right) => right[1] - left[1])[0] ?? ['universal', 0];
  return score >= Math.max(2, Math.ceil(words.length * 0.04)) ? language : 'universal';
}

function mattrThreshold(thresholds, language, tokenized) {
  if (typeof thresholds.mattr?.[language] === 'number') return thresholds.mattr[language];
  return isCJKText(tokenized.words.join('')) ? 0.68 : 0.72;
}

function locationFor(sentence) {
  return `Paragraph ${sentence.paragraphIndex}, Sentence ${sentence.sentenceIndex}`;
}

function regexFor(pattern) {
  return new RegExp(pattern, 'giu');
}

function patternViolations(tokenized, rules, wordCount) {
  if (!rules?.patterns) return [];
  const violations = [];
  for (const rule of rules.patterns) {
    const candidates = [];
    const sentences = rule.scope === 'paragraph-start'
      ? tokenized.paragraphs.map((paragraph) => paragraph.sentences[0]).filter(Boolean)
      : tokenized.sentences;

    for (const sentence of sentences) {
      const regex = regexFor(rule.pattern);
      for (const match of sentence.text.matchAll(regex)) candidates.push({ sentence, match: match[0] });
    }

    const allowed = rule.maxOccurrences == null
      ? 0
      : rule.maxOccurrences * Math.max(1, Math.ceil(wordCount / (rule.perWords || wordCount || 1)));
    for (const candidate of candidates.slice(allowed)) {
      violations.push({
        type: rule.type,
        ruleId: rule.id,
        location: locationFor(candidate.sentence),
        match: candidate.match,
        fixInstruction: rule.fixInstruction,
      });
    }
  }
  return violations;
}

function monotonyViolations(tokenized) {
  const violations = [];
  for (const paragraph of tokenized.paragraphs) {
    for (let index = 0; index <= paragraph.sentences.length - 3; index += 1) {
      const window = paragraph.sentences.slice(index, index + 3);
      const lengths = window.map((sentence) => sentence.wordCount);
      if (Math.abs(lengths[1] - lengths[0]) <= 3 && Math.abs(lengths[2] - lengths[1]) <= 3) {
        violations.push({
          type: 'MONOTONOUS_RHYTHM',
          location: `Paragraph ${paragraph.paragraphIndex}, Sentences ${window[0].sentenceIndex}-${window[2].sentenceIndex}`,
          lengths,
          fixInstruction: `Sentence lengths are uniform (${lengths.join(', ')} words). Split one sentence into a short statement or merge two into a longer clause.`,
        });
      }
    }
  }
  return violations;
}

function structuralViolations(tokenized, metrics) {
  const violations = [];
  if (metrics.wordCount >= 150 && metrics.compressionRatio < 0.42) {
    violations.push({
      type: 'LOW_ENTROPY_REPETITION',
      location: 'Whole text',
      fixInstruction: 'Remove repeated templates and vary concrete sentence structures.',
    });
  }

  for (let index = 0; index <= tokenized.paragraphs.length - 3; index += 1) {
    const window = tokenized.paragraphs.slice(index, index + 3);
    const counts = window.map((paragraph) => paragraph.sentences.length);
    if (counts[0] > 0 && counts.every((count) => count === counts[0])) {
      violations.push({
        type: 'SYMMETRIC_PARAGRAPHS',
        location: `Paragraphs ${window[0].paragraphIndex}-${window[2].paragraphIndex}`,
        counts,
        fixInstruction: 'Merge or split a paragraph where the content supports a different rhythm.',
      });
    }
  }

  for (const paragraph of tokenized.paragraphs) {
    const starters = new Map();
    for (const sentence of paragraph.sentences) {
      const starter = sentence.words[0];
      if (!starter) continue;
      const group = starters.get(starter) ?? [];
      group.push(sentence.sentenceIndex);
      starters.set(starter, group);
    }
    for (const [starter, indexes] of starters) {
      if (indexes.length >= 3) {
        violations.push({
          type: 'REPETITIVE_STARTERS',
          location: `Paragraph ${paragraph.paragraphIndex}, Sentences ${indexes.join(', ')}`,
          match: starter,
          fixInstruction: 'Change one sentence opening or combine sentences where the subject repeats.',
        });
      }
    }
  }
  return violations;
}

function statisticalViolations(metrics, thresholds, mattrTarget) {
  const violations = [];
  const cvTarget = metrics.sentenceCount >= 8 ? thresholds.burstinessCVLong : thresholds.burstinessCVShort;
  if (metrics.burstinessCV < cvTarget) {
    violations.push({
      type: 'LOW_BURSTINESS',
      location: 'Whole text',
      actual: round(metrics.burstinessCV),
      target: cvTarget,
      fixInstruction: 'Vary sentence lengths by splitting one uniform sentence and merging another where the meaning supports it.',
    });
  }
  if (metrics.sentenceCount >= 8 && (metrics.shortSentenceRatio < thresholds.shortSentenceRatio || metrics.longSentenceRatio < thresholds.longSentenceRatio)) {
    violations.push({
      type: 'MISSING_SENTENCE_RANGE',
      location: 'Whole text',
      shortSentenceRatio: round(metrics.shortSentenceRatio),
      longSentenceRatio: round(metrics.longSentenceRatio),
      fixInstruction: 'Add a supported sentence of 6 words or fewer and a supported sentence of 26 words or more until both distribution thresholds pass.',
    });
  }
  if (metrics.adjacentDelta < thresholds.adjacentDelta) {
    violations.push({
      type: 'LOW_ADJACENT_DELTA',
      location: 'Whole text',
      actual: round(metrics.adjacentDelta),
      target: thresholds.adjacentDelta,
      fixInstruction: 'Change neighboring sentence lengths by splitting or merging only where the content allows it.',
    });
  }
  if (metrics.mattr < mattrTarget) {
    violations.push({
      type: 'LOW_LEXICAL_DIVERSITY',
      location: 'Whole text',
      actual: round(metrics.mattr),
      target: mattrTarget,
      fixInstruction: 'Replace repeated generic wording with precise terms already supported by the source.',
    });
  }
  return violations;
}

function morphologyViolations(tokenized, morphology) {
  if (!morphology) return { violations: [], nominalizationRatio: 0, passiveRatio: 0 };
  const words = tokenized.words;
  const nominalizationPattern = new RegExp(morphology.nominalizationPattern, 'iu');
  const nominalizationWhitelist = new Set(morphology.nominalizationWhitelist);
  const nominalizations = words.filter((word) => nominalizationPattern.test(word) && !nominalizationWhitelist.has(word));
  const passivePattern = new RegExp(morphology.passivePattern, 'iu');
  const loanwordExclusion = new RegExp(morphology.loanwordExclusionPattern, 'iu');
  const loanwordSuffixExclusion = new RegExp(morphology.loanwordSuffixExclusionPattern ?? '$^', 'iu');
  const passives = words.filter((word) => passivePattern.test(word) && !loanwordExclusion.test(word) && !loanwordSuffixExclusion.test(word));
  const nominalizationRatio = words.length ? nominalizations.length / words.length : 0;
  const passiveRatio = words.length ? passives.length / words.length : 0;
  const violations = [];

  if (nominalizationRatio > morphology.nominalizationMaxRatio) {
    violations.push({
      type: 'EXCESSIVE_NOMINALIZATION',
      location: 'Whole text',
      ratio: round(nominalizationRatio),
      matches: [...new Set(nominalizations)],
      fixInstruction: 'Replace abstract nominalizations with concrete actors and verbs.',
    });
  }
  if (passiveRatio > morphology.passiveMaxRatio) {
    violations.push({
      type: 'PASSIVE_BLOATING',
      location: 'Whole text',
      ratio: round(passiveRatio),
      matches: [...new Set(passives)],
      fixInstruction: 'Name the actor and use an active verb where the actor is known.',
    });
  }

  const openingPattern = new RegExp(morphology.subordinateOpeningPattern, 'iu');
  let foundConsecutiveOpening = false;
  for (const paragraph of tokenized.paragraphs) {
    for (let index = 1; index < paragraph.sentences.length; index += 1) {
      const previous = paragraph.sentences[index - 1];
      const current = paragraph.sentences[index];
      if (!openingPattern.test(previous.text) || !openingPattern.test(current.text)) continue;
      violations.push({
        type: 'PASSIVE_BLOATING',
        location: `Paragraph ${paragraph.paragraphIndex}, Sentences ${previous.sentenceIndex}-${current.sentenceIndex}`,
        match: 'Two or more consecutive sentences start with translationese subordinate clauses',
        fixInstruction: 'Rewrite to start directly with the active subject (Subjek + Predikat).',
      });
      foundConsecutiveOpening = true;
      break;
    }
    if (foundConsecutiveOpening) break;
  }
  return { violations, nominalizationRatio, passiveRatio };
}

function voiceDeviation(metrics, tokenized, text, profile) {
  const targets = profile?.targets ?? profile?.metrics;
  if (!targets) return 0;
  const actual = {
    meanSentenceLength: metrics.meanSentenceLength,
    burstinessCV: metrics.burstinessCV,
    adjacentDelta: metrics.adjacentDelta,
    mattr: metrics.mattr,
    averageParagraphSentenceCount: mean(tokenized.paragraphs.map((paragraph) => paragraph.sentences.length)),
  };
  const deviations = [];
  for (const key of Object.keys(actual)) {
    if (typeof targets[key] !== 'number') continue;
    deviations.push(Math.min(3, Math.abs(actual[key] - targets[key]) / Math.max(Math.abs(targets[key]), 0.01)));
  }
  const targetPunctuation = targets.punctuationRates;
  if (targetPunctuation) {
    const actualPunctuation = punctuationRates(text, metrics.wordCount);
    for (const key of Object.keys(targetPunctuation)) {
      deviations.push(Math.min(3, Math.abs(actualPunctuation[key] - targetPunctuation[key]) / Math.max(Math.abs(targetPunctuation[key]), 0.01)));
    }
  }
  const result = deviations.length ? mean(deviations) : 0;
  return result < 0.0005 ? 0 : result;
}

function scoreResult(metrics, violations, thresholds, mattrTarget) {
  const cvTarget = metrics.sentenceCount >= 8 ? thresholds.burstinessCVLong : thresholds.burstinessCVShort;
  let burstinessPenalty = metrics.burstinessCV < cvTarget ? Math.min(25, Math.round((cvTarget - metrics.burstinessCV) * 100)) : 0;
  if (metrics.sentenceCount >= 8 && (metrics.shortSentenceRatio < thresholds.shortSentenceRatio || metrics.longSentenceRatio < thresholds.longSentenceRatio)) {
    burstinessPenalty = Math.min(25, burstinessPenalty + 8);
  }
  const rhythmPenalty = Math.min(20, violations.filter((violation) => violation.type === 'MONOTONOUS_RHYTHM').length * 6);
  const lexicalPenalty = Math.min(30, violations.reduce((total, violation) => {
    if (violation.type === 'SLOP_PHRASE' || violation.type === 'DEFINITIONAL_OPENING') return total + 5;
    if (violation.type === 'STRUCTURAL_CLICHE') return total + 4;
    return total;
  }, 0));
  const morphologyPenalty = Math.min(15,
    (violations.some((violation) => violation.type === 'EXCESSIVE_NOMINALIZATION') ? 7.5 : 0)
    + Math.min(15, violations.filter((violation) => violation.type === 'PASSIVE_BLOATING').length * 7.5));
  const vocabularyPenalty = metrics.mattr < mattrTarget ? 5 : 0;
  const entropyPenalty = violations.some((violation) => ['LOW_ENTROPY_REPETITION', 'SYMMETRIC_PARAGRAPHS', 'REPETITIVE_STARTERS'].includes(violation.type)) ? 5 : 0;
  const profilePenalty = violations.some((violation) => violation.type === 'VOICE_PROFILE_DEVIATION') ? 5 : 0;
  const vocabularyAndProfilePenalty = Math.min(10, vocabularyPenalty + entropyPenalty + profilePenalty);
  return Math.max(0, Math.round(100 - burstinessPenalty - rhythmPenalty - lexicalPenalty - morphologyPenalty - vocabularyAndProfilePenalty));
}

export function createAnalyzer({ rules, defaultProfile, calculateMetrics, calculateMetricsAsync }) {
  if (!rules || !defaultProfile || typeof calculateMetrics !== 'function') {
    throw new TypeError('createAnalyzer requires rules, defaultProfile, and calculateMetrics');
  }

  const prepare = (input, options) => {
    const sanitized = sanitizeMarkdown(input);
    const requestedLanguage = String(options.language ?? 'auto').toLowerCase();
    const initial = tokenizeText(sanitized, requestedLanguage);
    const language = requestedLanguage === 'auto' ? detectLanguage(sanitized, initial.words, rules) : requestedLanguage;
    return {
      sanitized,
      language,
      rulePack: rules[language] ? language : 'universal',
      tokenized: language === requestedLanguage ? initial : tokenizeText(sanitized, language),
    };
  };

  const analyzePrepared = ({ sanitized, language, rulePack, tokenized }, options, metrics) => {
    const profile = options.profile ?? defaultProfile;
    const thresholds = { ...defaultProfile.thresholds, ...(profile.thresholds ?? {}) };
    const mattrTarget = mattrThreshold(thresholds, language, tokenized);
    const patternMatches = patternViolations(tokenized, rules[language], metrics.wordCount);

    if (metrics.wordCount < thresholds.minimumWords || metrics.sentenceCount < thresholds.minimumSentences) {
      const violations = patternMatches.filter((violation) => violation.type === 'SLOP_PHRASE');
      return {
        status: 'SKIP',
        score: 100,
        language,
        rulePack,
        warning: 'Text too short for statistical stylometry (< 3 sentences)',
        metrics: Object.fromEntries(Object.entries({ ...metrics, nominalizationRatio: 0, passiveRatio: 0, voiceProfileDeviation: 0 }).map(([key, value]) => [key, typeof value === 'number' ? round(value) : value])),
        violations,
      };
    }

    const morphology = morphologyViolations(tokenized, rules[language]?.morphology);
    metrics.nominalizationRatio = morphology.nominalizationRatio;
    metrics.passiveRatio = morphology.passiveRatio;
    metrics.voiceProfileDeviation = voiceDeviation(metrics, tokenized, sanitized, profile);
    const profileTargets = profile.targets ?? profile.metrics ?? {};
    const targetMean = Number(profileTargets.meanSentenceLength);
    const meanDeviation = targetMean > 0 ? Math.abs(metrics.meanSentenceLength - targetMean) / targetMean : 0;
    const profileViolations = options.profile != null && meanDeviation > 0.3 ? [{
      type: 'VOICE_PROFILE_DEVIATION',
      location: 'Global Document',
      match: 'Mean sentence length deviates >30% from target voice profile',
      fixInstruction: 'Adjust overall sentence complexity so mean sentence length approaches the target profile.',
    }] : [];
    const violations = [
      ...patternMatches,
      ...monotonyViolations(tokenized),
      ...structuralViolations(tokenized, metrics),
      ...morphology.violations,
      ...profileViolations,
      ...statisticalViolations(metrics, thresholds, mattrTarget),
    ];
    const score = scoreResult(metrics, violations, thresholds, mattrTarget);
    const cvTarget = metrics.sentenceCount >= 8 ? thresholds.burstinessCVLong : thresholds.burstinessCVShort;
    const forbidden = violations.some((violation) => violation.type === 'SLOP_PHRASE' || violation.type === 'DEFINITIONAL_OPENING');
    const rhythmPass = metrics.adjacentDelta >= thresholds.adjacentDelta;
    const distributionPass = metrics.sentenceCount < 8 || (metrics.shortSentenceRatio >= thresholds.shortSentenceRatio && metrics.longSentenceRatio >= thresholds.longSentenceRatio);
    const status = score >= thresholds.passScore && !forbidden && metrics.burstinessCV >= cvTarget && rhythmPass && distributionPass ? 'PASS' : 'FAIL';

    return {
      status,
      score,
      language,
      rulePack,
      metrics: Object.fromEntries(Object.entries(metrics).map(([key, value]) => [key, typeof value === 'number' ? round(value) : value])),
      violations,
    };
  };

  return {
    analyzeText(input, options = {}) {
      const prepared = prepare(input, options);
      return analyzePrepared(prepared, options, calculateMetrics(prepared.tokenized, prepared.sanitized));
    },
    async analyzeTextAsync(input, options = {}) {
      if (typeof calculateMetricsAsync !== 'function') return this.analyzeText(input, options);
      const prepared = prepare(input, options);
      const metrics = await calculateMetricsAsync(prepared.tokenized, prepared.sanitized);
      return analyzePrepared(prepared, options, metrics);
    },
  };
}

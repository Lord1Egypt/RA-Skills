export function mean(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : 0;
}

export function standardDeviation(values) {
  if (!values.length) return 0;
  const average = mean(values);
  return Math.sqrt(mean(values.map((value) => (value - average) ** 2)));
}

export function coefficientOfVariation(values) {
  const average = mean(values);
  return average ? standardDeviation(values) / average : 0;
}

export function adjacentDelta(values) {
  if (values.length < 2) return 0;
  let total = 0;
  for (let index = 1; index < values.length; index += 1) total += Math.abs(values[index] - values[index - 1]);
  return total / (values.length - 1);
}

export function mattr(words, requestedWindow) {
  if (!words.length) return 0;
  const window = Math.min(words.length, requestedWindow ?? Math.min(50, Math.max(10, Math.floor(words.length / 2))));
  if (words.length <= window) return new Set(words).size / words.length;
  let total = 0;
  let windows = 0;
  for (let index = 0; index <= words.length - window; index += 1) {
    total += new Set(words.slice(index, index + window)).size / window;
    windows += 1;
  }
  return total / windows;
}

export function punctuationRates(text, wordCount) {
  const denominator = wordCount || 1;
  const count = (pattern) => (String(text ?? '').match(pattern) ?? []).length / denominator;
  return {
    comma: count(/,/g),
    semicolon: count(/;/g),
    colon: count(/:/g),
    question: count(/\?/g),
    exclamation: count(/!/g),
    parentheses: count(/[()]/g) / 2,
    dash: count(/—|\s--\s/g),
  };
}

export function calculateMetricsFromCompressionRatio(tokenized, compressionRatio) {
  const lengths = tokenized.sentences.map((sentence) => sentence.wordCount);
  const wordCount = tokenized.words.length;
  const sentenceCount = lengths.length;
  return {
    wordCount,
    sentenceCount,
    meanSentenceLength: mean(lengths),
    stdDev: standardDeviation(lengths),
    burstinessCV: coefficientOfVariation(lengths),
    adjacentDelta: adjacentDelta(lengths),
    shortSentenceRatio: sentenceCount ? lengths.filter((length) => length <= 6).length / sentenceCount : 0,
    longSentenceRatio: sentenceCount ? lengths.filter((length) => length >= 26).length / sentenceCount : 0,
    mattr: mattr(tokenized.words),
    compressionRatio,
  };
}

export function createMetrics({ encode, deflateRaw }) {
  if (typeof encode !== 'function' || typeof deflateRaw !== 'function') {
    throw new TypeError('createMetrics requires encode and deflateRaw functions');
  }

  const compressionRatio = (text) => {
    const bytes = encode(String(text ?? '').trim());
    return bytes.length ? deflateRaw(bytes).length / bytes.length : 0;
  };

  const calculateMetrics = (tokenized, normalizedText) => calculateMetricsFromCompressionRatio(
    tokenized,
    compressionRatio(normalizedText),
  );

  return { compressionRatio, calculateMetrics };
}

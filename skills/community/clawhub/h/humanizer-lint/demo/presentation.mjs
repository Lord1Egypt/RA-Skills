const projectRoot = '..';
const { tokenizeText } = await import(new URL([projectRoot, 'scripts', 'utils', 'tokenizer.mjs'].join('/'), import.meta.url));

const SAMPLE_IDS = new Set(['en', 'id', 'es', 'ms', 'fr', 'de', 'pt', 'zh'].flatMap((code) => [`ai-${code}`, `human-${code}`]));
const UI_LANGUAGES = new Set(['en', 'id', 'es', 'ms', 'fr', 'de', 'pt', 'zh']);
const TARGET_LANGUAGES = new Set(['auto', 'en', 'id', 'es', 'ms', 'fr', 'de', 'pt', 'zh', 'universal']);

const LANGUAGE_LABELS = {
  auto: 'Auto-Detect (Recommended)',
  en: 'English (Tier 1 Pack)',
  id: 'Bahasa Indonesia (Tier 1 Pack)',
  es: 'Español (Tier 1 Pack)',
  ms: 'Bahasa Melayu (Tier 1 Pack)',
  fr: 'Français (Tier 1 Pack)',
  de: 'Deutsch (Tier 1 Pack)',
  pt: 'Português (Tier 1 Pack)',
  zh: '中文 / Mandarin (Tier 1 Pack)',
  universal: 'Universal Stylometry (Tier 2)',
};

export function languageLabel(language) {
  return LANGUAGE_LABELS[language] ?? LANGUAGE_LABELS.universal;
}

export function parseDemoQuery(search) {
  const query = new URLSearchParams(search);
  const sample = query.get('sample');
  const language = query.get('lang');
  const targetLang = query.get('targetLang');
  return {
    sample: SAMPLE_IDS.has(sample) ? sample : null,
    language: UI_LANGUAGES.has(language) ? language : null,
    targetLang: TARGET_LANGUAGES.has(targetLang) ? targetLang : null,
  };
}

function sentenceAt(text, location) {
  const found = /^Paragraph (\d+), Sentence (\d+)/.exec(location ?? '');
  if (!found) return '';
  const [, paragraphIndex, sentenceIndex] = found.map(Number);
  const tokenized = tokenizeText(text, 'auto');
  return tokenized.paragraphs
    .find((paragraph) => paragraph.paragraphIndex === paragraphIndex)
    ?.sentences.find((sentence) => sentence.sentenceIndex === sentenceIndex)
    ?.text ?? '';
}

export function diagnosticExcerpt(text, violation) {
  return sentenceAt(text, violation.location) || violation.match || violation.location || '';
}

export function buildAutoFixPrompt({ text, report }) {
  const violations = report.violations.map((violation) => [
    `- ${violation.type} — ${violation.location}`,
    `  Instruction: ${violation.fixInstruction}`,
  ].join('\n')).join('\n');
  const metrics = Object.entries(report.metrics)
    .filter(([key]) => ['burstinessCV', 'adjacentDelta', 'mattr'].includes(key))
    .map(([key, value]) => `- ${key}: ${value}`)
    .join('\n');

  return `# Targeted prose revision\n\nRewrite only the sentences cited below in ${languageLabel(report.language)}. Preserve facts, names, numbers, quotations, and the original language. Remove flagged slop without adding unsupported claims. Aim for stronger sentence-length variation and no slop phrases, then re-run humanizer-lint to verify the result.\n\n## Analyzer report\n- Status: ${report.status}\n- Score: ${report.score}/100\n- Detected language: ${languageLabel(report.language)}\n- Rule pack: ${languageLabel(report.rulePack)}\n\n## Measured metrics\n${metrics}\n\n## Flagged diagnostics\n${violations}\n\n## Original text\n${text}`;
}

import { createBrowserAnalyzer } from './analyzer-browser.mjs';
import { I18N, UI_LANGUAGE_CODES, UI_LANGUAGE_NAMES } from './i18n.mjs';
import { buildAutoFixPrompt, diagnosticExcerpt, languageLabel, parseDemoQuery } from './presentation.mjs';
import { DEMO_SAMPLES } from './samples.mjs';

const LANGUAGE_KEY = 'humanizer-lint.language';
const THEME_KEY = 'humanizer-lint.theme';
const COMMANDS = {
  skill: 'npx skills add yanstd888/humanizer-lint',
  cli: 'npx humanizer-lint --file draft.md --lang auto',
};
const text = document.querySelector('#text');
const analyze = document.querySelector('#analyze');
const error = document.querySelector('#error');
const result = document.querySelector('#result');
const score = document.querySelector('#score');
const status = document.querySelector('#status');
const language = document.querySelector('#language');
const analysisLanguage = document.querySelector('#analysis-language');
const findings = document.querySelector('#findings');
const diagnostic = document.querySelector('#diagnostic');
const diagnosticText = document.querySelector('#diagnostic-text');
const themeToggle = document.querySelector('#theme-toggle');
const interfaceLanguage = document.querySelector('#interface-language');
const commandButtons = [...document.querySelectorAll('[data-command]')];
const sampleList = document.querySelector('#sample-list');
const installCommand = document.querySelector('#install-command');
const copyInstall = document.querySelector('#copy-install');
const copyAutoFix = document.querySelector('#copy-autofix');
const copyStatus = document.querySelector('#copy-status');
const metricElements = {
  burstiness: document.querySelector('#metric-burstiness'),
  rhythm: document.querySelector('#metric-rhythm'),
  lexical: document.querySelector('#metric-lexical'),
  slop: document.querySelector('#metric-slop'),
};
const queryState = parseDemoQuery(window.location.search);
let currentLanguage = 'en';
let currentTheme = 'light';
let currentCommand = 'skill';
let analyzer;
let defaultProfile;
let lastResult;
let lastText = '';
let ready = false;

function stored(key) {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function save(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // ponytail: preference persistence is optional when browser storage is unavailable.
  }
}

function initialLanguage() {
  const saved = stored(LANGUAGE_KEY);
  if (UI_LANGUAGE_CODES.includes(saved)) return saved;
  const browserCode = navigator.language?.toLowerCase().split('-')[0];
  return UI_LANGUAGE_CODES.includes(browserCode) ? browserCode : 'en';
}

function initialTheme() {
  const saved = stored(THEME_KEY);
  if (saved === 'light' || saved === 'dark') return saved;
  return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function copy() {
  return I18N[currentLanguage];
}

function sampleLabel(id) {
  const [kind, code] = id.split('-');
  return `${copy()[kind === 'ai' ? 'sampleAi' : 'sampleHuman']} (${UI_LANGUAGE_NAMES[code]}) — ${kind === 'ai' ? 'FAIL' : 'PASS'}`;
}

function renderSampleButtons() {
  sampleList.replaceChildren();
  for (const code of UI_LANGUAGE_CODES) {
    for (const kind of ['ai', 'human']) {
      const id = `${kind}-${code}`;
      const button = document.createElement('button');
      button.type = 'button';
      button.dataset.sample = id;
      button.textContent = sampleLabel(id);
      button.addEventListener('click', () => loadSample(id));
      sampleList.append(button);
    }
  }
}

function setError(message = '') {
  error.textContent = message;
  error.hidden = !message;
}

function formatNumber(value, fractionDigits = 2) {
  return new Intl.NumberFormat(currentLanguage === 'zh' ? 'zh-CN' : `${currentLanguage}-${currentLanguage === 'en' ? 'US' : currentLanguage.toUpperCase()}`, {
    maximumFractionDigits: fractionDigits,
    minimumFractionDigits: fractionDigits,
  }).format(value);
}

function formatPercent(value) {
  return new Intl.NumberFormat(currentLanguage === 'zh' ? 'zh-CN' : `${currentLanguage}-${currentLanguage === 'en' ? 'US' : currentLanguage.toUpperCase()}`, {
    maximumFractionDigits: 1,
    style: 'percent',
  }).format(value);
}

function setMetric(element, value, detail, healthy) {
  element.replaceChildren();
  const primary = document.createElement('strong');
  primary.textContent = value;
  const secondary = document.createElement('span');
  secondary.textContent = detail;
  element.dataset.status = healthy ? 'optimal' : 'low';
  element.append(primary, secondary);
}

function renderMetrics(report) {
  const { metrics } = report;
  const thresholds = defaultProfile.thresholds;
  const cvTarget = metrics.sentenceCount >= 8 ? thresholds.burstinessCVLong : thresholds.burstinessCVShort;
  const cvHealthy = metrics.burstinessCV >= cvTarget;
  setMetric(
    metricElements.burstiness,
    formatNumber(metrics.burstinessCV),
    `${cvHealthy ? copy().metricOptimal : copy().metricLow} · ${copy().metricTarget} ≥ ${formatNumber(cvTarget)}`,
    cvHealthy,
  );

  const rhythmHealthy = metrics.adjacentDelta >= thresholds.adjacentDelta
    && (metrics.sentenceCount < 8 || (metrics.shortSentenceRatio >= thresholds.shortSentenceRatio && metrics.longSentenceRatio >= thresholds.longSentenceRatio));
  setMetric(
    metricElements.rhythm,
    `Δ ${formatNumber(metrics.adjacentDelta)}`,
    `${rhythmHealthy ? copy().metricOptimal : copy().metricLow} · ${copy().metricShort} ${formatPercent(metrics.shortSentenceRatio)} · ${copy().metricLong} ${formatPercent(metrics.longSentenceRatio)}`,
    rhythmHealthy,
  );

  const mattrTarget = thresholds.mattr[report.language] ?? (['zh', 'ja', 'ko'].includes(report.language) ? 0.68 : 0.72);
  const lexicalHealthy = metrics.mattr >= mattrTarget;
  setMetric(
    metricElements.lexical,
    formatNumber(metrics.mattr),
    `${lexicalHealthy ? copy().metricOptimal : copy().metricLow} · ${copy().metricTarget} ≥ ${formatNumber(mattrTarget)}`,
    lexicalHealthy,
  );

  const slopCount = report.violations.filter((violation) => violation.type === 'SLOP_PHRASE').length;
  const morphologyTypes = new Set(['SLOP_PHRASE', 'EXCESSIVE_NOMINALIZATION', 'PASSIVE_BLOATING', 'DEFINITIONAL_OPENING']);
  const slopHealthy = !report.violations.some((violation) => morphologyTypes.has(violation.type));
  setMetric(
    metricElements.slop,
    `${slopCount} ${copy().metricPhrases}`,
    `${copy().metricNominalization} ${formatPercent(metrics.nominalizationRatio)} · ${copy().metricPassive} ${formatPercent(metrics.passiveRatio)}`,
    slopHealthy,
  );
}

function showDiagnostic(violation) {
  const excerpt = diagnosticExcerpt(lastText, violation);
  diagnosticText.textContent = excerpt;
  diagnostic.hidden = !excerpt;
  const index = excerpt ? text.value.indexOf(excerpt) : -1;
  if (index >= 0) {
    text.focus();
    text.setSelectionRange(index, index + excerpt.length);
  }
}

function renderFindings(violations) {
  findings.replaceChildren();
  diagnostic.hidden = true;
  if (!violations.length) {
    const item = document.createElement('li');
    item.textContent = copy().noFindings;
    findings.append(item);
    return;
  }

  for (const violation of violations) {
    const item = document.createElement('li');
    const button = document.createElement('button');
    const type = document.createElement('strong');
    type.textContent = violation.type;
    const location = document.createElement('span');
    location.textContent = ` — ${violation.location}`;
    const instruction = document.createElement('span');
    instruction.textContent = `: ${violation.fixInstruction}`;
    button.type = 'button';
    button.className = 'finding-button';
    button.append(type, location, instruction);
    button.addEventListener('click', () => showDiagnostic(violation));
    item.append(button);
    findings.append(item);
  }
}

function render(report) {
  result.hidden = false;
  score.textContent = String(report.score);
  status.textContent = report.status;
  status.dataset.status = report.status.toLowerCase();
  language.textContent = languageLabel(report.language);
  renderMetrics(report);
  renderFindings(report.violations);
  copyAutoFix.hidden = !report.violations.length;
}

function updateCommand() {
  installCommand.textContent = COMMANDS[currentCommand];
  commandButtons.forEach((button) => {
    const active = button.dataset.command === currentCommand;
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-pressed', String(active));
  });
}

function updateThemeButton() {
  themeToggle.setAttribute('aria-label', copy()[currentTheme === 'dark' ? 'themeToLight' : 'themeToDark']);
  themeToggle.setAttribute('title', themeToggle.getAttribute('aria-label'));
}

function applyLanguage(nextLanguage, persist = false) {
  currentLanguage = nextLanguage;
  const strings = copy();
  document.documentElement.lang = currentLanguage;
  document.title = strings.pageTitle;
  document.querySelectorAll('[data-i18n]').forEach((element) => {
    element.textContent = strings[element.dataset.i18n];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
    element.placeholder = strings[element.dataset.i18nPlaceholder];
  });
  document.querySelectorAll('[data-i18n-aria-label]').forEach((element) => {
    element.setAttribute('aria-label', strings[element.dataset.i18nAriaLabel]);
  });
  document.querySelectorAll('[data-i18n-content]').forEach((element) => {
    element.setAttribute('content', strings[element.dataset.i18nContent]);
  });
  document.querySelectorAll('[data-i18n-title]').forEach((element) => {
    element.setAttribute('title', strings[element.dataset.i18nTitle]);
  });
  interfaceLanguage.value = currentLanguage;
  analyze.textContent = ready ? strings.analyze : strings.loading;
  renderSampleButtons();
  updateThemeButton();
  updateCommand();
  if (lastResult) render(lastResult);
  if (persist) save(LANGUAGE_KEY, currentLanguage);
}

function applyTheme(nextTheme, persist = false) {
  currentTheme = nextTheme;
  document.documentElement.classList.toggle('theme-dark', currentTheme === 'dark');
  updateThemeButton();
  if (persist) save(THEME_KEY, currentTheme);
}

function replaceSampleQuery(sample) {
  const url = new URL(window.location.href);
  url.searchParams.set('sample', sample);
  history.replaceState(null, '', `${url.pathname}${url.search}${url.hash}`);
}

function replaceTargetLangQuery(targetLang) {
  const url = new URL(window.location.href);
  url.searchParams.set('targetLang', targetLang);
  history.replaceState(null, '', `${url.pathname}${url.search}${url.hash}`);
}

function removeLanguageQuery() {
  const url = new URL(window.location.href);
  if (!url.searchParams.has('lang')) return;
  url.searchParams.delete('lang');
  history.replaceState(null, '', `${url.pathname}${url.search}${url.hash}`);
}

async function copyText(value, button) {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(value);
    } else {
      const fallback = document.createElement('textarea');
      fallback.value = value;
      fallback.setAttribute('readonly', '');
      fallback.style.position = 'fixed';
      fallback.style.opacity = '0';
      document.body.append(fallback);
      fallback.select();
      const copied = document.execCommand('copy');
      fallback.remove();
      if (!copied) throw new Error('copy failed');
    }
    copyStatus.textContent = copy().copied;
    button.dataset.copied = 'true';
    const label = button.querySelector('[data-copy-label]');
    if (label) label.textContent = copy().copied;
    window.setTimeout(() => {
      copyStatus.textContent = '';
      delete button.dataset.copied;
      if (label) label.textContent = copy()[button.dataset.copyKey];
    }, 1800);
  } catch {
    setError(copy().copyUnavailable);
  }
}

async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(String(response.status));
  return response.json();
}

async function runAnalysis() {
  setError();
  const value = text.value.trim();
  if (!value) {
    setError(copy().emptyText);
    text.focus();
    return;
  }
  analyze.disabled = true;
  try {
    lastText = text.value;
    lastResult = await analyzer.analyzeTextAsync(lastText, { language: analysisLanguage.value });
    render(lastResult);
  } catch {
    setError(copy().analysisFailed);
  } finally {
    analyze.disabled = false;
  }
}

async function loadSample(sample, updateUrl = true) {
  const selected = DEMO_SAMPLES[sample];
  if (!selected) return;
  text.value = selected.text;
  analysisLanguage.value = selected.language;
  if (updateUrl) {
    replaceSampleQuery(sample);
    replaceTargetLangQuery(selected.language);
  }
  await runAnalysis();
}

applyTheme(initialTheme());
applyLanguage(queryState.language ?? initialLanguage());

interfaceLanguage.addEventListener('change', () => {
  applyLanguage(interfaceLanguage.value, true);
  removeLanguageQuery();
});
themeToggle.addEventListener('click', () => applyTheme(currentTheme === 'dark' ? 'light' : 'dark', true));
commandButtons.forEach((button) => button.addEventListener('click', () => {
  currentCommand = button.dataset.command;
  updateCommand();
}));

copyInstall.addEventListener('click', () => copyText(COMMANDS[currentCommand], copyInstall));
copyAutoFix.addEventListener('click', () => {
  if (lastResult) copyText(buildAutoFixPrompt({ text: lastText, report: lastResult }), copyAutoFix);
});
analyze.addEventListener('click', runAnalysis);
analysisLanguage.addEventListener('change', async () => {
  replaceTargetLangQuery(analysisLanguage.value);
  if (text.value.trim()) await runAnalysis();
});

try {
  const [ruleEntries, profile] = await Promise.all([
    Promise.all(['id', 'en', 'es', 'ms', 'fr', 'de', 'pt', 'zh'].map(async (code) => [code, await loadJson(`./rules/${code}-slop.json`)])),
    loadJson('./profiles/default-human.json'),
  ]);
  defaultProfile = profile;
  analyzer = createBrowserAnalyzer({ rules: Object.fromEntries(ruleEntries), defaultProfile });
  ready = true;
  analyze.disabled = false;
  analyze.textContent = copy().analyze;
  analysisLanguage.value = queryState.targetLang ?? DEMO_SAMPLES[queryState.sample]?.language ?? 'auto';
  if (queryState.sample) {
    text.value = DEMO_SAMPLES[queryState.sample].text;
    await runAnalysis();
  }
} catch {
  setError(copy().analysisFailed);
}

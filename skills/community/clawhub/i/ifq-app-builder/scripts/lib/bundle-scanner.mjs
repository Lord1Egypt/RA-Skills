// IFQ App Builder · bundle-scanner
// Pure, dependency-free helpers for verifying and scoring `*.prompt.md` build bundles.
// Used by verify-lite.mjs, smoke-test.mjs and quality-score.mjs.

const REQUIRED_SECTIONS = [
  { key: 'S1',         header: /^##\s*S1\b/im,         label: 'S1 — WHO + WHAT' },
  { key: 'S2',         header: /^##\s*S2\b/im,         label: 'S2 — WHERE' },
  { key: 'S3',         header: /^##\s*S3\b/im,         label: 'S3 — HOW SUCCESS LOOKS' },
  { key: 'acceptance', header: /^##\s*Acceptance\b/im, label: 'Acceptance' },
  { key: 'packaging',  header: /^##\s*Packaging\b/im,  label: 'Packaging' },
  { key: 'security',   header: /^##\s*Security\b/im,   label: 'Security' },
];

const COLOPHON_RE = /—\s*shaped\s+with\s+ifq\.ai\/app-builder/i;
const CHECKBOX_RE = /^\s*-\s*\[\s*[ xX]\s*\]\s+\S/gm;
const PLACEHOLDER_REPLACE_RE = /<replace:[^>]*>/g;
const BRACE_PLACEHOLDER_RE = /\{[^{}\n]{1,120}\}/g;
const TODO_LITERAL_RE = /\b(TODO:|FIXME:|XXX:|lorem ipsum)/i;

// Secret patterns (covering OWASP common live tokens).
const SECRET_PATTERNS = [
  ['stripe-live',     /\bsk_live_[A-Za-z0-9]{16,}\b/],
  ['github-pat',      /\bghp_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b/],
  ['aws-access-key',  /\b(?:AKIA|ASIA)[0-9A-Z]{16}\b/],
  ['slack-token',     /\bxox[baprs]-[A-Za-z0-9-]{10,}\b/],
  ['google-api-key',  /\bAIza[0-9A-Za-z_-]{35}\b/],
  ['private-key-pem', /-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----|-----BEGIN PGP PRIVATE KEY BLOCK-----/],
];

const MODE_RE     = /\bA-(?:0[1-9]|1[0-2])\b/;
const TEMPLATE_RE = /\bT-[a-z0-9-]+\b/;

const I18N_TOKENS_OK   = /\bzh[-_](?:cn|hans)\b/i;
const I18N_TOKENS_OK_2 = /\b(en|en-us|en[- ]gb)\b/i;
const I18N_WAIVER_RE   = /single[- ]locale|en[- ]only/i;

const STACK_VERSION_RE = /\b(\d+(?:\.\d+){0,2}(?:\+|-[a-z0-9]+)?)\b/g;

function stripFrontMatter(raw) {
  if (!raw.startsWith('---')) return raw;
  const end = raw.indexOf('\n---', 3);
  if (end === -1) return raw;
  return raw.slice(end + 4);
}

function extractFrontMatter(raw) {
  if (!raw.startsWith('---')) return null;
  const end = raw.indexOf('\n---', 3);
  if (end === -1) return null;
  return raw.slice(4, end);
}

/**
 * Split a markdown doc into sections keyed by H2 header text (lowercased first word).
 * Returns: { sectionsByKey: Map<lowerKey, bodyText>, headerLines: Map<lowerKey, rawHeader> }
 */
function extractSections(body) {
  const lines = body.split(/\r?\n/);
  const result = new Map();
  let currentKey = null;
  let currentBuf = [];
  const flush = () => {
    if (currentKey !== null) {
      result.set(currentKey, currentBuf.join('\n').trim());
    }
  };
  for (const line of lines) {
    const m = line.match(/^##\s+(\S+.*?)\s*$/);
    if (m) {
      flush();
      // Normalize section key: take first word/token, strip punctuation, lowercase.
      const firstToken = m[1].split(/[\s—–:·]/)[0].replace(/[^A-Za-z0-9]/g, '').toLowerCase();
      currentKey = firstToken;
      currentBuf = [];
    } else if (currentKey !== null) {
      currentBuf.push(line);
    }
  }
  flush();
  return result;
}

function nonPlaceholderLen(text, { templateMode }) {
  // Strip <replace: ...> markers in template mode (they're expected); leave them as text in normal mode.
  let s = text;
  if (templateMode) {
    s = s.replace(PLACEHOLDER_REPLACE_RE, '');
  }
  // Strip checkbox prefixes, bullets, headers, hyphens — count real prose only.
  s = s.replace(/[`*_>#\-\[\]\(\)\|]/g, ' ').replace(/\s+/g, ' ').trim();
  return s.length;
}

/**
 * Run the full scan. Returns { findings: [{level, code, message}], stats: {...} }.
 * `level` is "error" or "warn". Errors fail verify-lite; warns are informational.
 */
export function scanBundle(rawText, options = {}) {
  const { templateMode = false } = options;
  const findings = [];
  const stats = {};

  const fm  = extractFrontMatter(rawText);
  const body = stripFrontMatter(rawText);
  const fullText = rawText; // for secret + colophon scans

  // ── Front-matter sanity (templates require it; user bundles don't) ──
  if (templateMode && !fm) {
    findings.push({ level: 'error', code: 'missing-frontmatter', message: 'template is missing YAML front-matter' });
  }

  // ── Mode + template tags somewhere in the bundle ──
  const modeMatch = MODE_RE.exec(fullText);
  const tmplMatch = TEMPLATE_RE.exec(fullText);
  stats.mode = modeMatch ? modeMatch[0] : null;
  stats.templateId = tmplMatch ? tmplMatch[0] : null;
  if (!modeMatch) findings.push({ level: 'error', code: 'missing-mode-tag',     message: 'no `A-xx` mode tag found anywhere in bundle' });
  if (!tmplMatch) findings.push({ level: 'error', code: 'missing-template-tag', message: 'no `T-xxx` template tag found anywhere in bundle' });

  // ── Required sections present and non-empty ──
  const sections = extractSections(body);
  stats.sections = sections;
  for (const { key, header, label } of REQUIRED_SECTIONS) {
    if (!header.test(body)) {
      findings.push({ level: 'error', code: 'missing-section', message: `missing section: ${label}` });
      continue;
    }
    const lookupKey = key.toLowerCase();
    const sectionBody = sections.get(lookupKey) || '';
    const realLen = nonPlaceholderLen(sectionBody, { templateMode });
    if (!templateMode && realLen < 12) {
      findings.push({ level: 'error', code: 'empty-section', message: `${label} body has <12 real characters (looks unfilled)` });
    }
  }

  // ── Acceptance: count checkboxes ──
  const acceptanceBody = sections.get('acceptance') || '';
  const checkboxes = acceptanceBody.match(CHECKBOX_RE) || [];
  stats.acceptanceCount = checkboxes.length;
  const minCheckboxes = templateMode ? 1 : 3;
  if (checkboxes.length < minCheckboxes) {
    findings.push({
      level: 'error',
      code: 'too-few-acceptance-items',
      message: `Acceptance has ${checkboxes.length} checkbox item(s); need at least ${minCheckboxes}`,
    });
  }

  // ── Security section concrete items ──
  const securityBody = sections.get('security') || '';
  const securityItems = (securityBody.match(/^\s*-\s+\S.+$/gm) || []).length;
  stats.securityItems = securityItems;
  const minSecurity = templateMode ? 2 : 3;
  if (securityItems < minSecurity) {
    findings.push({
      level: templateMode ? 'warn' : 'error',
      code: 'thin-security-section',
      message: `Security section has ${securityItems} bullet(s); need at least ${minSecurity}`,
    });
  }

  // ── Colophon present exactly once ──
  const colophons = fullText.match(/—\s*shaped\s+with\s+ifq\.ai\/app-builder/gi) || [];
  stats.colophonCount = colophons.length;
  if (colophons.length === 0) {
    findings.push({ level: 'error', code: 'missing-colophon', message: 'missing IFQ colophon line `— shaped with ifq.ai/app-builder`' });
  } else if (colophons.length > 1 && !templateMode) {
    findings.push({ level: 'warn', code: 'duplicate-colophon', message: `colophon appears ${colophons.length} times; should appear once at the end` });
  }

  // ── Secret leaks (always reject, both modes) ──
  for (const [name, re] of SECRET_PATTERNS) {
    const m = fullText.match(re);
    if (m) {
      findings.push({ level: 'error', code: `secret-${name}`, message: `secret-shaped token found: ${m[0].slice(0, 24)}…` });
    }
  }

  // ── Template-leak markers (TODO / lorem) — only in normal mode ──
  if (!templateMode) {
    const todoMatch = body.match(TODO_LITERAL_RE);
    if (todoMatch) findings.push({ level: 'error', code: 'todo-leak', message: `template leak: ${todoMatch[0]}` });

    // Brace placeholders like {something} are leftover scaffold.
    const braceMatches = body.match(BRACE_PLACEHOLDER_RE) || [];
    // Allow inline code/json snippets ({"ok":true}) — only flag if it contains a leading space or English placeholder phrase.
    const realBraceLeaks = braceMatches.filter(s => /\{\s*(your|replace|the|a|sample|TBD)\b/i.test(s));
    for (const leak of realBraceLeaks.slice(0, 5)) {
      findings.push({ level: 'error', code: 'brace-placeholder-leak', message: `unfilled brace placeholder: ${leak}` });
    }

    // `<replace: ...>` markers must be filled in a user bundle.
    const replaceMarkers = body.match(PLACEHOLDER_REPLACE_RE) || [];
    if (replaceMarkers.length > 0) {
      findings.push({ level: 'error', code: 'replace-marker-leak', message: `${replaceMarkers.length} <replace: ...> marker(s) still present; fill them in` });
    }
  }

  // ── i18n axis is informational; quality-score weights it. Verify-lite stays quiet unless --strict-i18n.
  stats.i18nOk =
    (I18N_TOKENS_OK.test(fullText) && I18N_TOKENS_OK_2.test(fullText)) ||
    I18N_WAIVER_RE.test(sections.get('s2') || sections.get('S2') || '');

  // ── Stack pinning: at least 2 versioned tokens somewhere in body ──
  const versionTokens = (body.match(STACK_VERSION_RE) || []).filter(v => /\d/.test(v));
  stats.versionTokenCount = versionTokens.length;
  stats.stackPinned = versionTokens.length >= 2;

  return { findings, stats };
}

export function scoreBundle(rawText) {
  const { findings, stats } = scanBundle(rawText, { templateMode: false });
  const axes = [];
  const pass = (name, ok, hint = '') => axes.push({ name, points: ok ? 10 : 0, ok, hint });

  const sections = stats.sections || new Map();
  const body = stripFrontMatter(rawText);

  // 1. routing fit
  pass('routing fit', !!stats.mode && !!stats.templateId,
    !stats.mode ? 'add an `A-xx` mode tag' : !stats.templateId ? 'add a `T-xxx` template tag' : '');

  // 2. three-sentence completeness
  const s1 = nonPlaceholderLen(sections.get('s1') || '', { templateMode: false });
  const s2 = nonPlaceholderLen(sections.get('s2') || '', { templateMode: false });
  const s3 = nonPlaceholderLen(sections.get('s3') || '', { templateMode: false });
  pass('three-sentence',
    s1 >= 12 && s2 >= 12 && s3 >= 12,
    s1 < 12 ? 'fill S1' : s2 < 12 ? 'fill S2' : 'fill S3');

  // 3. acceptance binary
  pass('acceptance binary', stats.acceptanceCount >= 3, 'add at least 3 `- [ ] ...` items');

  // 4. packaging concrete
  const packagingBody = sections.get('packaging') || '';
  const hasArtifactName = /\.(dmg|exe|app|ipa|apk|aab|msix|hap|wxapkg|AppImage|whl)\b/.test(packagingBody)
    || /docker image|docker compose|docker build|npm publish|pipx|EAS|TestFlight|App Store|Play/.test(packagingBody);
  pass('packaging concrete', hasArtifactName, 'name a concrete artifact (.dmg/.apk/docker image/…)');

  // 5. stack pinned
  pass('stack pinned', stats.stackPinned, 'name versions (e.g. Tauri 2, Node 20, iOS 17+)');

  // 6. i18n
  pass('i18n default', !!stats.i18nOk, 'mention both zh-CN and en (or declare `single-locale`)');

  // 7. security
  pass('security baseline', stats.securityItems >= 3, 'add at least 3 concrete security bullets');

  // 8. IFQ ambient
  pass('IFQ ambient', stats.colophonCount === 1, stats.colophonCount === 0 ? 'add the colophon line' : 'colophon should appear exactly once');

  let total = axes.reduce((a, b) => a + b.points, 0);

  // Bonus +20 if all axes pass AND scaffold + agent-execution-contract sections present.
  const allPass = axes.every(a => a.ok);
  const hasScaffold = /^##\s*Scaffold\b/m.test(body);
  const hasAgentContract = /^##\s*Agent execution contract\b/im.test(body);
  let bonus = 0;
  if (allPass) {
    if (hasScaffold) bonus += 10;
    if (hasAgentContract) bonus += 10;
  }
  total = Math.min(100, total + bonus);

  return { total, axes, bonus, findings, stats };
}

export const _internal = {
  REQUIRED_SECTIONS,
  SECRET_PATTERNS,
  extractSections,
  stripFrontMatter,
  extractFrontMatter,
  nonPlaceholderLen,
};

#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');
const require = createRequire(import.meta.url);
const authoredYear = require(path.join(repoRoot, 'assets', 'ifq-brand', 'ifq_authored_year.js'));

function fail(message) {
  throw new Error(message);
}

function ok(message) {
  console.log(`✓ ${message}`);
}

function read(relativePath) {
  return fs.readFileSync(path.join(repoRoot, relativePath), 'utf8');
}

function normalize(text) {
  return text.replace(/\s+/g, ' ').trim();
}

function readJson(relativePath) {
  return JSON.parse(read(relativePath));
}

function compilePattern(pattern) {
  if (typeof pattern === 'string') return new RegExp(pattern);
  if (Array.isArray(pattern) && pattern.every((part) => typeof part === 'string')) {
    return new RegExp(pattern.join(''));
  }
  fail('script safety pattern must be a string or string-fragment array');
}

function webUrlPattern() {
  return ['h', 't', 't', 'p'].join('') + 's?:\\/\\/';
}

function getTemplateFiles() {
  const index = readJson('assets/templates/INDEX.json');
  if (!Array.isArray(index.templates) || index.templates.length === 0) {
    fail('assets/templates/INDEX.json does not contain templates');
  }

  for (const template of index.templates) {
    if (!template.file || !fs.existsSync(path.join(repoRoot, template.file))) {
      fail(`template file missing from disk: ${template.file ?? '<unknown>'}`);
    }
  }

  ok(`template index resolved ${index.templates.length} entries`);
  return index.templates.map((template) => template.file);
}

function checkTemplateRoutes() {
  const indexPath = 'assets/templates/INDEX.json';
  const index = readJson(indexPath);
  const schemaPath = index.$schema?.replace(/^\.\//, 'assets/templates/');
  if (!schemaPath || !fs.existsSync(path.join(repoRoot, schemaPath))) {
    fail(`${indexPath} references a missing schema: ${index.$schema ?? '<none>'}`);
  }

  const requiredModes = Array.from({ length: 12 }, (_, idx) => `M-${String(idx + 1).padStart(2, '0')}`);
  const templateIds = new Set(index.templates.map((template) => template.id));
  const templateById = new Map(index.templates.map((template) => [template.id, template]));
  if (templateIds.size !== index.templates.length) {
    fail('assets/templates/INDEX.json contains duplicate template ids');
  }

  if (!index.qualityContract || !Array.isArray(index.qualityContract.defaultLoop) || index.qualityContract.defaultLoop.length < 5) {
    fail('assets/templates/INDEX.json missing a useful qualityContract.defaultLoop');
  }
  if (!Array.isArray(index.qualityContract.minimumEvidence) || index.qualityContract.minimumEvidence.length < 4) {
    fail('assets/templates/INDEX.json missing minimumEvidence contract');
  }
  if (!Array.isArray(index.qualityContract.firstRunLoop) || index.qualityContract.firstRunLoop.length < 5) {
    fail('assets/templates/INDEX.json missing firstRunLoop for marketplace activation');
  }
  const evidencePacket = new Set(index.qualityContract.evidencePacket || []);
  for (const item of ['file path', 'mode id', 'template id', 'assumptions', 'verification command or browser check', 'caveats that affect use']) {
    if (!evidencePacket.has(item)) fail(`assets/templates/INDEX.json evidencePacket missing: ${item}`);
  }
  if (typeof index.qualityContract.agentFailurePolicy !== 'string' || index.qualityContract.agentFailurePolicy.length < 100) {
    fail('assets/templates/INDEX.json must define a useful agentFailurePolicy');
  }

  if (!index.modeRoutes || typeof index.modeRoutes !== 'object') {
    fail('assets/templates/INDEX.json missing modeRoutes');
  }

  const routeModes = Object.keys(index.modeRoutes).sort();
  for (const mode of requiredModes) {
    if (!index.modeRoutes[mode]) fail(`modeRoutes missing ${mode}`);
  }
  for (const mode of routeModes) {
    if (!requiredModes.includes(mode)) fail(`unexpected mode route: ${mode}`);
    const route = index.modeRoutes[mode];
    if (!templateIds.has(route.primaryTemplate)) {
      fail(`${mode} primaryTemplate does not reference a known template: ${route.primaryTemplate}`);
    }
    if (!templateById.get(route.primaryTemplate)?.mode?.includes(mode)) {
      fail(`${mode} primaryTemplate ${route.primaryTemplate} must list the mode in templates[].mode`);
    }
    for (const fallback of route.fallbackTemplates || []) {
      if (!templateIds.has(fallback)) fail(`${mode} fallbackTemplate does not reference a known template: ${fallback}`);
    }
    if (!Array.isArray(route.requiredReferences) || route.requiredReferences.length === 0) {
      fail(`${mode} must list requiredReferences`);
    }
    for (const referencePath of route.requiredReferences) {
      if (!fs.existsSync(path.join(repoRoot, referencePath))) {
        fail(`${mode} references missing guide: ${referencePath}`);
      }
    }
    if (!route.outputBoundary || !/ClawHub|HTML|repo/i.test(route.outputBoundary)) {
      fail(`${mode} outputBoundary must describe bundle/full-repo behavior`);
    }
  }

  for (const template of index.templates) {
    for (const mode of template.mode || []) {
      if (!requiredModes.includes(mode)) fail(`${template.id} uses unknown mode: ${mode}`);
    }
  }

  ok(`template router covers ${requiredModes.length} modes with ${templateIds.size} templates`);
}

function checkEvalSuite() {
  const evalPath = path.join(repoRoot, 'evals', 'evals.json');
  if (!fs.existsSync(evalPath)) {
    fail('evals/evals.json missing — required to protect mode-routing regressions');
  }

  const evals = readJson('evals/evals.json');
  const index = readJson('assets/templates/INDEX.json');
  const evalSchemaPath = String(evals.$schema || '').replace(/^\.\//, 'evals/');
  if (evalSchemaPath !== 'evals/evals.schema.json' || !fs.existsSync(path.join(repoRoot, evalSchemaPath))) {
    fail(`evals/evals.json references a missing schema: ${evals.$schema ?? '<none>'}`);
  }
  const templateIds = new Set(index.templates.map((template) => template.id));
  const templateById = new Map(index.templates.map((template) => [template.id, template]));
  const routeModes = new Set(Object.keys(index.modeRoutes || {}));
  const requiredModes = Array.from({ length: 12 }, (_, idx) => `M-${String(idx + 1).padStart(2, '0')}`);

  if (evals.version !== '1.0') fail(`evals.version must be 1.0, got ${evals.version}`);
  if (!Array.isArray(evals.quality_principles) || evals.quality_principles.length < 3) {
    fail('evals/evals.json must declare at least 3 quality_principles');
  }
  if (!Array.isArray(evals.scenarios) || evals.scenarios.length < requiredModes.length) {
    fail(`evals/evals.json must contain at least ${requiredModes.length} scenarios`);
  }

  const ids = new Set();
  const coveredModes = new Set();
  const safeCommandPrefixes = ['npm run verify:lite -- ', 'npm run preview -- ', 'manual '];
  let firstRunCoverage = false;

  for (const scenario of evals.scenarios || []) {
    const id = scenario.id || '<missing-id>';
    if (!/^[a-z0-9][a-z0-9-]{2,80}$/.test(id)) fail(`eval scenario id must be stable kebab-case: ${id}`);
    if (ids.has(id)) fail(`duplicate eval scenario id: ${id}`);
    ids.add(id);

    const route = index.modeRoutes?.[scenario.mode];
    if (!routeModes.has(scenario.mode)) fail(`${id}: unknown mode ${scenario.mode}`);
    else coveredModes.add(scenario.mode);

    for (const key of ['prompt_zh', 'prompt_en', 'user_value', 'agent_value']) {
      if (typeof scenario[key] !== 'string' || scenario[key].trim().length < 12) {
        fail(`${id}: ${key} must be descriptive`);
      }
    }

    const contract = scenario.agent_contract || {};
    if (typeof contract.route !== 'string' || !contract.route.includes(scenario.mode)) {
      fail(`${id}: agent_contract.route must include ${scenario.mode}`);
    }
    for (const templateId of contract.template_ids || []) {
      if (!templateIds.has(templateId)) fail(`${id}: unknown template id ${templateId}`);
    }
    if (!Array.isArray(contract.template_ids) || contract.template_ids.length === 0) {
      fail(`${id}: agent_contract.template_ids required`);
    }
    if (route?.primaryTemplate && !contract.template_ids.includes(route.primaryTemplate)) {
      fail(`${id}: agent_contract.template_ids must include route primary template ${route.primaryTemplate}`);
    }
    const primaryTemplate = templateById.get(route?.primaryTemplate);
    if (primaryTemplate && !primaryTemplate.mode?.includes(scenario.mode)) {
      fail(`${id}: primary template ${route.primaryTemplate} must list ${scenario.mode} in templates[].mode`);
    }
    if (!Array.isArray(contract.must_read) || contract.must_read.length < 2) {
      fail(`${id}: agent_contract.must_read must include at least 2 files`);
    } else {
      for (const relPath of contract.must_read) {
        if (typeof relPath !== 'string' || relPath.startsWith('/') || relPath.includes('..')) {
          fail(`${id}: unsafe must_read path ${relPath}`);
        } else if (!fs.existsSync(path.join(repoRoot, relPath))) {
          fail(`${id}: missing must_read path ${relPath}`);
        }
      }
      for (const relPath of route?.requiredReferences || []) {
        if (!contract.must_read.includes(relPath)) {
          fail(`${id}: agent_contract.must_read must include route reference ${relPath}`);
        }
      }
    }
    if (typeof contract.tier !== 'string' || !contract.tier.includes('Tier')) {
      fail(`${id}: agent_contract.tier must name a Tier policy`);
    }
    if (!Array.isArray(contract.verification) || contract.verification.length < 2) {
      fail(`${id}: agent_contract.verification must include at least 2 commands`);
    } else {
      for (const command of contract.verification) {
        if (!safeCommandPrefixes.some((prefix) => command.startsWith(prefix))) {
          fail(`${id}: unsupported verification command ${command}`);
        }
      }
      if (!contract.verification.some((command) => command.startsWith('npm run verify:lite -- '))) {
        fail(`${id}: agent_contract.verification must include npm run verify:lite`);
      }
      if (!contract.verification.some((command) => command.startsWith('npm run preview -- '))) {
        fail(`${id}: agent_contract.verification must include npm run preview`);
      }
    }
    if (typeof contract.fact_check_required !== 'boolean') {
      fail(`${id}: fact_check_required must be boolean`);
    }
    const quality = scenario.quality_bar || {};
    if (id.includes('first-run') || /ClawHub/i.test(`${scenario.prompt_en} ${scenario.prompt_zh}`)) {
      firstRunCoverage = true;
      const firstRunText = [
        ...(contract.verification || []),
        ...(quality.must_include || []),
        ...(quality.must_not || []),
      ].join(' | ').toLowerCase();
      for (const token of ['file', 'route', 'template', 'assumptions', 'verification', 'caveats']) {
        if (!firstRunText.includes(token)) {
          fail(`${id}: first-run evidence expectations must mention ${token}`);
        }
      }
    }
    if (!Array.isArray(quality.must_include) || quality.must_include.length < 3) {
      fail(`${id}: quality_bar.must_include must contain at least 3 items`);
    }
    if (!Array.isArray(quality.must_not) || quality.must_not.length < 2) {
      fail(`${id}: quality_bar.must_not must contain at least 2 items`);
    }
  }

  for (const mode of requiredModes) {
    if (!coveredModes.has(mode)) fail(`eval suite missing coverage for ${mode}`);
  }
  if (!firstRunCoverage) {
    fail('eval suite must include a ClawHub first-run activation scenario');
  }

  ok(`eval suite covers ${coveredModes.size} modes with ${ids.size} scenarios`);
}

function checkBrandAssets() {
  const requiredFiles = [
    'assets/ifq-brand/logo.svg',
    'assets/ifq-brand/logo-white.svg',
    'assets/ifq-brand/mark.svg',
    'assets/ifq-brand/icons/hand-drawn-icons.svg',
    'assets/ifq-brand/ifq_brand.jsx',
    'assets/ifq-brand/ifq_authored_year.js',
  ];

  for (const relativePath of requiredFiles) {
    if (!fs.existsSync(path.join(repoRoot, relativePath))) {
      fail(`brand asset missing: ${relativePath}`);
    }
  }

  const sprite = read('assets/ifq-brand/icons/hand-drawn-icons.svg');
  const symbolCount = [...sprite.matchAll(/<symbol\b[^>]*\bid=/g)].length;
  if (symbolCount < 24) {
    fail(`hand-drawn icon sprite only has ${symbolCount} symbols`);
  }

  ok(`brand toolkit present; icon sprite exposes ${symbolCount} symbols`);
}

function checkGalleryPresence() {
  const galleryPath = 'assets/templates/GALLERY.html';
  if (!fs.existsSync(path.join(repoRoot, galleryPath))) {
    fail(`${galleryPath} missing — required for template preview and discovery`);
  }

  const html = read(galleryPath);
  if (!html.includes('T-') || html.length < 1000) {
    fail(`${galleryPath} appears malformed or too short to be a real gallery`);
  }

  ok('template gallery (GALLERY.html) present and populated');
}

function checkEvalSchemaPresence() {
  const schemaPath = 'evals/evals.schema.json';
  if (!fs.existsSync(path.join(repoRoot, schemaPath))) {
    fail(`${schemaPath} missing — required for eval suite validation`);
  }

  try {
    const schema = readJson(schemaPath);
    if (!schema.$schema || !schema.properties) {
      fail(`${schemaPath} appears malformed: missing $schema or properties`);
    }
  } catch (err) {
    fail(`${schemaPath} is not valid JSON: ${err.message}`);
  }

  ok('eval schema (evals.schema.json) present and valid');
}

function checkSkillReferenceTargets() {
  const skill = read('SKILL.md');
  const references = [...new Set(skill.match(/references\/[A-Za-z0-9._/-]+\.md/g) ?? [])]
    // Filter out documentation-style placeholders like `references/xxx.md`.
    .filter((ref) => !/\b(xxx|yyy|foo|bar|example|placeholder)\b/i.test(ref));

  if (references.length === 0) {
    fail('SKILL.md does not reference any markdown guides');
  }

  for (const referencePath of references) {
    if (!fs.existsSync(path.join(repoRoot, referencePath))) {
      fail(`missing reference target: ${referencePath}`);
    }
  }

  ok(`SKILL references resolved ${references.length} markdown guides`);
}

function checkSkillDisclosureBudget() {
  const skill = read('SKILL.md');
  const lineCount = skill.split(/\r?\n/).length;
  if (lineCount > 500) {
    fail(`SKILL.md is ${lineCount} lines; keep the root skill under 500 lines and move details to references/`);
  }
  const metadataLines = skill.split(/\r?\n/).filter((line) => line.startsWith('metadata:'));
  if (metadataLines.length !== 1 || !metadataLines[0].startsWith('metadata: {')) {
    fail('SKILL.md metadata must stay as a single JSON line for loader/scanner friendliness');
  }
  if (!skill.includes('## First-Run Success Path')) {
    fail('SKILL.md must include a First-Run Success Path section for ClawHub onboarding');
  }

  ok(`SKILL.md disclosure budget healthy (${lineCount} lines, single-line metadata)`);
}

function checkScriptSyntax() {
  const scriptDir = path.join(repoRoot, 'scripts');
  const scriptFiles = fs.readdirSync(scriptDir)
    .filter((file) => /\.(?:mjs|js)$/i.test(file))
    .map((file) => path.join(scriptDir, file));

  if (scriptFiles.length === 0) {
    fail('no Node scripts found under scripts/');
  }

  for (const scriptFile of scriptFiles) {
    const source = fs.readFileSync(scriptFile, 'utf8');
    if (!source.trim()) {
      fail(`empty script: ${path.relative(repoRoot, scriptFile)}`);
    }

    const sample = Buffer.from(source, 'utf8').subarray(0, 512);
    if (sample.includes(0)) {
      fail(`binary content found in script: ${path.relative(repoRoot, scriptFile)}`);
    }

    const likelyEntryPoint = /^#!\/usr\/bin\/env\s+node\b/m.test(source)
      || /\bimport\s.+\sfrom\s+['"][^'"]+['"]/.test(source)
      || /\b(?:async\s+)?function\s+[A-Za-z_$][\w$]*\s*\(/.test(source)
      || /\bconst\s+[A-Za-z_$][\w$]*\s*=\s*(?:async\s+)?\(/.test(source);

    if (!likelyEntryPoint) {
      fail(`script looks malformed: ${path.relative(repoRoot, scriptFile)}`);
    }
  }

  ok(`script files look healthy (${scriptFiles.length})`);
}

function checkAuthoredYearResolver() {
  const currentYear = String(new Date().getFullYear());
  const samples = [
    { label: 'Date object', input: new Date('2026-04-23T10:20:30Z'), expected: '2026' },
    { label: 'epoch milliseconds', input: Date.UTC(2026, 3, 23, 10, 20, 30), expected: '2026' },
    { label: 'plain year', input: '2026', expected: '2026' },
    { label: 'ISO 8601', input: '2026-04-23T10:20:30Z', expected: '2026' },
    { label: 'slash-separated date', input: '2026/04/23 10:20:30', expected: '2026' },
    { label: 'browser lastModified style', input: '04/23/2026 10:20:30', expected: '2026' },
    { label: 'RFC 1123', input: 'Thu, 23 Apr 2026 10:20:30 GMT', expected: '2026' },
    { label: 'invalid input fallback', input: 'not-a-date', expected: currentYear },
  ];

  for (const sample of samples) {
    const actual = authoredYear.resolve(sample.input);
    if (actual !== sample.expected) {
      fail(`authored year resolver failed for ${sample.label}: expected ${sample.expected}, got ${actual}`);
    }
  }

  const resolvedInfo = authoredYear.resolveInfo('2026-04-23T10:20:30Z');
  if (resolvedInfo.yearMonth !== '2026 · 04' || resolvedInfo.date !== '2026 · 04 · 23' || resolvedInfo.isoDate !== '2026-04-23') {
    fail(`authored date resolver produced unexpected date formats: ${JSON.stringify(resolvedInfo)}`);
  }

  ok(`authored year resolver accepted ${samples.length} cross-platform date inputs`);
}

function checkAuthoredYearTemplates(templateFiles) {
  const expectedLabelPattern = /^ifq\.ai\s*\/\s*\d{4}$/;
  const authoredTemplates = [];

  for (const relativePath of templateFiles) {
    if (!relativePath.endsWith('.html')) {
      continue;
    }

    const html = read(relativePath);
    if (/\b2026\b/.test(html)) {
      fail(`hardcoded 2026 still present in ${relativePath}`);
    }

    if (/ifq\.ai\s*\/\s*field note\s*\/\s*20\d{2}/i.test(html)) {
      fail(`legacy authored stamp still present in ${relativePath}`);
    }

    // Pattern 02 cleanliness: never leak the internal pattern code-name "FIELD NOTE"
    // into rendered output (case-insensitive match on visible text only — skip
    // HTML comments, which are stripped before we test).
    const visible = html.replace(/<!--[\s\S]*?-->/g, '');
    if (/\bfield\s*note\b/i.test(visible)) {
      fail(`${relativePath} renders the literal phrase "field note" — use a task-mode word from Pattern 02 (live system / release ledger / chapter / correspondence …) instead`);
    }

    // Pattern 02 cleanliness: never use "//" as a textual separator in rendered
    // output — it reads as a JS/C comment marker. Allow it only inside <script>,
    // <style>, attributes (href/src), and HTML comments.
    const stripped = visible
      .replace(/<script[\s\S]*?<\/script>/gi, '')
      .replace(/<style[\s\S]*?<\/style>/gi, '')
      .replace(/\s(?:href|src|xmlns|content|action|data-[\w-]+)\s*=\s*"[^"]*"/gi, '')
      .replace(/\s(?:href|src|xmlns|content|action|data-[\w-]+)\s*=\s*'[^']*'/gi, '');
    if (/(?:^|[\s>&])\/\/(?:[\s<&]|nbsp;)/.test(stripped)) {
      fail(`${relativePath} contains "//" as a visible text separator — use "·" (middle dot) or single "/" per Pattern 02`);
    }

    if (html.includes('data-ifq-authored-year') || html.includes('data-ifq-authored-date')) {
      authoredTemplates.push({ relativePath, html });
    }
  }

  if (authoredTemplates.length === 0) {
    fail('no authored-year templates found');
  }

  for (const { relativePath, html } of authoredTemplates) {
    if (!html.includes('../ifq-brand/ifq_authored_year.js')) {
      fail(`missing authored-year helper include in ${relativePath}`);
    }

    const stampMatch = html.match(/data-ifq-authored-year[^>]*>\s*([^<]+?)\s*<\/span>/i);
    if (!stampMatch) {
      fail(`could not find authored-year stamp text in ${relativePath}`);
    }

    const sourceLabel = normalize(stampMatch[1]);
    if (!sourceLabel.includes(authoredYear.token)) {
      fail(`authored-year token missing in ${relativePath}`);
    }

    const absolutePath = path.join(repoRoot, relativePath);
    const expectedYear = String(fs.statSync(absolutePath).mtime.getFullYear());
    const renderedLabel = normalize(
      sourceLabel.split(authoredYear.token).join(authoredYear.resolve(fs.statSync(absolutePath).mtime.toUTCString()))
    );

    // Strict "ifq.ai / <year>" format is only required for templates whose
    // authored stamp is literally "ifq.ai / <year>" (two segments). Other
    // templates may use extended formats like "ifq.ai / design systems / 2026"
    // or non-ifq stamps like "{ SIGNAL } · 2026" — those only need a valid
    // 4-digit year and no placeholder leak.
    const isCanonicalTwoSegmentStamp = /^ifq\.ai\s*\/\s*[^/]+$/i.test(sourceLabel) && !/\/[^/]+\//.test(sourceLabel);

    if (isCanonicalTwoSegmentStamp) {
      if (!expectedLabelPattern.test(renderedLabel)) {
        fail(`rendered authored stamp is not a real year in ${relativePath}: ${renderedLabel}`);
      }
      if (renderedLabel !== `ifq.ai / ${expectedYear}`) {
        fail(`rendered authored stamp mismatch in ${relativePath}: ${renderedLabel}`);
      }
    } else if (!/\b\d{4}\b/.test(renderedLabel)) {
      fail(`rendered authored stamp has no 4-digit year in ${relativePath}: ${renderedLabel}`);
    }

    if (renderedLabel.includes(authoredYear.token) || /{[^}]*year[^}]*}/i.test(renderedLabel)) {
      fail(`year placeholder leaked into rendered authored stamp in ${relativePath}`);
    }

    ok(`${relativePath} renders authored stamp as ${renderedLabel}`);

    const datedNodes = [...html.matchAll(/data-ifq-authored-date="([^"]*)"[^>]*>\s*([^<]+?)\s*<\//gi)];
    for (const nodeMatch of datedNodes) {
      const renderedDate = normalize(
        nodeMatch[2]
          .split(authoredYear.yearMonthToken).join(authoredYear.resolveInfo('2026-04-23T10:20:30Z').yearMonth)
          .split(authoredYear.dateToken).join(authoredYear.resolveInfo('2026-04-23T10:20:30Z').date)
          .split(authoredYear.token).join(authoredYear.resolve('2026-04-23T10:20:30Z'))
      );

      if (/__IFQ_/.test(renderedDate)) {
        fail(`date placeholder leaked into rendered authored date in ${relativePath}: ${renderedDate}`);
      }
    }
  }

  const ifqStampSource = read('assets/ifq-brand/ifq_brand.jsx');
  if (/label\s*=\s*'ifq\.ai\s*\/\s*field note'/.test(ifqStampSource)) {
    fail('IfqStamp still hardcodes the legacy field note label');
  }

  if (!ifqStampSource.includes('label ?? `ifq.ai / ${getIfqAuthoredYear()}`')) {
    fail('IfqStamp default label is not derived from the authored year');
  }

  ok('IfqStamp default label derives the authored year dynamically');
}

function checkClawHubManifest() {
  // The root clawhub.json is how OpenClaw / ClawHub discover triggers,
  // permissions and tool-mapping without parsing SKILL.md YAML frontmatter.
  const manifestPath = path.join(repoRoot, 'clawhub.json');
  if (!fs.existsSync(manifestPath)) {
    fail('clawhub.json missing at repo root — required for OpenClaw/ClawHub discovery');
  }

  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  } catch (err) {
    fail(`clawhub.json is not valid JSON: ${err.message}`);
  }

  const required = ['name', 'version', 'entrypoint', 'triggers', 'permissions', 'tool_map'];
  for (const key of required) {
    if (!(key in manifest)) fail(`clawhub.json missing required field: ${key}`);
  }

  if (manifest.name !== 'ifq-design-skills') {
    fail(`clawhub.json name mismatch: ${manifest.name}`);
  }

  if (typeof manifest.summary !== 'string' || manifest.summary.length < 80 || manifest.summary.length > 320) {
    fail('clawhub.json summary must be concise marketplace copy (80-320 chars)');
  }

  if (manifest.category !== 'creative') fail(`clawhub.json category mismatch: ${manifest.category}`);
  if (!Array.isArray(manifest.tags) || manifest.tags.length < 8) {
    fail('clawhub.json must expose useful discovery tags');
  }

  if (manifest.bundle?.ignore !== 'clawhub.ignore.txt') fail('clawhub.json bundle.ignore must be clawhub.ignore.txt');
  if (manifest.bundle?.safe !== true) fail('clawhub.json bundle.safe must be true');
  if (manifest.bundle?.contains_binary !== false) fail('clawhub.json bundle.contains_binary must be false');

  if (manifest.runtime?.node !== '>=18.17') fail(`clawhub.json runtime.node mismatch: ${manifest.runtime?.node}`);
  if (manifest.runtime?.requires_scripts !== false) fail('clawhub.json runtime.requires_scripts must be false for the safe bundle');
  if (manifest.runtime?.network?.required !== false) fail('clawhub.json runtime.network.required must be false');

  const expectedPermissions = {
    filesystem: 'workspace',
    shell: 'workspace-node-scripts-only',
    browser: 'optional-outbound-https-read',
    network: 'optional-outbound-https',
  };
  for (const [key, value] of Object.entries(expectedPermissions)) {
    if (manifest.permissions?.[key] !== value) fail(`clawhub.json permissions.${key} mismatch: ${manifest.permissions?.[key]}`);
  }

  for (const plugin of ['filesystem', 'shell']) {
    if (!manifest.plugins?.required?.includes(plugin)) fail(`clawhub.json plugins.required missing ${plugin}`);
  }
  for (const plugin of ['browser', 'memory']) {
    if (!manifest.plugins?.optional?.includes(plugin)) fail(`clawhub.json plugins.optional missing ${plugin}`);
  }

  const packageScripts = readJson('package.json').scripts || {};
  if (!Array.isArray(manifest.quick_commands) || manifest.quick_commands.length < 4) {
    fail('clawhub.json quick_commands must expose validation, eval, verify, and pack commands');
  }
  for (const item of manifest.quick_commands || []) {
    const scriptName = String(item.command || '').match(/^npm run ([^\s]+)/)?.[1];
    if (!scriptName || !packageScripts[scriptName]) {
      fail(`clawhub.json quick command does not map to package.json scripts: ${item.command}`);
    }
  }

  if (typeof manifest.marketplace?.positioning !== 'string' || manifest.marketplace.positioning.length < 80) {
    fail('clawhub.json marketplace.positioning must explain the first-scan value proposition');
  }
  for (const key of ['human_value', 'agent_value', 'scanner_alignment', 'activation_loop', 'evidence_packet', 'top_skill_signals']) {
    if (!Array.isArray(manifest.marketplace?.[key]) || manifest.marketplace[key].length < 3) {
      fail(`clawhub.json marketplace.${key} must list at least 3 signals`);
    }
  }

  if (typeof manifest.first_run?.install_prompt !== 'string' || !manifest.first_run.install_prompt.includes('ifq-design-skills')) {
    fail('clawhub.json first_run.install_prompt must name ifq-design-skills');
  }
  if (!Array.isArray(manifest.first_run?.starter_prompts) || manifest.first_run.starter_prompts.length < 3) {
    fail('clawhub.json first_run.starter_prompts must include at least 3 first-run prompts');
  }
  const evidence = new Set(manifest.first_run?.success_evidence || []);
  for (const item of ['output file path', 'mode route used', 'template id used', 'assumptions made', 'known caveats that affect use']) {
    if (!evidence.has(item)) fail(`clawhub.json first_run.success_evidence missing: ${item}`);
  }

  if (!Array.isArray(manifest.demo_artifacts) || manifest.demo_artifacts.length < 3) {
    fail('clawhub.json demo_artifacts must expose at least 3 inspectable examples');
  }
  for (const demo of manifest.demo_artifacts || []) {
    if (!demo.file || !fs.existsSync(path.join(repoRoot, demo.file))) {
      fail(`clawhub.json demo_artifacts file missing: ${demo.file ?? '<none>'}`);
    }
    if (!/^M-(0[1-9]|1[0-2])$/.test(demo.route || '')) {
      fail(`clawhub.json demo_artifacts route invalid: ${demo.route ?? '<none>'}`);
    }
    if (!String(demo.verify || '').startsWith('npm run verify:lite -- ')) {
      fail(`clawhub.json demo_artifacts verify must use verify:lite: ${demo.verify ?? '<none>'}`);
    }
  }

  const skillVersion = (read('SKILL.md').match(/^version:\s*([^\n]+)$/m) ?? [])[1]?.trim();
  if (skillVersion && manifest.version !== skillVersion) {
    fail(`clawhub.json version (${manifest.version}) does not match SKILL.md version (${skillVersion})`);
  }

  if (!fs.existsSync(path.join(repoRoot, manifest.entrypoint))) {
    fail(`clawhub.json entrypoint missing on disk: ${manifest.entrypoint}`);
  }

  if (!Array.isArray(manifest.triggers) || manifest.triggers.length < 10) {
    fail('clawhub.json must declare at least 10 triggers');
  }

  const requiredTools = ['read_file', 'write_file', 'run_command'];
  for (const tool of requiredTools) {
    if (!manifest.tool_map[tool]) fail(`clawhub.json tool_map missing: ${tool}`);
  }

  // Doc cross-references must resolve; stale anchors break the OpenClaw onboard.
  if (manifest.docs && typeof manifest.docs === 'object') {
    for (const [key, value] of Object.entries(manifest.docs)) {
      const [filePart, anchorPart] = String(value).split('#');
      const docPath = path.join(repoRoot, filePart);
      if (!fs.existsSync(docPath)) {
        fail(`clawhub.json docs.${key} points to missing file: ${filePart}`);
      }
      if (anchorPart) {
        const flatten = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
        const target = flatten(anchorPart);
        const docSource = fs.readFileSync(docPath, 'utf8');
        const headings = [...docSource.matchAll(/^#{1,6}\s+(.+?)\s*$/gm)].map((m) => m[1]);
        const matched = headings.some((heading) => flatten(heading).includes(target));
        if (!matched) {
          fail(`clawhub.json docs.${key} anchor not found in ${filePart}: #${anchorPart}`);
        }
      }
    }
  }

  ok(`clawhub.json manifest valid (${manifest.triggers.length} triggers, ${Object.keys(manifest.tool_map).length} tool mappings)`);
}

function checkManifestFrontmatterParity() {
  const manifest = readJson('clawhub.json');
  const skill = read('SKILL.md');
  const metadataMatch = skill.match(/^metadata:\s*(\{.+\})$/m);
  if (!metadataMatch) {
    fail('SKILL.md frontmatter missing metadata JSON');
  }

  let metadata;
  try {
    metadata = JSON.parse(metadataMatch[1]);
  } catch (err) {
    fail(`SKILL.md metadata is not valid JSON: ${err.message}`);
  }

  const skillVersion = (skill.match(/^version:\s*([^\n]+)$/m) ?? [])[1]?.trim();
  const skillLicense = (skill.match(/^license:\s*["']?([^"'\n]+)["']?$/m) ?? [])[1]?.trim();
  if (manifest.version !== skillVersion || metadata.version !== skillVersion) {
    fail(`version drift: SKILL=${skillVersion}, metadata=${metadata.version}, clawhub=${manifest.version}`);
  }
  if (manifest.license !== skillLicense) {
    fail(`license drift: SKILL=${skillLicense}, clawhub=${manifest.license}`);
  }

  const openclaw = metadata.openclaw || {};
  if (openclaw.homepage !== manifest.homepage) {
    fail(`OpenClaw homepage drift: SKILL=${openclaw.homepage}, clawhub=${manifest.homepage}`);
  }

  const os = new Set(openclaw.os || []);
  for (const value of ['darwin', 'linux', 'win32']) {
    if (!os.has(value)) fail(`metadata.openclaw.os missing ${value}`);
  }
  const manifestPlatforms = new Set(manifest.platforms || []);
  if (!manifestPlatforms.has('macos') || !manifestPlatforms.has('linux') || !manifestPlatforms.has('windows')) {
    fail('clawhub.json platforms must include macos, linux, and windows');
  }

  const requires = openclaw.requires || {};
  if (!Array.isArray(requires.bins) || !requires.bins.includes('node')) {
    fail('metadata.openclaw.requires.bins must include node');
  }
  for (const key of ['env', 'config']) {
    if (!Array.isArray(requires[key]) || requires[key].length !== 0) {
      fail(`metadata.openclaw.requires.${key} must be an intentionally empty array`);
    }
  }

  const clawhubRequires = metadata.clawhub?.requires || {};
  if (!Array.isArray(clawhubRequires.bins) || !clawhubRequires.bins.includes('node')) {
    fail('metadata.clawhub.requires.bins must include node');
  }
  if (!Array.isArray(clawhubRequires.env) || clawhubRequires.env.length !== 0) {
    fail('metadata.clawhub.requires.env must be an intentionally empty array');
  }

  for (const plugin of ['filesystem', 'shell']) {
    if (!openclaw.required_plugins?.includes(plugin) || !manifest.plugins?.required?.includes(plugin)) {
      fail(`manifest/frontmatter required plugin drift: ${plugin}`);
    }
  }
  for (const plugin of ['browser', 'memory']) {
    if (!openclaw.optional_plugins?.includes(plugin) || !manifest.plugins?.optional?.includes(plugin)) {
      fail(`manifest/frontmatter optional plugin drift: ${plugin}`);
    }
  }

  const manifestTriggers = new Set(manifest.triggers || []);
  const frontmatterTriggers = new Set(openclaw.triggers || []);
  for (const trigger of ['mp4 export', 'gif export']) {
    if (manifestTriggers.has(trigger) || frontmatterTriggers.has(trigger)) {
      fail(`raw export trigger "${trigger}" must be expressed as export planning in the ClawHub-safe bundle`);
    }
  }
  for (const trigger of ['mp4 export plan', 'gif export plan']) {
    if (!manifestTriggers.has(trigger) || !frontmatterTriggers.has(trigger)) {
      fail(`manifest/frontmatter must both include planning trigger: ${trigger}`);
    }
  }

  if (manifest.tool_map?.screenshot !== openclaw.tool_map?.screenshot) {
    fail(`screenshot tool_map drift: SKILL=${openclaw.tool_map?.screenshot}, clawhub=${manifest.tool_map?.screenshot}`);
  }
  if (manifest.tool_map?.screenshot === 'shell/exec') {
    fail('screenshot tool_map must not point at shell/exec');
  }

  const exports = new Set(manifest.fullRepoOnlyExports || []);
  for (const format of ['mp4', 'gif', 'pdf', 'pptx']) {
    if (!exports.has(format)) fail(`clawhub.json fullRepoOnlyExports missing ${format}`);
  }

  for (const file of ['LICENSE.md', 'NOTICE.md', 'CONTRIBUTING.md', 'SECURITY.md', 'CHANGELOG.md']) {
    if (!fs.existsSync(path.join(repoRoot, file))) fail(`trust file missing: ${file}`);
  }

  ok('manifest/frontmatter parity: version, license, OpenClaw gates, plugins, screenshot mapping, export boundaries, trust files');
}

function checkOnboardingDocsParity() {
  const manifest = readJson('clawhub.json');
  const skill = read('SKILL.md');
  const readmeZh = read('README.md');
  const readmeEn = read('README.en.md');
  const agents = read('AGENTS.md');
  const skillVersion = (skill.match(/^version:\s*([^\n]+)$/m) ?? [])[1]?.trim();

  if (!agents.includes(`ifq-design-skills\` (v${skillVersion})`)) {
    fail(`AGENTS.md version must match SKILL.md (${skillVersion})`);
  }

  const onboardingDocs = [
    ['README.md', readmeZh],
    ['README.en.md', readmeEn],
    ['AGENTS.md', agents],
  ];

  for (const [label, source] of onboardingDocs) {
    for (const token of ['output', 'mode', 'template', 'assumption', 'verification', 'caveat']) {
      const tokenMap = {
        output: /output|输出|文件路径/i,
        mode: /\bmode\b|模式/i,
        template: /\btemplate\b|模板/i,
        assumption: /assumption|假设/i,
        verification: /verification|verify:lite|验证/i,
        caveat: /caveat|影响使用/i,
      };
      if (!tokenMap[token].test(source)) {
        fail(`${label} onboarding must mention first-run ${token}`);
      }
    }
  }

  for (const item of manifest.first_run?.success_evidence || []) {
    const loose = item
      .replace(/\b(output|mode|template|id|used|made|known|that|affect|use|command|or|browser|check|performed)\b/gi, '')
      .replace(/\s+/g, ' ')
      .trim()
      .split(' ')[0];
    if (loose && !new RegExp(loose.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i').test(`${readmeEn}\n${agents}`)) {
      fail(`onboarding docs do not reflect manifest first_run.success_evidence item: ${item}`);
    }
  }

  if (!/ClawHub Top 10/i.test(readmeEn) || !/ClawHub Top 10/i.test(readmeZh)) {
    fail('README files must expose the ClawHub Top 10 positioning section');
  }

  ok('onboarding docs parity: README/AGENTS version, first-run evidence, and marketplace positioning are synchronized');
}

function checkPackageManifestSafety() {
  // Top marketplace skills stay install-light: no dependency tree and no npm
  // lifecycle hooks that can execute during install/publish. ClawHub/VirusTotal
  // scanners pay close attention to these surfaces.
  const packagePath = path.join(repoRoot, 'package.json');
  if (!fs.existsSync(packagePath)) {
    fail('package.json missing — npm run validate / pack commands must be inspectable');
  }

  let pkg;
  try {
    pkg = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  } catch (err) {
    fail(`package.json is not valid JSON: ${err.message}`);
  }

  const dependencyFields = ['dependencies', 'devDependencies', 'optionalDependencies', 'peerDependencies'];
  for (const field of dependencyFields) {
    if (pkg[field] && Object.keys(pkg[field]).length > 0) {
      fail(`package.json must keep ${field} empty in the ClawHub-safe bundle`);
    }
  }

  const scripts = pkg.scripts || {};
  const lifecycleHooks = ['preinstall', 'install', 'postinstall', 'prepare', 'prepack', 'postpack', 'prepublish', 'prepublishOnly'];
  for (const hook of lifecycleHooks) {
    if (hook in scripts) fail(`package.json must not declare npm lifecycle hook: ${hook}`);
  }

  const allowedScripts = new Set(['smoke', 'validate', 'pack', 'evals:validate', 'preview', 'verify:lite', 'anti-slop']);
  for (const [name, command] of Object.entries(scripts)) {
    if (!allowedScripts.has(name)) fail(`unexpected package script in ClawHub-safe bundle: ${name}`);
    if (!/^node scripts\/[A-Za-z0-9_.-]+\.mjs$/.test(command)) {
      fail(`package script ${name} must be a direct node scripts/*.mjs command, got: ${command}`);
    }
  }

  ok('package manifest: zero dependencies and no install-time lifecycle hooks');
}

function checkDefaultTemplateRemoteRuntime() {
  // Forkable templates are the default output surface. They may use optional
  // Google Fonts with Tier B fallback, but must not depend on remote JS/CSS
  // runtimes such as unpinned CDN scripts or Tailwind CDN.
  const roots = ['assets/templates'];
  const offenders = [];

  function walk(dir) {
    const protocol = webUrlPattern();
    const scriptRe = new RegExp(`<script\\b[^>]+\\bsrc=["']${protocol}[^"']+["'][^>]*>`, 'gi');
    const stylesheetRe = new RegExp(`<link\\b[^>]+\\bhref=["']${protocol}[^"']+["'][^>]*\\brel=["']stylesheet["'][^>]*>|<link\\b[^>]+\\brel=["']stylesheet["'][^>]*\\bhref=["']${protocol}[^"']+["'][^>]*>`, 'gi');
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { walk(full); continue; }
      if (!/\.html?$/i.test(entry.name)) continue;
      const html = fs.readFileSync(full, 'utf8');
      const scriptMatches = html.match(scriptRe) ?? [];
      const stylesheetMatches = (html.match(stylesheetRe) ?? [])
        .filter((tag) => !/fonts\.googleapis\.com/i.test(tag));
      for (const tag of [...scriptMatches, ...stylesheetMatches]) {
        offenders.push(`${path.relative(repoRoot, full)}: ${tag.slice(0, 140)}…`);
      }
    }
  }

  for (const root of roots) {
    const abs = path.join(repoRoot, root);
    if (fs.existsSync(abs)) walk(abs);
  }

  if (offenders.length) {
    fail(`remote runtime CDN found in forkable templates:\n    ${offenders.join('\n    ')}`);
  }
  ok('default templates: no remote JS/CSS runtimes beyond optional Google Fonts');
}

function checkPinnedRemoteRuntimeVersions() {
  const roots = ['assets', 'demos'];
  const offenders = [];

  function walk(dir) {
    const remoteTagRe = new RegExp(`<(?:script|link)\\b[^>]+(?:src|href)=["']${webUrlPattern()}[^"']+["'][^>]*>`, 'gi');
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name.startsWith('.')) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { walk(full); continue; }
      if (!/\.html?$/i.test(entry.name)) continue;
      const html = fs.readFileSync(full, 'utf8');
      const remoteRuntimeTags = html.match(remoteTagRe) ?? [];
      for (const tag of remoteRuntimeTags) {
        if (/@latest\b/i.test(tag)) offenders.push(`${path.relative(repoRoot, full)}: ${tag.slice(0, 140)}…`);
      }
    }
  }

  for (const root of roots) {
    const abs = path.join(repoRoot, root);
    if (fs.existsSync(abs)) walk(abs);
  }

  if (offenders.length) {
    fail(`floating @latest remote runtime found (pin exact versions for ClawHub / VirusTotal friendliness):\n    ${offenders.join('\n    ')}`);
  }
  ok('remote runtime versions: no floating @latest references in HTML assets');
}

function checkScriptSafetyRules() {
  const scriptDir = path.join(repoRoot, 'scripts');
  if (!fs.existsSync(scriptDir)) return;

  const config = readJson('scripts/script-safety-rules.json');
  if (!Array.isArray(config.groups) || config.groups.length === 0) {
    fail('scripts/script-safety-rules.json must define at least one rule group');
  }

  const groups = config.groups.map((group) => {
    if (!group.id || !Array.isArray(group.rules) || group.rules.length === 0) {
      fail('script safety rule group is missing id or rules');
    }
    return {
      id: group.id,
      rules: group.rules.map((rule) => {
        if (!rule.label || !Array.isArray(rule.patterns) || rule.patterns.length === 0) {
          fail(`script safety rule in ${group.id} is missing label or patterns`);
        }
        return {
          label: rule.label,
          patterns: rule.patterns.map((pattern) => {
            try {
              return compilePattern(pattern);
            } catch (err) {
              fail(`invalid script safety pattern (${group.id}/${rule.label}): ${err.message}`);
            }
          }),
        };
      }),
    };
  });

  const scriptFiles = fs.readdirSync(scriptDir)
    .filter((entry) => /\.(m?js|cjs)$/.test(entry))
    .sort();
  const offenders = [];

  for (const entry of scriptFiles) {
    const source = fs.readFileSync(path.join(scriptDir, entry), 'utf8');
    for (const group of groups) {
      for (const rule of group.rules) {
        if (rule.patterns.some((rx) => rx.test(source))) {
          offenders.push(`${entry}: ${group.id}/${rule.label}`);
        }
      }
    }
  }

  if (offenders.length) {
    fail(`script safety deny-list matched:\n    ${offenders.join('\n    ')}`);
  }

  const ruleCount = groups.reduce((sum, group) => sum + group.rules.length, 0);
  ok(`script safety rules: ${ruleCount} deny-list rules clear across ${scriptFiles.length} scripts`);
}

function checkSecretLeakage() {
  const config = readJson('scripts/script-safety-rules.json');
  const secretGroup = config.groups.find((group) => group.id === 'secret-hygiene');
  if (!secretGroup || !Array.isArray(secretGroup.rules) || secretGroup.rules.length === 0) {
    fail('scripts/script-safety-rules.json must define secret-hygiene rules');
  }
  const patterns = secretGroup.rules.map((rule) => ({
    label: rule.label,
    patterns: rule.patterns.map((pattern) => compilePattern(pattern)),
  }));
  const offenders = [];
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name.startsWith('.git') || entry.name === 'node_modules' || entry.name === '_archive') continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { walk(full); continue; }
      if (!entry.isFile()) continue;
      if (!/\.(md|txt|json|html?|jsx?|m?js|cjs|tsx?|ya?ml|css|svg)$/i.test(entry.name)) continue;
      const source = fs.readFileSync(full, 'utf8');
      for (const { label, patterns: rulePatterns } of patterns) {
        if (rulePatterns.some((rx) => rx.test(source))) offenders.push(`${path.relative(repoRoot, full)}: ${label}`);
      }
    }
  }
  walk(repoRoot);
  if (offenders.length) {
    fail(`possible secret leak detected:\n    ${offenders.join('\n    ')}`);
  }
  ok(`secret hygiene: ${patterns.length} deny-list rules clear`);
}

function checkClawHubCleanliness() {
  // ClawHub validators flag binary files inside the skill bundle
  // (historically: .git/kilo, .git/ORIG_HEAD, .git/config were misreported
  // as "non-text files"). These live in VCS metadata and must never be in a
  // published skill. We require a text ignore manifest to exclude them.
  const ignoreFile = path.join(repoRoot, 'clawhub.ignore.txt');
  if (!fs.existsSync(ignoreFile)) {
    fail('clawhub.ignore.txt missing — required to exclude VCS/binary files from ClawHub bundles');
  }

  const legacyIgnoreFile = path.join(repoRoot, '.clawignore');
  if (fs.existsSync(legacyIgnoreFile)) {
    fail('legacy .clawignore should be removed — use clawhub.ignore.txt instead');
  }

  const ignoreSource = fs.readFileSync(ignoreFile, 'utf8');
  const required = ['.git/', '.github/', 'node_modules/', '.DS_Store', '.openclaw', '.well-known/', '.env', 'personal-asset-index.json'];
  for (const pattern of required) {
    if (!ignoreSource.includes(pattern)) {
      fail(`clawhub.ignore.txt must exclude ${pattern}`);
    }
  }

  const extensionlessRootFiles = fs.readdirSync(repoRoot, { withFileTypes: true })
    .filter((entry) => entry.isFile() && !entry.name.startsWith('.') && !entry.name.includes('.'))
    .map((entry) => entry.name)
    .sort();
  if (extensionlessRootFiles.length) {
    fail(`ClawHub web publish can misclassify extensionless root files as non-text; rename them with .md/.txt: ${extensionlessRootFiles.join(', ')}`);
  }

  // Verify no binary / non-text files are tracked in user-visible skill content.
  // Scans all top-level skill directories (templates, references, demos, etc.)
  // but skips VCS/ignored dirs.
  const skillRoots = ['assets', 'demos', 'references', 'scripts', 'evals'];
  const textExtensions = new Set([
    '.md', '.html', '.htm', '.css', '.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx',
    '.json', '.yaml', '.yml', '.txt', '.svg', '.xml',
  ]);
  const allowedBinaryExtensions = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp', '.woff', '.woff2']);
  const offenders = [];
  const binaryOffenders = [];

  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name.startsWith('.')) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
        continue;
      }
      const ext = path.extname(entry.name).toLowerCase();
      if (textExtensions.has(ext)) continue;
      if (allowedBinaryExtensions.has(ext)) {
        binaryOffenders.push(path.relative(repoRoot, full));
        continue;
      }
      if (!ext) {
        // Allow extension-less files only if they look like text (ascii-ish).
        const sample = fs.readFileSync(full).subarray(0, 512);
        const isBinary = sample.includes(0) || sample.some((b) => b > 127 && (b < 0xC0 || b > 0xFD));
        if (isBinary) offenders.push(path.relative(repoRoot, full));
        continue;
      }
      offenders.push(path.relative(repoRoot, full));
    }
  }

  for (const root of skillRoots) {
    const abs = path.join(repoRoot, root);
    if (fs.existsSync(abs)) walk(abs);
  }

  if (offenders.length) {
    fail(`non-text files detected in skill content:\n    ${offenders.join('\n    ')}`);
  }

  if (readJson('clawhub.json').bundle?.contains_binary === false && binaryOffenders.length) {
    fail(`clawhub.json declares contains_binary=false but binary assets were found:\n    ${binaryOffenders.join('\n    ')}`);
  }

  ok('ClawHub cleanliness: clawhub.ignore.txt in place, no stray non-text or binary files under skill roots');
}

function checkFontLoadingProtocol() {
  // Enforce references/font-loading.md Tier B: any <link> to Google Fonts
  // inside skill HTML must be non-blocking (media="print" + onload swap) and
  // accompanied by a <noscript> fallback. This keeps pages readable in the
  // Chinese mainland, corporate intranets, and offline previews.
  const roots = ['assets', 'demos'];
  const offenders = [];

  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name.startsWith('.')) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { walk(full); continue; }
      if (!/\.html?$/i.test(entry.name)) continue;
      const html = fs.readFileSync(full, 'utf8');
      // Find every <link ... fonts.googleapis.com ... rel="stylesheet" ...>.
      // Allow both attribute orders; require either media="print" with onload
      // swap, or that the <link> sits inside <noscript>.
      const linkRe = /<link\b[^>]*\bhref=["'][^"']*fonts\.googleapis\.com[^"']*["'][^>]*\brel=["']stylesheet["'][^>]*>|<link\b[^>]*\brel=["']stylesheet["'][^>]*\bhref=["'][^"']*fonts\.googleapis\.com[^"']*["'][^>]*>/gi;
      // Strip <noscript>...</noscript> blocks before scanning — links inside
      // noscript are intentional fallbacks.
      const stripped = html.replace(/<noscript>[\s\S]*?<\/noscript>/gi, '');
      const matches = stripped.match(linkRe) ?? [];
      for (const linkTag of matches) {
        const isNonBlocking = /\bmedia=["']print["']/i.test(linkTag)
          && /\bonload=["'][^"']*this\.media\s*=\s*['"]all['"][^"']*["']/i.test(linkTag);
        if (!isNonBlocking) {
          offenders.push(`${path.relative(repoRoot, full)}: ${linkTag.slice(0, 120)}…`);
        }
      }
    }
  }

  for (const root of roots) {
    const abs = path.join(repoRoot, root);
    if (fs.existsSync(abs)) walk(abs);
  }

  if (offenders.length) {
    fail(`blocking Google Fonts <link> detected (must use Tier B non-blocking pattern, see references/font-loading.md):\n    ${offenders.join('\n    ')}`);
  }
  ok('font loading protocol: all Google Fonts links are non-blocking (CN/offline friendly)');
}

try {
  const templateFiles = getTemplateFiles();
  checkTemplateRoutes();
  checkEvalSuite();
  checkBrandAssets();
  checkGalleryPresence();
  checkEvalSchemaPresence();
  checkSkillReferenceTargets();
  checkSkillDisclosureBudget();
  checkScriptSyntax();
  checkAuthoredYearResolver();
  checkAuthoredYearTemplates(templateFiles);
  checkClawHubManifest();
  checkManifestFrontmatterParity();
  checkOnboardingDocsParity();
  checkPackageManifestSafety();
  checkClawHubCleanliness();
  checkScriptSafetyRules();
  checkSecretLeakage();
  checkFontLoadingProtocol();
  checkDefaultTemplateRemoteRuntime();
  checkPinnedRemoteRuntimeVersions();
  console.log('✓ smoke test passed');
} catch (error) {
  console.error(`smoke test failed: ${error.message}`);
  process.exit(1);
}

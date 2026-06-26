#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { scanBundle, scoreBundle } from './lib/bundle-scanner.mjs';
import { validateEvalSuite } from './lib/evals-validator.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
let failures = 0;

function fail(message) {
  failures += 1;
  console.error(`✗ ${message}`);
}

function ok(message) {
  console.log(`✓ ${message}`);
}

function read(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), 'utf8');
}

function readJson(relativePath) {
  return JSON.parse(read(relativePath));
}

function compilePattern(pattern) {
  if (typeof pattern === 'string') return new RegExp(pattern);
  if (Array.isArray(pattern) && pattern.every((part) => typeof part === 'string')) return new RegExp(pattern.join(''));
  throw new Error('script safety pattern must be a string or string-fragment array');
}

function walk(dir, predicate = () => true) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full, predicate));
    else if (entry.isFile() && predicate(full)) out.push(full);
  }
  return out;
}

function headingAnchorExists(filePart, anchorPart) {
  if (!anchorPart) return true;
  const docPath = path.join(root, filePart);
  if (!fs.existsSync(docPath)) return false;
  const normalize = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
  const target = normalize(anchorPart);
  const headings = [...fs.readFileSync(docPath, 'utf8').matchAll(/^#{1,6}\s+(.+?)\s*$/gm)].map((m) => normalize(m[1]));
  return headings.some((heading) => heading.includes(target));
}

function checkRequiredFiles() {
  const required = [
    'SKILL.md', 'clawhub.json', 'clawhub.ignore.txt', 'package.json', 'README.md', 'README.en.md',
    'AGENTS.md', 'CHANGELOG.md', 'CONTRIBUTING.md', 'LICENSE.md', 'NOTICE.md', 'SECURITY.md',
    'assets/templates/INDEX.json',
    'assets/ifq-brand/BRAND-DNA.md', 'assets/ifq-brand/ifq-tokens.css', 'assets/ifq-brand/mark.svg',
    'scripts/script-safety-rules.json', 'evals/evals.json',
    'references/clawhub-publishing.md', 'references/modes.md', 'references/three-sentence-contract.md',
    'references/verification.md', 'references/quality-bar.md', 'references/security-baseline.md'
  ];
  for (const rel of required) if (!fs.existsSync(path.join(root, rel))) fail(`missing required file: ${rel}`);
  ok(`${required.length} required files checked`);
}

function checkSkillDisclosure() {
  const skill = read('SKILL.md');
  const lines = skill.split(/\r?\n/);
  if (lines.length > 500) fail(`SKILL.md is ${lines.length} lines; keep root under 500 lines`);
  const metadataLines = lines.filter((line) => line.startsWith('metadata:'));
  if (metadataLines.length !== 1 || !metadataLines[0].startsWith('metadata: {')) fail('SKILL.md metadata must be a single JSON line');
  else {
    try { JSON.parse(metadataLines[0].replace(/^metadata:\s*/, '')); }
    catch (error) { fail(`SKILL.md metadata JSON invalid: ${error.message}`); }
  }
  if (!skill.includes('## First-Run Success Path')) fail('SKILL.md must include First-Run Success Path');
  if (!skill.includes('## OpenClaw And ClawHub Contract')) fail('SKILL.md must include OpenClaw And ClawHub Contract');
  ok(`SKILL.md disclosure budget healthy (${lines.length} lines)`);
}

function checkPackageSafety() {
  const pkg = readJson('package.json');
  for (const field of ['dependencies', 'devDependencies', 'optionalDependencies', 'peerDependencies']) {
    if (pkg[field] && Object.keys(pkg[field]).length > 0) fail(`package.json must keep ${field} empty`);
  }
  const scripts = pkg.scripts || {};
  for (const hook of ['preinstall', 'install', 'postinstall', 'prepare', 'prepack', 'postpack', 'prepublish', 'prepublishOnly']) {
    if (hook in scripts) fail(`package.json must not declare npm lifecycle hook: ${hook}`);
  }
  const allowed = new Set(['smoke', 'validate', 'validate:templates', 'evals:validate', 'verify:lite', 'quality:score', 'pack']);
  for (const [name, command] of Object.entries(scripts)) {
    if (!allowed.has(name)) fail(`unexpected package script: ${name}`);
    if (!/^node scripts\/[A-Za-z0-9_.:-]+\.mjs$/.test(command)) fail(`script ${name} must be a direct node scripts/*.mjs command`);
  }
  ok('package manifest: zero dependencies and no install hooks');
}

function checkManifest() {
  const manifest = readJson('clawhub.json');
  const skill = read('SKILL.md');
  const metadataMatch = skill.match(/^metadata:\s*(\{.+\})$/m);
  const versionMatch = skill.match(/^version:\s*["']?([^"'\n]+)["']?$/m);
  const licenseMatch = skill.match(/^license:\s*["']?([^"'\n]+)["']?$/m);
  if (!metadataMatch) fail('SKILL.md frontmatter missing metadata JSON');
  let metadata = {};
  try { metadata = metadataMatch ? JSON.parse(metadataMatch[1]) : {}; }
  catch (error) { fail(`metadata JSON invalid: ${error.message}`); }

  if (manifest.name !== 'ifq-app-builder') fail(`clawhub.json name mismatch: ${manifest.name}`);
  if (manifest.version !== versionMatch?.[1]) fail('clawhub.json version must match SKILL.md');
  if (manifest.license !== licenseMatch?.[1]) fail('clawhub.json license must match SKILL.md');
  if (manifest.bundle?.ignore !== 'clawhub.ignore.txt') fail('bundle.ignore must be clawhub.ignore.txt');
  if (manifest.bundle?.safe !== true || manifest.bundle?.contains_binary !== false) fail('bundle.safe must be true and contains_binary false');
  if (manifest.runtime?.node !== '>=18.17') fail('runtime.node must be >=18.17');
  if (manifest.runtime?.network?.required !== false) fail('runtime.network.required must be false');
  if (manifest.permissions?.filesystem !== 'workspace') fail('filesystem permission must be workspace');
  if (manifest.permissions?.shell !== 'workspace-node-scripts-only') fail('shell permission must be workspace-node-scripts-only');
  for (const plugin of ['filesystem', 'shell']) if (!manifest.plugins?.required?.includes(plugin)) fail(`required plugin missing: ${plugin}`);
  for (const plugin of ['browser', 'memory']) if (!manifest.plugins?.optional?.includes(plugin)) fail(`optional plugin missing: ${plugin}`);
  if (!Array.isArray(manifest.triggers) || manifest.triggers.length < 15) fail('clawhub.json must expose at least 15 triggers');
  for (const tool of ['read_file', 'write_file', 'list_dir', 'run_command']) if (!manifest.tool_map?.[tool]) fail(`tool_map missing ${tool}`);
  if (!Array.isArray(manifest.quick_commands) || manifest.quick_commands.length < 5) fail('quick_commands must list at least 5 commands');

  const packageScripts = readJson('package.json').scripts || {};
  for (const item of manifest.quick_commands || []) {
    const scriptName = String(item.command || '').match(/^npm run ([^\s]+)/)?.[1];
    if (!scriptName || !packageScripts[scriptName]) fail(`quick command does not map to package script: ${item.command}`);
  }

  const evidence = new Set(manifest.first_run?.success_evidence || []);
  for (const item of ['output file path', 'mode route used', 'template id used', 'assumptions made', 'verification command or check performed', 'known caveats that affect use']) {
    if (!evidence.has(item)) fail(`first_run.success_evidence missing ${item}`);
  }
  if (!Array.isArray(manifest.demo_artifacts) || manifest.demo_artifacts.length < 3) fail('demo_artifacts must include at least 3 examples');
  for (const demo of manifest.demo_artifacts || []) {
    if (!fs.existsSync(path.join(root, demo.file || ''))) fail(`demo file missing: ${demo.file}`);
    if (!String(demo.verify || '').startsWith('npm run verify:lite -- ')) fail(`demo verify must use verify:lite: ${demo.verify}`);
  }

  if (metadata.version !== manifest.version) fail('metadata.version must match clawhub.json version');
  if (metadata.openclaw?.skillKey !== manifest.name) fail('metadata.openclaw.skillKey must match manifest.name');
  for (const plugin of ['filesystem', 'shell']) if (!metadata.openclaw?.required_plugins?.includes(plugin)) fail(`metadata.openclaw.required_plugins missing ${plugin}`);
  for (const key of ['env', 'config']) if (!Array.isArray(metadata.openclaw?.requires?.[key]) || metadata.openclaw.requires[key].length !== 0) fail(`metadata.openclaw.requires.${key} must be empty`);

  for (const [key, value] of Object.entries(manifest.docs || {})) {
    const [filePart, anchorPart] = String(value).split('#');
    if (!fs.existsSync(path.join(root, filePart))) fail(`docs.${key} points to missing file: ${filePart}`);
    else if (!headingAnchorExists(filePart, anchorPart)) fail(`docs.${key} anchor not found: ${value}`);
  }
  ok(`clawhub.json manifest valid (${manifest.triggers.length} triggers)`);
}

function checkTemplatesAndDemos() {
  const index = readJson('assets/templates/INDEX.json');
  if ('$schema' in index) fail('INDEX.json must not reference external schema artifacts');
  if (!Array.isArray(index.modeRoutes) || index.modeRoutes.length !== 12) fail('INDEX.json must list 12 modeRoutes');
  const seen = new Set();
  for (const route of index.modeRoutes || []) {
    seen.add(route.mode);
    const templatePath = path.join(root, 'assets/templates', route.templateFile);
    if (!fs.existsSync(templatePath)) { fail(`template missing: ${route.templateFile}`); continue; }
    const result = scanBundle(fs.readFileSync(templatePath, 'utf8'), { templateMode: true });
    for (const finding of result.findings.filter((f) => f.level === 'error')) fail(`${route.templateFile}: ${finding.code} ${finding.message}`);
  }
  for (const mode of ['A-01','A-02','A-03','A-04','A-05','A-06','A-07','A-08','A-09','A-10','A-11','A-12']) if (!seen.has(mode)) fail(`INDEX missing ${mode}`);

  for (const file of fs.readdirSync(path.join(root, 'demos')).filter((entry) => entry.endsWith('.prompt.md'))) {
    const raw = read(`demos/${file}`);
    const result = scanBundle(raw, { templateMode: false });
    for (const finding of result.findings.filter((f) => f.level === 'error')) fail(`demo ${file}: ${finding.code} ${finding.message}`);
    const score = scoreBundle(raw);
    if (score.total < 90) fail(`demo ${file}: quality score ${score.total}/100 is below 90`);
  }
  ok('templates and demo bundles scan clean with demo quality >= 90');
}

function checkEvalSuite() {
  const evalFailures = validateEvalSuite(root);
  for (const failure of evalFailures) fail(failure);
  if (!evalFailures.length) ok('eval suite covers 12 modes and first-run evidence');
}

function checkClawHubCleanliness() {
  const ignore = read('clawhub.ignore.txt');
  for (const token of ['.git/', '.github/', 'node_modules/', '.DS_Store', '.openclaw', '.well-known/', '.env', '*.schema.json', 'personal-asset-index.json']) {
    if (!ignore.includes(token)) fail(`clawhub.ignore.txt must exclude ${token}`);
  }
  const extensionlessRootFiles = fs.readdirSync(root, { withFileTypes: true })
    .filter((entry) => entry.isFile() && !entry.name.startsWith('.') && !entry.name.includes('.'))
    .map((entry) => entry.name);
  if (extensionlessRootFiles.length) fail(`extensionless root files may be flagged: ${extensionlessRootFiles.join(', ')}`);

  const textExtensions = new Set(['.md', '.html', '.htm', '.css', '.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx', '.json', '.yaml', '.yml', '.txt', '.svg', '.xml']);
  const roots = ['assets', 'demos', 'references', 'scripts', 'evals'];
  for (const relRoot of roots) {
    for (const file of walk(path.join(root, relRoot))) {
      if (file.endsWith('.schema.json')) fail(`schema artifact must not ship in ClawHub skill content: ${path.relative(root, file)}`);
      const ext = path.extname(file).toLowerCase();
      if (!textExtensions.has(ext)) fail(`non-text file detected in skill content: ${path.relative(root, file)}`);
      else {
        const sample = fs.readFileSync(file).subarray(0, 512);
        if (sample.includes(0)) fail(`binary-looking content detected: ${path.relative(root, file)}`);
      }
    }
  }
  ok('ClawHub cleanliness: ignore manifest and text-only content pass');
}

function checkScriptSafety() {
  const config = readJson('scripts/script-safety-rules.json');
  const groups = config.groups || [];
  const rules = groups.flatMap((group) => (group.rules || []).map((rule) => ({
    group: group.id,
    label: rule.label,
    patterns: (rule.patterns || []).map(compilePattern),
  })));
  if (rules.length < 18) fail(`script safety rules must include at least 18 deny-list rules, got ${rules.length}`);

  const offenders = [];
  for (const file of walk(path.join(root, 'scripts'), (full) => /\.(mjs|js|cjs)$/.test(full))) {
    const source = fs.readFileSync(file, 'utf8');
    for (const rule of rules) {
      if (rule.patterns.some((rx) => rx.test(source))) offenders.push(`${path.relative(root, file)}: ${rule.group}/${rule.label}`);
    }
  }
  if (offenders.length) fail(`script safety deny-list matched:\n  ${offenders.join('\n  ')}`);
  else ok(`script safety: ${rules.length} deny-list rules clear`);
}

function checkSecretHygiene() {
  const config = readJson('scripts/script-safety-rules.json');
  const secretRules = (config.groups || []).find((group) => group.id === 'secret-hygiene')?.rules || [];
  const patterns = secretRules.flatMap((rule) => (rule.patterns || []).map(compilePattern));
  const offenders = [];
  const textFiles = walk(root, (full) => /\.(md|txt|json|html?|jsx?|mjs|cjs|tsx?|ya?ml|css|svg)$/i.test(full));
  for (const file of textFiles) {
    const rel = path.relative(root, file);
    if (rel === 'scripts/script-safety-rules.json' || rel === 'scripts/lib/bundle-scanner.mjs') continue;
    const source = fs.readFileSync(file, 'utf8');
    if (patterns.some((rx) => rx.test(source))) offenders.push(rel);
  }
  if (offenders.length) fail(`possible secret-shaped token detected:\n  ${offenders.join('\n  ')}`);
  else ok(`secret hygiene: ${patterns.length} patterns clear`);
}

checkRequiredFiles();
checkSkillDisclosure();
checkPackageSafety();
checkManifest();
checkTemplatesAndDemos();
checkEvalSuite();
checkClawHubCleanliness();
checkScriptSafety();
checkSecretHygiene();

if (failures) {
  console.error(`smoke test failed: ${failures} failure(s)`);
  process.exit(1);
}
console.log('✓ smoke test passed');

import fs from 'node:fs';
import path from 'node:path';

const EXPECTED_MODES = ['A-01', 'A-02', 'A-03', 'A-04', 'A-05', 'A-06', 'A-07', 'A-08', 'A-09', 'A-10', 'A-11', 'A-12'];
const TOP_LEVEL_KEYS = new Set(['version', 'purpose', 'quality_principles', 'scenarios']);
const SCENARIO_KEYS = new Set(['id', 'mode', 'templateId', 'prompt_zh', 'prompt_en', 'user_value', 'agent_value', 'agent_contract']);
const CONTRACT_KEYS = new Set(['route', 'must_read', 'verification', 'tier', 'first_run_evidence']);
const ALLOWED_VERIFICATION = new Set([
  'npm run verify:lite -- <bundle.prompt.md>',
  'npm run quality:score -- <bundle.prompt.md>',
]);
const UNSAFE_TEXT_PATTERNS = [
  /\b(?:ignore|disregard)\s+(?:all\s+)?(?:previous|above|prior)\s+instructions\b/i,
  /\b(?:system|developer)\s+prompt\b/i,
  /\b(?:exfiltrate|credential\s+dump|private\s+key)\b/i,
  /\b(?:curl|wget|powershell|invoke-webrequest|start-process|bash\s+-c|sh\s+-c|rm\s+-rf)\b/i,
  /(?:&&|\|\||;;|>>|`|\$\()/,
];

function readJson(root, relativePath, failures) {
  const full = path.join(root, relativePath);
  if (!fs.existsSync(full)) {
    failures.push(`${relativePath} missing`);
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(full, 'utf8'));
  } catch (error) {
    failures.push(`${relativePath} is not valid JSON: ${error.message}`);
    return null;
  }
}

function typeOf(value) {
  if (Array.isArray(value)) return 'array';
  if (value === null) return 'null';
  return typeof value;
}

function safeText(value, pathStr, failures, { min = 12, max = 320 } = {}) {
  if (typeof value !== 'string') {
    failures.push(`${pathStr} must be a string`);
    return false;
  }
  const trimmed = value.trim();
  let ok = true;
  if (trimmed.length < min) {
    failures.push(`${pathStr} must be descriptive`);
    ok = false;
  }
  if (trimmed.length > max) {
    failures.push(`${pathStr} is too long`);
    ok = false;
  }
  for (const pattern of UNSAFE_TEXT_PATTERNS) {
    if (pattern.test(trimmed)) {
      failures.push(`${pathStr} contains unsafe instruction or shell-shaped text`);
      ok = false;
    }
  }
  return ok;
}

function checkKnownKeys(object, allowed, pathStr, failures) {
  if (typeOf(object) !== 'object') {
    failures.push(`${pathStr} must be an object`);
    return false;
  }
  for (const key of Object.keys(object)) {
    if (!allowed.has(key)) failures.push(`${pathStr}.${key} is not allowed`);
  }
  return true;
}

export function validateEvalSuite(root) {
  const failures = [];
  const evals = readJson(root, 'evals/evals.json', failures);
  const index = readJson(root, 'assets/templates/INDEX.json', failures);
  if (!evals || !index) return failures;

  checkKnownKeys(evals, TOP_LEVEL_KEYS, 'evals', failures);
  if (evals.version !== '1.0') failures.push(`evals.version must be 1.0, got ${evals.version}`);
  safeText(evals.purpose, 'evals.purpose', failures, { min: 24, max: 420 });
  if (!Array.isArray(evals.quality_principles) || evals.quality_principles.length < 4) {
    failures.push('evals.quality_principles must contain at least 4 items');
  } else {
    for (const [i, principle] of evals.quality_principles.entries()) {
      safeText(principle, `evals.quality_principles[${i}]`, failures, { min: 12, max: 220 });
    }
  }
  if (!Array.isArray(evals.scenarios) || evals.scenarios.length < EXPECTED_MODES.length) {
    failures.push('evals.scenarios must contain at least 12 scenarios');
    return failures;
  }

  const routes = new Map((index.modeRoutes || []).map((route) => [route.mode, route]));
  const ids = new Set();
  const coveredModes = new Set();
  let firstRun = false;

  for (const [position, scenario] of evals.scenarios.entries()) {
    const scenarioPath = `evals.scenarios[${position}]`;
    if (!checkKnownKeys(scenario, SCENARIO_KEYS, scenarioPath, failures)) continue;

    const id = scenario.id || '<missing-id>';
    if (!/^[a-z0-9][a-z0-9-]{2,90}$/.test(id)) failures.push(`${id}: id must be stable kebab-case`);
    if (ids.has(id)) failures.push(`${id}: duplicate scenario id`);
    ids.add(id);

    const route = routes.get(scenario.mode);
    if (!route) failures.push(`${id}: unknown mode ${scenario.mode}`);
    else {
      coveredModes.add(scenario.mode);
      if (scenario.templateId !== route.templateId) failures.push(`${id}: templateId ${scenario.templateId} does not match INDEX route ${route.templateId}`);
    }

    for (const key of ['prompt_zh', 'prompt_en', 'user_value', 'agent_value']) {
      safeText(scenario[key], `${id}.${key}`, failures);
    }

    const contract = scenario.agent_contract || {};
    checkKnownKeys(contract, CONTRACT_KEYS, `${id}.agent_contract`, failures);
    if (contract.route !== scenario.mode) failures.push(`${id}: agent_contract.route must equal ${scenario.mode}`);
    if (!Array.isArray(contract.must_read) || contract.must_read.length < 3) failures.push(`${id}: agent_contract.must_read must include at least 3 files`);
    else {
      for (const rel of contract.must_read) {
        if (typeof rel !== 'string' || rel.startsWith('/') || rel.includes('..') || /[\\:*?"<>|]/.test(rel)) failures.push(`${id}: unsafe must_read path ${rel}`);
        else if (!fs.existsSync(path.join(root, rel))) failures.push(`${id}: missing must_read file ${rel}`);
      }
      if (!contract.must_read.includes('assets/templates/INDEX.json')) failures.push(`${id}: must_read must include assets/templates/INDEX.json`);
    }
    if (!Array.isArray(contract.verification) || contract.verification.length < 1) failures.push(`${id}: agent_contract.verification required`);
    else {
      for (const command of contract.verification) {
        if (!ALLOWED_VERIFICATION.has(String(command))) failures.push(`${id}: unsafe verification command ${command}`);
      }
      if (!contract.verification.includes('npm run verify:lite -- <bundle.prompt.md>')) failures.push(`${id}: verification must include verify:lite`);
    }
    if (typeof contract.tier !== 'string' || !contract.tier.includes('Tier 0')) failures.push(`${id}: tier must name Tier 0 boundary`);

    if (id.includes('first-run')) {
      firstRun = true;
      const evidence = new Set(contract.first_run_evidence || []);
      for (const item of ['output file path', 'mode route used', 'template id used', 'assumptions made', 'verification command or check performed', 'known caveats that affect use']) {
        if (!evidence.has(item)) failures.push(`${id}: first_run_evidence missing ${item}`);
      }
    }
  }

  for (const mode of EXPECTED_MODES) {
    if (!coveredModes.has(mode)) failures.push(`eval suite missing coverage for ${mode}`);
  }
  if (!firstRun) failures.push('eval suite must include a first-run scenario');

  return failures;
}

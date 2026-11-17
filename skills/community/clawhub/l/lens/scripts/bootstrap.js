import fs from 'fs';
import os from 'os';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const __filename = fs.realpathSync(fileURLToPath(import.meta.url));
const __dirname = path.dirname(__filename);
export const SKILL_DIR = path.resolve(__dirname, '..');
export const HOME_DIR = process.env.HOME || os.homedir();
export const LENS_DIR = path.join(HOME_DIR, '.lens');
export const DEFAULT_SOURCES = ['antigravity', 'openclaw', 'claude', 'codex'];
export const VALID_RUNNERS = ['antigravity', 'openclaw', 'claude', 'codex', 'none'];

export function checkAccess(err) {
  if (err && (err.code === 'EPERM' || err.code === 'EACCES')) {
    console.error(`LENS_ACCESS_DENIED: Permission denied accessing ${err.path || LENS_DIR}. Re-run outside the workspace sandbox or grant access to ~/.lens.`);
    process.exit(1);
  }
}

const packagePath = path.join(SKILL_DIR, 'package.json');
const LENS_VERSION = JSON.parse(fs.readFileSync(packagePath, 'utf8')).version;
const isMain = Boolean(
  process.argv[1] &&
  fs.existsSync(process.argv[1]) &&
  fs.realpathSync(path.resolve(process.argv[1])) === __filename
);

function readOpenClawConfig() {
  try {
    if (HOME_DIR) {
      const configPath = path.join(HOME_DIR, '.openclaw/openclaw.json');
      if (fs.existsSync(configPath)) {
        return JSON.parse(fs.readFileSync(configPath, 'utf8'));
      }
    }
  } catch (e) {}
  return null;
}

function getInterviewCronExpr(phase) {
  if (phase === 'stabilizing') return '30 11 * * *';
  if (phase === 'habitual') return '30 11 * * 3';
  return '30 11,17 * * *';
}

function detectDefaultRunner(openclawConfig = null) {
  if (process.env.OPENCLAW_CRON_LIST || process.env.OPENCLAW_HOME) return 'openclaw';
  if (process.env.ANTIGRAVITY_CLI_ALIAS || process.env.ANTIGRAVITY_AGENT) return 'antigravity';
  if (openclawConfig || (HOME_DIR && fs.existsSync(path.join(HOME_DIR, '.openclaw')))) return 'openclaw';
  if (
    HOME_DIR &&
    (fs.existsSync(path.join(HOME_DIR, '.gemini/config')) || fs.existsSync(path.join(HOME_DIR, '.gemini/antigravity')))
  ) {
    return 'antigravity';
  }
  if (process.env.CLAUDECODE || process.env.CLAUDE_CODE_ENTRYPOINT) return 'claude';
  if (process.env.CODEX_SANDBOX || process.env.CODEX_THREAD_ID) return 'codex';
  if (HOME_DIR && fs.existsSync(path.join(HOME_DIR, '.claude'))) return 'claude';
  if (
    (process.env.CODEX_HOME && fs.existsSync(process.env.CODEX_HOME)) ||
    (HOME_DIR && fs.existsSync(path.join(HOME_DIR, '.codex')))
  ) {
    return 'codex';
  }
  return 'none';
}

function normalizeModel(model, priorVersion = '') {
  if (typeof model !== 'string' || !model.trim()) return 'default';
  const trimmed = model.trim();
  if (priorVersion && !priorVersion.startsWith('2.') && trimmed === 'google/gemini-3.1-pro-preview') {
    return 'default';
  }
  return trimmed;
}

function resolvePayloadModel(model) {
  return !model || model === 'default' ? undefined : model;
}

function writeFileIfChanged(filePath, content) {
  if (fs.existsSync(filePath)) {
    try {
      if (fs.readFileSync(filePath, 'utf8') === content) return;
    } catch (e) {}
  }
  fs.writeFileSync(filePath, content, 'utf8');
}

function ensureSkillLink(linkPath, reboot = false) {
  try {
    let stat = null;
    try {
      stat = fs.lstatSync(linkPath);
    } catch (e) {}

    if (stat) {
      if (stat.isSymbolicLink()) {
        let resolvedTarget = null;
        try {
          resolvedTarget = fs.realpathSync(linkPath);
        } catch (e) {}
        if (resolvedTarget === SKILL_DIR) {
          return linkPath;
        }
        const rawTarget = path.resolve(path.dirname(linkPath), fs.readlinkSync(linkPath));
        const isBrokenOrLensTarget = !resolvedTarget || path.basename(rawTarget) === 'lens';
        if (reboot && !isBrokenOrLensTarget) {
          return null;
        }
        fs.unlinkSync(linkPath);
      } else {
        return null;
      }
    }

    fs.mkdirSync(path.dirname(linkPath), { recursive: true });
    fs.symlinkSync(SKILL_DIR, linkPath, process.platform === 'win32' ? 'junction' : 'dir');
    return linkPath;
  } catch (e) {
    if (!reboot) checkAccess(e);
    return null;
  }
}

function syncSkillLinks(reboot = false, openclawConfig = null) {
  const linked = [];
  if (!HOME_DIR) return linked;

  const geminiDir = path.join(HOME_DIR, '.gemini');
  if (fs.existsSync(geminiDir)) {
    const agyConfigDir = path.join(geminiDir, 'config');
    const agyDir = path.join(geminiDir, 'antigravity');
    const agyCliDir = path.join(geminiDir, 'antigravity-cli');
    if (fs.existsSync(agyConfigDir) || fs.existsSync(agyDir) || fs.existsSync(agyCliDir)) {
      const skillsJsonPath = path.join(agyConfigDir, 'skills.json');
      let coveredBySkillsJson = false;
      if (fs.existsSync(skillsJsonPath)) {
        try {
          const raw = fs.readFileSync(skillsJsonPath, 'utf8');
          const escapedSkillDir = SKILL_DIR.replace(/\\/g, '\\\\');
          if (raw.includes(SKILL_DIR) || raw.includes(escapedSkillDir)) {
            coveredBySkillsJson = true;
            linked.push(skillsJsonPath);
          }
        } catch (e) {}
      }
      if (!coveredBySkillsJson) {
        const agyLink = ensureSkillLink(path.join(agyConfigDir, 'skills', 'lens'), reboot);
        if (agyLink) linked.push(agyLink);
      }
    }
  }

  const claudeDir = path.join(HOME_DIR, '.claude');
  if (fs.existsSync(claudeDir)) {
    const claudeLink = ensureSkillLink(path.join(claudeDir, 'skills', 'lens'), reboot);
    if (claudeLink) linked.push(claudeLink);
  }

  const codexDir = process.env.CODEX_HOME || path.join(HOME_DIR, '.codex');
  if (fs.existsSync(codexDir)) {
    const codexLink = ensureSkillLink(path.join(codexDir, 'skills', 'lens'), reboot);
    if (codexLink) linked.push(codexLink);
  }

  if (openclawConfig) {
    const rawWs = openclawConfig.agents?.defaults?.workspace;
    if (typeof rawWs === 'string' && rawWs.trim()) {
      const ws = rawWs.startsWith('~/') ? path.join(HOME_DIR, rawWs.slice(2)) : rawWs;
      if (fs.existsSync(ws)) {
        const wsLink = ensureSkillLink(path.join(ws, 'skills', 'lens'), reboot);
        if (wsLink) linked.push(wsLink);
      }
    }
  }

  return linked;
}

function syncAntigravitySidecars(timezone, interviewExpr, distillationPrompt, interviewPrompt, scope, reboot = false) {
  const synced = [];
  if (!HOME_DIR) return synced;

  const geminiDir = path.join(HOME_DIR, '.gemini');
  const agyConfigDir = path.join(geminiDir, 'config');
  const agyDir = path.join(geminiDir, 'antigravity');
  if (!fs.existsSync(agyConfigDir) && !fs.existsSync(agyDir)) return synced;

  const sidecarsRoot = path.join(agyConfigDir, 'sidecars');
  const lensWorkspaceUri = pathToFileURL(LENS_DIR).href;
  const distillationScript = path.join(__dirname, 'distillation.js');
  const interviewScript = path.join(__dirname, 'interview.js');
  const bootstrapScript = path.join(__dirname, 'bootstrap.js');

  const definitions = [
    {
      id: 'lens-distillation',
      enabled: scope.distillation?.runner === 'antigravity',
      config: {
        builtin: 'schedule',
        args: [
          `CRON_TZ=${timezone} 0 3 * * *`,
          'agentapi',
          'new-conversation',
          '--',
          distillationPrompt
        ],
        restart_policy: 'always',
        display_name: 'LENS Nightly Distillation',
        description: `Every night at 3:00 AM (${timezone}), harvests recent user messages across your AI tools into ~/.lens/TRACE.txt and distills enduring insights into ~/.lens/AXIOM.yaml, ETHOS.yaml, and MODUS.yaml.`,
        agent_permissions: {
          workspace_uris: [lensWorkspaceUri],
          access_grants: [
            `command(node ${distillationScript})`,
            `command(node ${distillationScript} --commit)`,
            `command(node ${bootstrapScript})`,
            `read_file(${LENS_DIR})`,
            `write_file(${LENS_DIR})`,
            `read_file(${SKILL_DIR})`
          ]
        }
      }
    },
    {
      id: 'lens-interview',
      enabled: scope.interview?.runner === 'antigravity',
      config: {
        builtin: 'schedule',
        args: [
          `CRON_TZ=${timezone} ${interviewExpr}`,
          'agentapi',
          'new-conversation',
          '--',
          interviewPrompt
        ],
        restart_policy: 'always',
        display_name: 'LENS Calibration Interview',
        description: `Runs on schedule (${interviewExpr} ${timezone}) to ask a single scenario or trade-off calibration question that sharpens your ~/.lens/ Trinity Nodes.`,
        agent_permissions: {
          workspace_uris: [lensWorkspaceUri],
          access_grants: [
            `command(node ${interviewScript})`,
            `command(node ${distillationScript})`,
            `command(node ${distillationScript} --commit)`,
            `command(node ${bootstrapScript})`,
            `read_file(${LENS_DIR})`,
            `write_file(${LENS_DIR})`,
            `read_file(${SKILL_DIR})`
          ]
        }
      }
    }
  ];

  for (const def of definitions) {
    try {
      const dir = path.join(sidecarsRoot, def.id);
      const filePath = path.join(dir, 'sidecar.json');
      if (def.enabled) {
        fs.mkdirSync(dir, { recursive: true });
        writeFileIfChanged(filePath, JSON.stringify(def.config, null, 2) + '\n');
        synced.push(filePath);
      } else if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
        try {
          fs.rmdirSync(dir);
        } catch (rmErr) {}
      }
    } catch (e) {
      if (!reboot) checkAccess(e);
    }
  }

  return synced;
}

export function bootstrap(reboot = false) {
  try {
    if (!fs.existsSync(LENS_DIR)) fs.mkdirSync(LENS_DIR, { recursive: true });
  } catch (e) {
    checkAccess(e);
    throw e;
  }

  const axiomPath = path.join(LENS_DIR, 'AXIOM.yaml');
  const ethosPath = path.join(LENS_DIR, 'ETHOS.yaml');
  const modusPath = path.join(LENS_DIR, 'MODUS.yaml');
  const readmePath = path.join(LENS_DIR, 'README.md');
  const scopePath = path.join(LENS_DIR, 'SCOPE.json');
  const tracePath = path.join(LENS_DIR, 'TRACE.txt');

  const openclawConfig = readOpenClawConfig();
  const timezone = openclawConfig?.agents?.defaults?.userTimezone || Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
  const defaultRunner = detectDefaultRunner(openclawConfig);

  let scope = {
    meta: {
      version: LENS_VERSION,
      installed: new Date().toISOString().split('T')[0],
      anonymize: false,
      push: false
    },
    interview: {
      phase: 'onboarding',
      questions: 15,
      runner: defaultRunner,
      model: 'default'
    },
    distillation: {
      runner: defaultRunner,
      model: 'default',
      sources: [...DEFAULT_SOURCES]
    }
  };

  if (fs.existsSync(scopePath)) {
    try {
      const existing = JSON.parse(fs.readFileSync(scopePath, 'utf8'));
      const priorVersion = String(existing.meta?.version || '');
      scope.meta = {
        ...scope.meta,
        ...(existing.meta || {}),
        version: LENS_VERSION,
        anonymize: Boolean(existing.meta?.anonymize),
        push: typeof existing.meta?.push === 'boolean' ? existing.meta.push : false
      };
      scope.interview = {
        ...scope.interview,
        ...(existing.interview || {}),
        runner: VALID_RUNNERS.includes(existing.interview?.runner) ? existing.interview.runner : defaultRunner,
        model: normalizeModel(existing.interview?.model, priorVersion)
      };
      scope.distillation = {
        ...scope.distillation,
        ...(existing.distillation || {}),
        runner: VALID_RUNNERS.includes(existing.distillation?.runner) ? existing.distillation.runner : defaultRunner,
        model: normalizeModel(existing.distillation?.model, priorVersion),
        sources: Array.isArray(existing.distillation?.sources) ? existing.distillation.sources : [...DEFAULT_SOURCES]
      };

      if (typeof scope.interview.questions === 'number' && scope.interview.questions <= 0) {
        if (scope.interview.phase === 'onboarding') {
          scope.interview.phase = 'stabilizing';
          scope.interview.questions = 22;
        } else {
          scope.interview.phase = 'habitual';
          scope.interview.questions = true;
        }
      }
    } catch (e) {
      checkAccess(e);
      try {
        fs.copyFileSync(scopePath, path.join(LENS_DIR, 'scope.json.corrupt.bak'));
      } catch (copyErr) {}
    }
  }

  const interviewExpr = getInterviewCronExpr(scope.interview.phase);

  const distillationPrompt = `Run \`node ${path.join(__dirname, 'distillation.js')}\`. If the output is 'TRACE_EMPTY', reply with ONLY: NO_REPLY and stop. If the output includes 'DISTILLATION_READY', read \`${path.join(SKILL_DIR, 'prompts/distillation.md')}\` and follow it strictly.`;
  const interviewPrompt = `Run \`node ${path.join(__dirname, 'interview.js')}\`. If the output includes 'INTERVIEW_READY', read \`${path.join(SKILL_DIR, 'prompts/interview.md')}\` and follow it strictly. Generate a single question for the human and stop.`;

  const jobs = [];
  const removeJobs = [];

  if (scope.distillation.runner === 'openclaw') {
    jobs.push({
      id: 'lens-distillation',
      name: 'lens-distillation',
      schedule: { kind: 'cron', expr: '0 3 * * *', tz: timezone },
      sessionTarget: 'isolated',
      payload: {
        kind: 'agentTurn',
        message: distillationPrompt,
        model: resolvePayloadModel(scope.distillation.model)
      },
      delivery: {
        mode: 'none'
      }
    });
  } else {
    removeJobs.push('lens-distillation');
  }

  if (scope.interview.runner === 'openclaw') {
    jobs.push({
      id: 'lens-interview',
      name: 'lens-interview',
      schedule: { kind: 'cron', expr: interviewExpr, tz: timezone },
      sessionTarget: 'main',
      payload: {
        kind: 'systemEvent',
        text: interviewPrompt,
        model: resolvePayloadModel(scope.interview.model)
      }
    });
  } else {
    removeJobs.push('lens-interview');
  }

  try {
    writeFileIfChanged(scopePath, JSON.stringify(scope, null, 2) + '\n');
    if (!fs.existsSync(tracePath)) fs.writeFileSync(tracePath, '', 'utf8');

    const templatesDir = path.join(__dirname, 'templates');
    const lensNodes = [
      { name: 'AXIOM.yaml', path: axiomPath },
      { name: 'ETHOS.yaml', path: ethosPath },
      { name: 'MODUS.yaml', path: modusPath }
    ];

    lensNodes.forEach(lensNode => {
      if (!fs.existsSync(lensNode.path)) {
        fs.copyFileSync(path.join(templatesDir, lensNode.name), lensNode.path);
      }
    });
    writeFileIfChanged(readmePath, fs.readFileSync(path.join(templatesDir, 'README.md'), 'utf8'));
  } catch (e) {
    checkAccess(e);
    throw e;
  }

  const linkedSkills = syncSkillLinks(reboot, openclawConfig);
  const antigravitySidecars = syncAntigravitySidecars(timezone, interviewExpr, distillationPrompt, interviewPrompt, scope, reboot);
  const isInitialOnboarding = !reboot && scope.interview.runner !== 'none' && scope.interview.phase === 'onboarding' && scope.interview.questions === 15;

  const result = {
    jobs,
    removeJobs,
    timezone,
    lensDir: LENS_DIR,
    skillDir: SKILL_DIR,
    linkedSkills,
    antigravitySidecars,
    triggerImmediate: isInitialOnboarding ? 'lens-interview' : null
  };

  if (reboot || isMain) {
    console.log('BOOTSTRAP_LENS: RESULT_START');
    console.log(JSON.stringify(result, null, 2));
    console.log('BOOTSTRAP_LENS: RESULT_END');
  }

  return scope;
}

export function preflight(job) {
  const scopePath = path.join(LENS_DIR, 'SCOPE.json');
  let scope = null;
  let needsReboot = !fs.existsSync(scopePath);

  if (!needsReboot) {
    try {
      scope = JSON.parse(fs.readFileSync(scopePath, 'utf8'));
      const expectedInterviewExpr = getInterviewCronExpr(scope.interview?.phase);

      if (
        scope.meta?.version !== LENS_VERSION ||
        typeof scope.meta?.push !== 'boolean' ||
        !VALID_RUNNERS.includes(scope.interview?.runner) ||
        !VALID_RUNNERS.includes(scope.distillation?.runner) ||
        typeof scope.interview?.model !== 'string' ||
        !scope.interview.model.trim() ||
        typeof scope.distillation?.model !== 'string' ||
        !scope.distillation.model.trim() ||
        !Array.isArray(scope.distillation?.sources)
      ) {
        needsReboot = true;
      } else {
        if (process.env.OPENCLAW_CRON_LIST) {
          const parsed = JSON.parse(process.env.OPENCLAW_CRON_LIST);
          const crons = Array.isArray(parsed) ? parsed : (Array.isArray(parsed?.jobs) ? parsed.jobs : []);
          const distillationCron = crons.find(j => j.name === 'lens-distillation');
          const interviewCron = crons.find(j => j.name === 'lens-interview');

          if (scope.distillation.runner === 'openclaw') {
            const distillationText = distillationCron?.payload?.message || distillationCron?.payload?.text || '';
            const expectedDistModel = resolvePayloadModel(scope.distillation.model) || '';
            if (
              !distillationCron ||
              !distillationText.includes(path.join(__dirname, 'distillation.js')) ||
              expectedDistModel !== (distillationCron.payload?.model || '')
            ) {
              needsReboot = true;
            }
          } else if (distillationCron) {
            needsReboot = true;
          }

          if (scope.interview.runner === 'openclaw') {
            const interviewText = interviewCron?.payload?.message || interviewCron?.payload?.text || '';
            const expectedIntModel = resolvePayloadModel(scope.interview.model) || '';
            if (
              !interviewCron ||
              !interviewText.includes(path.join(__dirname, 'interview.js')) ||
              interviewCron.schedule?.expr !== expectedInterviewExpr ||
              expectedIntModel !== (interviewCron.payload?.model || '')
            ) {
              needsReboot = true;
            }
          } else if (interviewCron) {
            needsReboot = true;
          }
        }

        if (!needsReboot && HOME_DIR) {
          const agyConfigDir = path.join(HOME_DIR, '.gemini', 'config');
          const agyDir = path.join(HOME_DIR, '.gemini', 'antigravity');
          if (fs.existsSync(agyConfigDir) || fs.existsSync(agyDir)) {
            const distSidecar = path.join(agyConfigDir, 'sidecars', 'lens-distillation', 'sidecar.json');
            const intSidecar = path.join(agyConfigDir, 'sidecars', 'lens-interview', 'sidecar.json');
            const hasDistSidecar = fs.existsSync(distSidecar);
            const hasIntSidecar = fs.existsSync(intSidecar);
            if (
              hasDistSidecar !== (scope.distillation.runner === 'antigravity') ||
              hasIntSidecar !== (scope.interview.runner === 'antigravity')
            ) {
              needsReboot = true;
            }
          }
        }
      }

      if (job === 'interview') {
        if (typeof scope.interview?.questions === 'number' && scope.interview.questions <= 0) {
          needsReboot = true;
        }
      }
    } catch (e) {
      checkAccess(e);
      needsReboot = true;
    }
  }

  if (needsReboot) {
    scope = bootstrap(true);
  }

  return { scope, rebooted: needsReboot };
}

if (isMain) bootstrap();

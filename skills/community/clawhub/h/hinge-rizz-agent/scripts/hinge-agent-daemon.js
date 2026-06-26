#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const readline = require('node:readline/promises');
const { spawn, spawnSync } = require('child_process');
const {
  AGENT_MODE_DEFINITIONS,
  buildAgentModePolicy,
  defaultConfig,
  ensureDir,
  normalizeAgentMode,
  nowIso,
  readJson,
  resolvePaths,
  writeJson
} = require('./session-utils');

const args = process.argv.slice(2);
const rootDir = path.resolve(__dirname, '..');
const defaultWorkspaceDir = path.resolve(rootDir, '..', '..', 'workspaces', 'hinge-automation');
const defaultDataDir = path.join(rootDir, 'hinge-data');
const appiumScript = path.join(rootDir, 'scripts', 'appium-ios.js');
const hingeScript = path.join(rootDir, 'scripts', 'hinge-ios.js');
const autopilotScript = path.join(rootDir, 'scripts', 'discover-autopilot.js');

function hasFlag(name) {
  return args.includes(name);
}

function getArg(name, fallback = '') {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] || fallback;
}

function toNumber(value, fallback) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function toBoolean(value, fallback) {
  if (value === undefined || value === null || String(value).trim() === '') {
    return fallback;
  }
  const normalized = String(value).trim().toLowerCase();
  if (['1', 'true', 'yes', 'on'].includes(normalized)) return true;
  if (['0', 'false', 'no', 'off'].includes(normalized)) return false;
  return fallback;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function rotateLogIfLarge(filePath, maxBytes = 10 * 1024 * 1024) {
  try {
    if (!filePath || !fs.existsSync(filePath)) return;
    const stat = fs.statSync(filePath);
    if (!stat.isFile() || stat.size <= maxBytes) return;
    const rotatedPath = `${filePath}.1`;
    if (fs.existsSync(rotatedPath)) {
      fs.unlinkSync(rotatedPath);
    }
    fs.renameSync(filePath, rotatedPath);
  } catch (error) {
    // Ignore log-rotation errors to avoid blocking automation startup.
  }
}

function unique(values) {
  return [...new Set((values || []).filter(Boolean))];
}

const OBSERVE_STOP_WORDS = new Set([
  'about',
  'after',
  'again',
  'all',
  'also',
  'and',
  'any',
  'are',
  'back',
  'been',
  'being',
  'both',
  'but',
  'can',
  'could',
  'did',
  'does',
  'dont',
  'for',
  'from',
  'have',
  'her',
  'hers',
  'him',
  'his',
  'into',
  'its',
  'just',
  'like',
  'more',
  'much',
  'not',
  'one',
  'only',
  'ours',
  'over',
  'really',
  'same',
  'some',
  'that',
  'than',
  'the',
  'their',
  'them',
  'then',
  'they',
  'this',
  'very',
  'want',
  'what',
  'when',
  'where',
  'which',
  'who',
  'with',
  'would',
  'you',
  'your',
  'youre'
]);

function tokenize(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .map((token) => token.trim())
    .filter((token) => token.length >= 3 && !OBSERVE_STOP_WORDS.has(token));
}

function oneLiner(value, maxWords = 14) {
  const compact = String(value || '').replace(/\s+/g, ' ').trim();
  if (!compact) return '';
  const firstSentence = compact.match(/^(.+?[.!?])(?:\s|$)/)?.[1] || compact;
  const words = firstSentence.split(/\s+/).filter(Boolean);
  return words.slice(0, maxWords).join(' ').trim();
}

function briefPhrase(value, maxWords = 6) {
  const compact = String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  if (!compact) return '';
  const words = compact.split(' ').filter(Boolean);
  if (words.length < 2) return '';
  return words.slice(0, maxWords).join(' ');
}

function defaultObservationLog() {
  const timestamp = nowIso();
  return {
    createdAt: timestamp,
    updatedAt: timestamp,
    sessions: []
  };
}

function readObservationLog(paths) {
  return readJson(paths.observationPath, defaultObservationLog());
}

function writeObservationLog(paths, observationLog) {
  writeJson(paths.observationPath, {
    ...observationLog,
    updatedAt: nowIso()
  });
}

function resolveAutomationWorkspace() {
  const explicit = getArg('--workspace-dir', process.env.HINGE_AUTOMATION_WORKSPACE || '');
  if (explicit) return path.resolve(explicit);
  if (fs.existsSync(defaultWorkspaceDir)) return defaultWorkspaceDir;
  return process.cwd();
}

function loadWorkspace(dirPath) {
  const paths = resolvePaths(dirPath);
  ensureDir(paths.root);
  return {
    paths,
    config: readJson(paths.configPath, defaultConfig())
  };
}

function readJsonFileSafe(filePath) {
  try {
    if (!filePath || !fs.existsSync(filePath)) return null;
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch (error) {
    return null;
  }
}

function readOpenClawOpenAiApiKey() {
  const candidates = [
    path.resolve(rootDir, '..', '..', 'openclaw.json'),
    path.resolve(process.cwd(), 'openclaw.json')
  ];

  for (const configPath of candidates) {
    const config = readJsonFileSafe(configPath);
    const key = config?.models?.providers?.openai?.apiKey;
    if (typeof key === 'string' && key.startsWith('sk-')) {
      return key.trim();
    }
  }

  return '';
}

function resolveOpenAiApiKey(config) {
  if (typeof process.env.OPENAI_API_KEY === 'string' && process.env.OPENAI_API_KEY.trim()) {
    return process.env.OPENAI_API_KEY.trim();
  }

  const keyCandidates = [
    config?.ai?.openaiApiKey,
    config?.ai?.openAiApiKey,
    config?.ai?.apiKey
  ];
  for (const candidate of keyCandidates) {
    if (typeof candidate === 'string' && candidate.trim().startsWith('sk-')) {
      return candidate.trim();
    }
  }

  return readOpenClawOpenAiApiKey();
}

function readState(paths) {
  return readJson(paths.agentStatePath, {
    startedAt: '',
    updatedAt: '',
    status: 'idle',
    pid: null,
    appiumPid: null,
    sessionId: '',
    server: '',
    port: null,
    cycles: 0,
    phase: '',
    lastResult: null,
    lastError: '',
    lastObservation: null,
    device: {},
    agentMode: '',
    agentModeLabel: '',
    progressDetail: '',
    progress: {}
  });
}

function writeState(paths, state) {
  writeJson(paths.agentStatePath, {
    ...state,
    updatedAt: nowIso()
  });
}

function isProcessAlive(pid) {
  if (!pid) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return false;
  }
}

function runNodeJson(scriptPath, extraArgs, options = {}) {
  const timeoutMs = toNumber(options.timeoutMs, 30000);
  const result = spawnSync(process.execPath, [scriptPath, ...extraArgs], {
    cwd: options.cwd || process.cwd(),
    env: {
      ...process.env,
      ...(options.env || {})
    },
    encoding: 'utf-8',
    timeout: timeoutMs,
    killSignal: 'SIGKILL'
  });

  if (result.error && result.error.code === 'ETIMEDOUT') {
    throw new Error(`Timed out after ${timeoutMs}ms: ${path.basename(scriptPath)} ${extraArgs.join(' ')}`);
  }

  if (result.status !== 0) {
    const output = (result.stderr || result.stdout || '').trim();
    throw new Error(output || `Command failed: ${scriptPath}`);
  }

  const output = (result.stdout || '').trim();
  return output ? JSON.parse(output) : null;
}

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  const text = await response.text();
  if (!response.ok) {
    throw new Error(text || `HTTP ${response.status}`);
  }
  return text ? JSON.parse(text) : {};
}

async function appiumReady(server) {
  try {
    const status = await fetchJson(`${server}/status`);
    return Boolean(status.value?.ready);
  } catch (error) {
    return false;
  }
}

async function waitForAppium(server, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (await appiumReady(server)) {
      return true;
    }
    await sleep(1000);
  }
  return false;
}

function parseUdidFromLine(line) {
  const match = String(line || '').match(/\b([0-9A-F]{8}(?:-[0-9A-F]{4,})+|[0-9A-F]{20,})\b/i);
  return match ? match[1] : '';
}

function detectFromXctraceOutput(output) {
  const lines = String(output || '').split('\n');
  let inDevicesSection = false;
  for (const line of lines) {
    const trimmed = line.trim();
    if (/^== Devices ==$/i.test(trimmed)) {
      inDevicesSection = true;
      continue;
    }
    if (/^== .* ==$/i.test(trimmed)) {
      inDevicesSection = false;
      continue;
    }
    if (!inDevicesSection) continue;
    if (!/iphone/i.test(line) || /simulator/i.test(line)) continue;
    const udid = parseUdidFromLine(line);
    if (udid) return udid;
  }
  return '';
}

function detectFromGenericDeviceList(output) {
  const lines = String(output || '').split('\n');
  for (const line of lines) {
    if (!/iphone/i.test(line) || /simulator/i.test(line)) continue;
    const udid = parseUdidFromLine(line);
    if (udid) return udid;
  }
  return '';
}

function detectConnectedIphoneUdid() {
  const probes = [
    {
      name: 'xctrace',
      cmd: 'DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcrun xctrace list devices',
      parse: detectFromXctraceOutput
    },
    {
      name: 'devicectl',
      cmd: 'DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcrun devicectl list devices',
      parse: detectFromGenericDeviceList
    },
    {
      name: 'idevice_id',
      cmd: 'idevice_id -l',
      parse: (output) => {
        const first = String(output || '')
          .split('\n')
          .map((line) => line.trim())
          .find(Boolean);
        return parseUdidFromLine(first);
      }
    }
  ];

  const errors = [];
  for (const probe of probes) {
    const result = spawnSync('/bin/zsh', ['-lc', probe.cmd], { encoding: 'utf-8' });
    if (result.status !== 0) {
      const reason = (result.stderr || result.stdout || '').trim() || `exit ${result.status}`;
      errors.push(`${probe.name}: ${reason}`);
      continue;
    }

    const udid = probe.parse(result.stdout || '');
    if (udid) return udid;
    errors.push(`${probe.name}: no physical iPhone detected`);
  }

  throw new Error(
    'No connected physical iPhone detected. Checked xctrace/devicectl/idevice_id. ' +
      `Details: ${errors.slice(0, 3).join(' | ')}`
  );
}

function buildRuntimeOptions(workspace) {
  const config = workspace.config;
  const agentMode = normalizeAgentMode(getArg('--agent-mode', config.automation?.agentMode || 'full_access'));
  const modePolicy = buildAgentModePolicy(agentMode, config.automation?.activeTabs || []);
  const runtimeWorkspaceDir = resolveAutomationWorkspace();
  const appiumPort = toNumber(getArg('--port', '4725'), 4725);
  const server = getArg('--server', `http://127.0.0.1:${appiumPort}`);
  const sampleMatches = toNumber(
    getArg('--sample-matches', String(config.automation?.sampleMatches || 8)),
    8
  );
  const profileScrollSteps = toNumber(
    getArg('--profile-scroll-steps', String(config.automation?.profileScrollSteps || 3)),
    3
  );
  const batchSize = toNumber(getArg('--batch-size', '1'), 1);
  const trustMode = getArg('--trust-mode', config.automation?.trustMode || 'queue');
  const sleepMs = toNumber(getArg('--sleep-ms', String(config.automation?.runForeverSleepMs || 4000)), 4000);
  const tasteRefreshEveryCycles = toNumber(
    getArg('--taste-refresh-every-cycles', String(config.automation?.tasteRefreshEveryCycles || 5)),
    5
  );
  const udid = getArg('--udid', config.ios?.udid || '');
  const openAiApiKey = resolveOpenAiApiKey(config);
  const observeBeforeTakeover = !hasFlag('--skip-observe') && toBoolean(
    getArg(
      '--observe-before-takeover',
      String(config.automation?.observeBeforeTakeover ?? true)
    ),
    true
  );
  const observeWarmupSeconds = Math.max(
    0,
    toNumber(
      getArg(
        '--observe-seconds',
        String(config.automation?.observeWarmupSeconds ?? 90)
      ),
      90
    )
  );
  const observeSnapshotIntervalMs = Math.max(
    500,
    toNumber(
      getArg(
        '--observe-interval-ms',
        String(config.automation?.observeSnapshotIntervalMs ?? 1500)
      ),
      1500
    )
  );

  return {
    agentMode: modePolicy.agentMode,
    agentModeLabel: modePolicy.label,
    agentModeTabs: modePolicy.activeTabs,
    server,
    appiumPort,
    workspaceDir: runtimeWorkspaceDir,
    appiumBasePath: '/',
    bundleId: getArg('--bundle-id', config.ios?.bundleId || 'co.hinge.mobile.ios'),
    deviceName: getArg('--device-name', config.ios?.deviceName || 'iPhone'),
    udid: udid || detectConnectedIphoneUdid(),
    sampleMatches,
    profileScrollSteps,
    batchSize,
    trustMode,
    sleepMs,
    tasteRefreshEveryCycles,
    disableTasteRefresh: hasFlag('--skip-taste-refresh') || sampleMatches <= 0,
    observeBeforeTakeover,
    observeWarmupSeconds,
    observeSnapshotIntervalMs,
    openAiApiKey,
    platformVersion: getArg('--platform-version', config.ios?.platformVersion || ''),
    wdaLocalPort: toNumber(getArg('--wda-local-port', '8102'), 8102),
    mjpegServerPort: toNumber(getArg('--mjpeg-server-port', '9102'), 9102)
  };
}

function startDetachedAppium(paths, options) {
  rotateLogIfLarge(paths.appiumLogPath);
  const logFd = fs.openSync(paths.appiumLogPath, 'a');
  const child = spawn(
    '/bin/zsh',
    [
      '-lc',
      `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer npx appium --base-path ${options.appiumBasePath} -p ${options.appiumPort} --log-level warn`
    ],
    {
      cwd: options.workspaceDir,
      detached: true,
      stdio: ['ignore', logFd, logFd]
    }
  );
  child.unref();
  return child.pid;
}

async function ensureAppium(paths, state, options) {
  if (await appiumReady(options.server)) {
    return state.appiumPid || null;
  }

  const pid = startDetachedAppium(paths, options);
  const ready = await waitForAppium(options.server, 30000);
  if (!ready) {
    throw new Error(`Appium did not become ready on ${options.server}`);
  }
  return pid;
}

function createSession(options) {
  const argsForSession = [
    '--server',
    options.server,
    '--create-session',
    '--device-name',
    options.deviceName,
    '--udid',
    options.udid,
    '--bundle-id',
    options.bundleId,
    '--wda-local-port',
    String(options.wdaLocalPort),
    '--mjpeg-server-port',
    String(options.mjpegServerPort),
    '--new-command-timeout',
    '600',
    '--wda-launch-timeout',
    '180000',
    '--wda-startup-retries',
    '2',
    '--wda-startup-retry-interval',
    '10000'
  ];

  if (options.platformVersion) {
    argsForSession.push('--platform-version', options.platformVersion);
  }

  return runNodeJson(appiumScript, argsForSession, { timeoutMs: 240000 });
}

function sessionIdFromCreateResponse(payload) {
  return payload?.value?.sessionId || payload?.sessionId || '';
}

async function waitForSessionReady(server, sessionId, timeoutMs = 12000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const response = await fetchJson(`${server}/session/${sessionId}/source`);
      if (response?.value) {
        return true;
      }
    } catch (error) {
      // WebDriverAgent can reject commands briefly right after session creation.
    }
    await sleep(1000);
  }
  return false;
}

function sessionHealthy(server, sessionId) {
  if (!sessionId) return false;
  try {
    runNodeJson(hingeScript, ['--server', server, '--session-id', sessionId, '--snapshot'], { timeoutMs: 15000 });
    return true;
  } catch (error) {
    return false;
  }
}

function readSessionSnapshot(server, sessionId) {
  return runNodeJson(hingeScript, ['--server', server, '--session-id', sessionId, '--snapshot'], { timeoutMs: 15000 });
}

function canRefreshTasteFromSnapshot(snapshot) {
  return ['chat-list', 'chat-thread', 'thread-profile'].includes(snapshot?.screenType || '');
}

function pushUniqueLimited(list, value, limit = 16) {
  const normalized = String(value || '').trim();
  if (!normalized) return;
  if (list.includes(normalized)) return;
  list.push(normalized);
  if (list.length > limit) {
    list.splice(0, list.length - limit);
  }
}

function incrementCount(map, key, weight = 1) {
  const normalized = String(key || '').trim();
  if (!normalized) return;
  map.set(normalized, (map.get(normalized) || 0) + weight);
}

function topCountEntries(map, limit = 10) {
  return [...map.entries()]
    .sort((left, right) => right[1] - left[1])
    .slice(0, limit)
    .map(([value, weight]) => ({ value, weight }));
}

function extractProfileSignalTexts(snapshot) {
  return [
    ...((snapshot?.prompts || []).flatMap((prompt) => [prompt.prompt, prompt.answer])),
    ...(snapshot?.statusBadges || []),
    ...(snapshot?.filters || [])
  ]
    .map((value) => String(value || '').trim())
    .filter(Boolean);
}

function extractProfileSignalPhrases(snapshot) {
  return unique(
    extractProfileSignalTexts(snapshot)
      .map((value) => briefPhrase(value, 7))
      .filter(Boolean)
  ).slice(0, 14);
}

function learnFromSnapshot(snapshot, tokenCounts, phraseCounts) {
  const tokens = unique(extractProfileSignalTexts(snapshot).flatMap((value) => tokenize(value))).slice(0, 40);
  const phrases = extractProfileSignalPhrases(snapshot);
  tokens.forEach((token) => incrementCount(tokenCounts, token, 1));
  phrases.forEach((phrase) => incrementCount(phraseCounts, phrase, 1));
}

function mergeObservationIntoConfig(workspace, observationSession) {
  workspace.config.user = workspace.config.user || {};
  workspace.config.automation = workspace.config.automation || {};
  const user = workspace.config.user;
  const learnedHints = observationSession.learnedHints || [];
  const styleSamples = unique([
    ...(observationSession.typedLikeComments || []),
    ...(observationSession.typedReplySamples || [])
  ]);

  user.observedInterestHints = unique([...(user.observedInterestHints || []), ...learnedHints]).slice(0, 24);
  user.likesToLeadWith = unique([...(user.likesToLeadWith || []), ...learnedHints]).slice(0, 24);
  user.chatStyleExamples = unique([...(user.chatStyleExamples || []), ...styleSamples]).slice(0, 24);
  user.observationSummary = observationSession.summary || user.observationSummary || '';
  user.lastObservedAt = observationSession.endedAt || nowIso();
  workspace.config.automation.lastObserveWarmupAt = observationSession.endedAt || nowIso();

  writeJson(workspace.paths.configPath, workspace.config);
}

async function observeUserWarmup(workspace, options, state, setProgress) {
  const durationMs = Math.max(0, Math.round(options.observeWarmupSeconds * 1000));
  const intervalMs = Math.max(500, toNumber(options.observeSnapshotIntervalMs, 1500));
  if (durationMs <= 0) {
    return null;
  }

  const startedAt = nowIso();
  const deadline = Date.now() + durationMs;
  let previousSnapshot = null;

  const tabCounts = new Map();
  const likedTokenCounts = new Map();
  const likedPhraseCounts = new Map();
  const passedTokenCounts = new Map();
  const passedPhraseCounts = new Map();
  const typedLikeComments = [];
  const typedReplySamples = [];
  const inferredLikes = [];
  const inferredPasses = [];

  let sampleCount = 0;
  let activeComposerProfileName = '';
  const progressTick = Math.max(1, Math.round(5000 / intervalMs));

  while (Date.now() < deadline) {
    let snapshot;
    try {
      snapshot = readSessionSnapshot(options.server, state.sessionId);
    } catch (error) {
      await sleep(intervalMs);
      continue;
    }

    sampleCount += 1;
    if (snapshot.currentTab) {
      incrementCount(tabCounts, snapshot.currentTab, 1);
    }

    if (snapshot.screenType === 'like-composer') {
      const typedComment = oneLiner(snapshot.composer?.commentText || '', 14);
      if (typedComment && !/^add a comment$/i.test(typedComment)) {
        pushUniqueLimited(typedLikeComments, typedComment, 14);
      }
      if (snapshot.currentProfile?.name) {
        activeComposerProfileName = String(snapshot.currentProfile.name).trim().toLowerCase();
      }
    }

    if (snapshot.screenType === 'chat-thread') {
      const yourMessage = (snapshot.thread?.messages || [])
        .filter((message) => message.side === 'you' && !message.isSystem)
        .map((message) => oneLiner(message.text, 14))
        .find(Boolean);
      if (yourMessage) {
        pushUniqueLimited(typedReplySamples, yourMessage, 14);
      }
    }

    if (previousSnapshot) {
      const previousName = String(previousSnapshot.currentProfile?.name || '').trim();
      const currentName = String(snapshot.currentProfile?.name || '').trim();

      const profileAdvanced =
        previousSnapshot.screenType === 'profile' &&
        snapshot.screenType === 'profile' &&
        previousName &&
        currentName &&
        previousName !== currentName;

      const composerSent =
        previousSnapshot.screenType === 'like-composer' &&
        snapshot.screenType === 'profile' &&
        previousName &&
        currentName &&
        previousName !== currentName;

      if (profileAdvanced || composerSent) {
        const inferredLike =
          composerSent ||
          (activeComposerProfileName && activeComposerProfileName === previousName.toLowerCase());

        if (inferredLike) {
          pushUniqueLimited(inferredLikes, previousName, 24);
          learnFromSnapshot(previousSnapshot, likedTokenCounts, likedPhraseCounts);
        } else {
          pushUniqueLimited(inferredPasses, previousName, 24);
          learnFromSnapshot(previousSnapshot, passedTokenCounts, passedPhraseCounts);
        }
        activeComposerProfileName = '';
      }
    }

    previousSnapshot = snapshot;

    if (sampleCount === 1 || sampleCount % progressTick === 0) {
      const remainingSeconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
      setProgress(`Observing your actions (${remainingSeconds}s left)`);
    }

    await sleep(intervalMs);
  }

  const topLikedTokens = topCountEntries(likedTokenCounts, 12);
  const topLikedPhrases = topCountEntries(likedPhraseCounts, 8);
  const topPassedTokens = topCountEntries(passedTokenCounts, 10);
  const topPassedPhrases = topCountEntries(passedPhraseCounts, 6);
  const passedWords = new Set(topPassedTokens.map((entry) => entry.value));
  const passedPhrases = new Set(topPassedPhrases.map((entry) => entry.value));
  const learnedHints = unique([
    ...topLikedPhrases.map((entry) => entry.value).filter((value) => !passedPhrases.has(value)),
    ...topLikedTokens.map((entry) => entry.value).filter((value) => !passedWords.has(value))
  ]).slice(0, 16);
  const topTabs = topCountEntries(tabCounts, 6);
  const endedAt = nowIso();
  const summary = [
    `Observed ${Math.round(durationMs / 1000)}s of manual use.`,
    `Inferred likes: ${inferredLikes.length}.`,
    `Inferred passes: ${inferredPasses.length}.`,
    `Style samples: ${typedLikeComments.length + typedReplySamples.length}.`,
    learnedHints.length ? `Learned hints: ${learnedHints.slice(0, 5).join(', ')}.` : ''
  ]
    .filter(Boolean)
    .join(' ');

  const session = {
    startedAt,
    endedAt,
    durationSeconds: Math.round(durationMs / 1000),
    sampleCount,
    inferredLikes,
    inferredPasses,
    typedLikeComments,
    typedReplySamples,
    topTabs,
    topLikedTokens,
    topLikedPhrases,
    topPassedTokens,
    topPassedPhrases,
    learnedHints,
    summary
  };

  const observationLog = readObservationLog(workspace.paths);
  observationLog.sessions.unshift(session);
  observationLog.sessions = observationLog.sessions.slice(0, 24);
  writeObservationLog(workspace.paths, observationLog);
  mergeObservationIntoConfig(workspace, session);

  return session;
}

async function ensureSession(state, options) {
  if (sessionHealthy(options.server, state.sessionId)) {
    return state.sessionId;
  }

  const created = createSession(options);
  const sessionId = sessionIdFromCreateResponse(created);
  if (!sessionId) {
    throw new Error('Session creation succeeded without a session id');
  }

  const ready = await waitForSessionReady(options.server, sessionId);
  if (!ready) {
    throw new Error(`Session ${sessionId} did not become ready in time`);
  }

  runNodeJson(hingeScript, ['--server', options.server, '--session-id', sessionId, '--activate'], { timeoutMs: 30000 });
  return sessionId;
}

function runAutopilotBatch(workspace, options, sessionId, refreshTaste) {
  const autopilotArgs = [
    '--server',
    options.server,
    '--session-id',
    sessionId,
    '--dir',
    workspace.paths.root,
    '--sample-matches',
    String(options.sampleMatches),
    '--profile-scroll-steps',
    String(options.profileScrollSteps),
    '--agent-mode',
    options.agentMode,
    '--max-profiles',
    String(options.batchSize),
    '--trust-mode',
    options.trustMode
  ];

  if (!refreshTaste) {
    autopilotArgs.push('--skip-taste-refresh');
  }

  const env = options.openAiApiKey ? { OPENAI_API_KEY: options.openAiApiKey } : {};
  return runNodeJson(autopilotScript, autopilotArgs, { timeoutMs: 90000, env });
}

function shouldPause(result, trustMode) {
  if (!result) return false;
  if (result.mode === 'staged') return true;
  if (trustMode === 'queue' && result.mode === 'review') return true;
  return false;
}

async function runLoop(workspace, options) {
  const state = readState(workspace.paths);
  state.startedAt = state.startedAt || nowIso();
  state.pid = process.pid;
  state.server = options.server;
  state.port = options.appiumPort;
  state.device = {
    udid: options.udid,
    deviceName: options.deviceName,
    bundleId: options.bundleId
  };
  state.status = 'starting';
  state.agentMode = options.agentMode;
  state.agentModeLabel = options.agentModeLabel;
  writeState(workspace.paths, state);

  let stopping = false;
  let observationCompleted = false;

  const setProgress = (detail, extra = {}) => {
    state.progressDetail = detail || '';
    state.progress = {
      ...(state.progress || {}),
      ...extra,
      detail: detail || '',
      updatedAt: nowIso()
    };
    if (extra.phase) {
      state.phase = extra.phase;
    }
    writeState(workspace.paths, state);
  };

  process.on('SIGINT', () => {
    stopping = true;
  });
  process.on('SIGTERM', () => {
    stopping = true;
  });

  while (!stopping) {
    try {
      state.status = 'recovering';
      writeState(workspace.paths, state);

      state.appiumPid = await ensureAppium(workspace.paths, state, options);
      state.sessionId = await ensureSession(state, options);

      if (!observationCompleted && options.observeBeforeTakeover && options.observeWarmupSeconds > 0) {
        state.status = 'observing';
        state.phase = 'observing-user';
        setProgress(`Observing your actions (${Math.round(options.observeWarmupSeconds)}s planned)`, {
          phase: 'observing-user'
        });
        try {
          const observation = await observeUserWarmup(
            workspace,
            options,
            state,
            (detail) => setProgress(detail, { phase: 'observing-user' })
          );
          state.lastObservation = observation;
          state.lastError = '';
        } catch (error) {
          state.lastError = `Observation warmup failed: ${error.message || String(error)}`;
        } finally {
          observationCompleted = true;
          state.status = 'running';
          setProgress('Observation complete, taking over.', { phase: 'browsing' });
        }
      }

      const sessionSnapshot = readSessionSnapshot(options.server, state.sessionId);
      const refreshTaste =
        !options.disableTasteRefresh &&
        canRefreshTasteFromSnapshot(sessionSnapshot) &&
        (state.cycles === 0 || state.cycles % Math.max(options.tasteRefreshEveryCycles, 1) === 0);
      state.status = 'running';
      state.phase = refreshTaste ? 'refreshing-taste' : 'browsing';
      writeState(workspace.paths, state);

      let result;
      try {
        result = runAutopilotBatch(workspace, options, state.sessionId, refreshTaste);
      } catch (error) {
        if (refreshTaste && /Unable to reach chat list from screen profile/i.test(error.message)) {
          state.lastError = 'Taste refresh skipped because Hinge stayed on Discover.';
          state.phase = 'browsing';
          writeState(workspace.paths, state);
          result = runAutopilotBatch(workspace, options, state.sessionId, false);
        } else {
          throw error;
        }
      }
      state.lastResult = result;
      state.lastError = '';
      state.cycles = (state.cycles || 0) + 1;
      state.phase = 'idle';

      if (shouldPause(result, options.trustMode)) {
        state.status = result.mode;
        writeState(workspace.paths, state);
        return;
      }

      writeState(workspace.paths, state);
      await sleep(options.sleepMs);
    } catch (error) {
      state.lastError = error.message;
      state.status = 'recovering';
      state.phase = 'recovering';
      if (/Unable to reach Appium|invalid session|socket hang up|session.*not found/i.test(error.message)) {
        state.sessionId = '';
      }
      writeState(workspace.paths, state);
      await sleep(Math.max(options.sleepMs, 3000));
    }
  }

  state.status = 'stopped';
  writeState(workspace.paths, state);
}

function launchDetached(workspace) {
  rotateLogIfLarge(workspace.paths.agentLogPath);
  const logFd = fs.openSync(workspace.paths.agentLogPath, 'a');
  const child = spawn(process.execPath, [__filename, '--run-daemon', '--dir', workspace.paths.root, ...args], {
    cwd: process.cwd(),
    detached: true,
    stdio: ['ignore', logFd, logFd]
  });
  child.unref();
  return child.pid;
}

function removeOption(argv, flag, expectsValue = false) {
  const filtered = [];
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === flag) {
      if (expectsValue) {
        index += 1;
      }
      continue;
    }
    filtered.push(argv[index]);
  }
  return filtered;
}

function canPromptAgentMode() {
  return Boolean(process.stdin?.isTTY && process.stdout?.isTTY);
}

async function promptForAgentMode(defaultMode) {
  const fallback = normalizeAgentMode(defaultMode || 'full_access');
  const fallbackPolicy = buildAgentModePolicy(fallback);
  console.log('Select Hinge agent mode:');
  AGENT_MODE_DEFINITIONS.forEach((mode, index) => {
    console.log(`${index + 1}. ${mode.label} (${mode.id})`);
    console.log(`   ${mode.description}`);
  });
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  try {
    const answer = await rl.question(`Choice [1-3] (default ${fallbackPolicy.label}): `);
    const selected = normalizeAgentMode(answer || fallback);
    const policy = buildAgentModePolicy(selected);
    console.log(`Using mode: ${policy.label} (${policy.agentMode})`);
    return policy.agentMode;
  } finally {
    rl.close();
  }
}

function persistAgentMode(workspace, mode) {
  const selectedMode = normalizeAgentMode(mode);
  const config = readJson(workspace.paths.configPath, defaultConfig());
  config.automation = config.automation || {};
  config.automation.agentMode = selectedMode;
  writeJson(workspace.paths.configPath, config);
  workspace.config = config;
  return selectedMode;
}

function stopAgent(workspace) {
  const state = readState(workspace.paths);
  if (isProcessAlive(state.pid)) {
    process.kill(state.pid, 'SIGTERM');
  }
  if (state.appiumPid && isProcessAlive(state.appiumPid)) {
    process.kill(state.appiumPid, 'SIGTERM');
  }
  writeState(workspace.paths, {
    ...state,
    status: 'stopped',
    phase: 'stopped',
    pid: null,
    appiumPid: null,
    sessionId: ''
  });
  return readState(workspace.paths);
}

async function main() {
  const dirPath = getArg('--dir', defaultDataDir);
  const workspace = loadWorkspace(dirPath);

  if (hasFlag('--status')) {
    console.log(JSON.stringify(readState(workspace.paths), null, 2));
    return;
  }

  if (hasFlag('--stop')) {
    console.log(JSON.stringify(stopAgent(workspace), null, 2));
    return;
  }

  if (hasFlag('--launch')) {
    const existing = readState(workspace.paths);
    if (isProcessAlive(existing.pid)) {
      console.log(JSON.stringify(existing, null, 2));
      return;
    }
    const explicitMode = getArg('--agent-mode', '');
    let selectedMode = normalizeAgentMode(explicitMode || workspace.config.automation?.agentMode || 'full_access');
    const shouldPromptMode = !explicitMode && !hasFlag('--skip-agent-mode-prompt') && canPromptAgentMode();
    if (shouldPromptMode) {
      selectedMode = await promptForAgentMode(selectedMode);
    }
    selectedMode = persistAgentMode(workspace, selectedMode);
    const selectedPolicy = buildAgentModePolicy(selectedMode, workspace.config.automation?.activeTabs || []);
    let launchArgs = removeOption(args, '--launch');
    launchArgs = removeOption(launchArgs, '--run-daemon');
    launchArgs = removeOption(launchArgs, '--dir', true);
    launchArgs = removeOption(launchArgs, '--agent-mode', true);
    launchArgs = removeOption(launchArgs, '--skip-agent-mode-prompt');
    launchArgs.push('--agent-mode', selectedMode);
    args.length = 0;
    args.push(...launchArgs);
    const pid = launchDetached(workspace);
    const state = {
      ...readState(workspace.paths),
      status: 'starting',
      pid,
      startedAt: nowIso(),
      agentMode: selectedMode,
      agentModeLabel: selectedPolicy.label
    };
    writeState(workspace.paths, state);
    console.log(JSON.stringify(state, null, 2));
    return;
  }

  const options = buildRuntimeOptions(workspace);
  await runLoop(workspace, options);
}

main().catch(error => {
  console.error(error.message);
  process.exit(1);
});

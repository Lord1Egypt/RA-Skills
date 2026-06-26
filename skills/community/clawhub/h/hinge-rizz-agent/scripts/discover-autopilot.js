#!/usr/bin/env node

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const {
  buildAgentModePolicy,
  appendActivityEntry,
  defaultActivityLog,
  defaultConfig,
  defaultQueue,
  deriveProfileId,
  ensureDir,
  normalizeAgentMode,
  normalizeFit,
  nowIso,
  readJson,
  renderActivityMarkdown,
  renderMarkdown,
  resolvePaths,
  slugify,
  upsertEntry,
  writeJson
} = require('./session-utils');

const args = process.argv.slice(2);
const rootDir = path.resolve(__dirname, '..');
const hingeIosScript = path.join(rootDir, 'scripts', 'hinge-ios.js');
const hingeAiScript = path.join(rootDir, 'scripts', 'hinge-ai.js');

const STOP_WORDS = new Set([
  'about',
  'after',
  'again',
  'all',
  'and',
  'are',
  'back',
  'been',
  'from',
  'have',
  'hers',
  'into',
  'its',
  'just',
  'like',
  'more',
  'once',
  'only',
  'ours',
  'over',
  'same',
  'some',
  'than',
  'that',
  'them',
  'then',
  'they',
  'this',
  'very',
  'want',
  'what',
  'when',
  'with',
  'your',
  'youre'
]);

function hasFlag(name) {
  return args.includes(name);
}

function getArg(name, fallback = '') {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] || fallback;
}

function getRequiredArg(name) {
  const value = getArg(name);
  if (!value) {
    throw new Error(`Missing ${name}`);
  }
  return value;
}

function toNumber(value, fallback) {
  if (value === null || value === undefined) return fallback;
  if (typeof value === 'string' && value.trim() === '') return fallback;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function defaultTasteModel() {
  return {
    createdAt: nowIso(),
    updatedAt: nowIso(),
    sources: [],
    signals: [],
    promptExamples: []
  };
}

function defaultThreadState() {
  return {
    updatedAt: nowIso(),
    threads: {}
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

  const inlineKeyCandidates = [
    config?.ai?.openaiApiKey,
    config?.ai?.openAiApiKey,
    config?.ai?.apiKey
  ];
  for (const candidate of inlineKeyCandidates) {
    if (typeof candidate === 'string' && candidate.trim().startsWith('sk-')) {
      return candidate.trim();
    }
  }

  return readOpenClawOpenAiApiKey();
}

function loadWorkspace(dirPath) {
  const paths = resolvePaths(dirPath);
  ensureDir(paths.root);
  ensureDir(paths.activityRoot);
  ensureDir(paths.activityDayRoot);
  ensureDir(paths.activityImagesDir);
  const config = readJson(paths.configPath, defaultConfig());
  const openAiApiKey = resolveOpenAiApiKey(config);
  return {
    paths,
    config,
    queue: readJson(paths.queuePath, defaultQueue()),
    tasteModel: readJson(paths.tasteModelPath, defaultTasteModel()),
    threadState: readJson(paths.threadStatePath, defaultThreadState()),
    activityLog: readJson(paths.activityJsonPath, defaultActivityLog()),
    runtimeEnv: openAiApiKey ? { OPENAI_API_KEY: openAiApiKey } : {}
  };
}

function runNodeScript(scriptPath, extraArgs, options = {}) {
  const timeoutMs = toNumber(options.timeoutMs, 15000);
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
    const errorOutput = (result.stderr || result.stdout || '').trim();
    throw new Error(errorOutput || `Command failed: ${scriptPath}`);
  }

  return (result.stdout || '').trim();
}

function runHinge(extraArgs) {
  const sessionId = getRequiredArg('--session-id');
  const server = getArg('--server', process.env.APPIUM_SERVER || 'http://127.0.0.1:4725');
  const timeoutMs =
    extraArgs.some((arg) =>
      [
        '--send-like-with-comment',
        '--send-like',
        '--send-rose-with-comment',
        '--send-reply',
        '--complete-open-interest',
        '--open-interest-composer',
        '--replace-open-interest-comment'
      ].includes(arg)
    )
      ? 30000
      : 15000;
  const output = runNodeScript(
    hingeIosScript,
    ['--session-id', sessionId, '--server', server, ...extraArgs],
    { env: process.env, timeoutMs }
  );
  return output ? JSON.parse(output) : null;
}

function runAi(mode, context, workspaceRoot, screenshotPath, extraArgs = [], runtimeEnv = {}) {
  const commandArgs = [
    '--mode',
    mode,
    '--dir',
    workspaceRoot,
    '--context-json',
    JSON.stringify(context)
  ];

  if (screenshotPath) {
    commandArgs.push('--screenshot-file', screenshotPath);
  }

  commandArgs.push(...extraArgs);

  const output = runNodeScript(hingeAiScript, commandArgs, { env: runtimeEnv, timeoutMs: 25000 });
  return output ? JSON.parse(output) : null;
}

function updateAgentProgress(workspace, detail, extra = {}) {
  const current = readJson(workspace.paths.agentStatePath, {});
  writeJson(workspace.paths.agentStatePath, {
    ...current,
    phase: extra.phase || current.phase || 'browsing',
    progressDetail: detail,
    progress: {
      ...(current.progress || {}),
      ...extra,
      detail,
      updatedAt: nowIso()
    },
    updatedAt: nowIso()
  });
}

function tempScreenshotPath(prefix) {
  return path.join(os.tmpdir(), `${prefix}-${Date.now()}.png`);
}

function captureScreenshot(prefix) {
  const screenshotPath = tempScreenshotPath(prefix);
  runHinge(['--screenshot', '--out', screenshotPath]);
  return screenshotPath;
}

function tokenize(text) {
  return String(text || '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .map(token => token.trim())
    .filter(token => token.length >= 3 && !STOP_WORDS.has(token));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function uniquePrompts(prompts) {
  const seen = new Set();
  const result = [];
  for (const prompt of prompts || []) {
    const key = [prompt.label || '', prompt.prompt || '', prompt.answer || ''].join('::');
    if (!key.trim() || seen.has(key)) continue;
    seen.add(key);
    result.push(prompt);
  }
  return result;
}

function mergeProfileSnapshots(snapshots) {
  const validSnapshots = (snapshots || []).filter(Boolean);
  const first = validSnapshots[0] || {};
  const last = validSnapshots[validSnapshots.length - 1] || first;

  return {
    ...first,
    currentProfile: {
      ...(first.currentProfile || {}),
      ...(last.currentProfile || {}),
      name: first.currentProfile?.name || last.currentProfile?.name || ''
    },
    prompts: uniquePrompts(validSnapshots.flatMap(snapshot => snapshot.prompts || [])),
    likeTargets: unique(validSnapshots.flatMap(snapshot => snapshot.likeTargets || [])),
    statusBadges: unique(validSnapshots.flatMap(snapshot => snapshot.statusBadges || [])),
    filters: unique(validSnapshots.flatMap(snapshot => snapshot.filters || [])),
    inspectedViews: validSnapshots.length
  };
}

function extractSignalTexts(snapshot) {
  const prompts = snapshot.prompts || [];
  const promptTexts = prompts.flatMap(prompt => [prompt.prompt, prompt.answer].filter(Boolean));
  return unique([
    ...(snapshot.statusBadges || []),
    ...(snapshot.filters || []),
    ...promptTexts
  ]);
}

function buildSignalWeights(examples) {
  const totalCounts = new Map();
  const documentCounts = new Map();

  for (const example of examples) {
    const exampleTokens = tokenize((example.signalTexts || []).join(' '));
    const tokenSet = new Set(exampleTokens);

    for (const token of exampleTokens) {
      totalCounts.set(token, (totalCounts.get(token) || 0) + 1);
    }

    for (const token of tokenSet) {
      documentCounts.set(token, (documentCounts.get(token) || 0) + 1);
    }
  }

  return [...documentCounts.entries()]
    .map(([token, docCount]) => ({
      token,
      weight: docCount * 3 + (totalCounts.get(token) || 0)
    }))
    .sort((left, right) => right.weight - left.weight)
    .slice(0, 60);
}

function mergeTasteModel(tasteModel, examples) {
  const sources = examples.map(example => ({
    matchName: example.matchName,
    prompts: example.prompts,
    signalTexts: example.signalTexts
  }));

  return {
    createdAt: tasteModel.createdAt || nowIso(),
    updatedAt: nowIso(),
    sources,
    signals: buildSignalWeights(examples),
    promptExamples: examples.slice(0, 12).map(example => ({
      matchName: example.matchName,
      prompts: example.prompts
    }))
  };
}

function saveWorkspace(paths, queue, tasteModel, threadState, activityLog) {
  writeJson(paths.queuePath, queue);
  writeJson(paths.tasteModelPath, tasteModel);
  if (threadState) {
    writeJson(paths.threadStatePath, threadState);
  }
  if (activityLog) {
    writeJson(paths.activityJsonPath, activityLog);
    fs.writeFileSync(paths.activityMarkdownPath, renderActivityMarkdown(activityLog));
  }
  fs.writeFileSync(paths.markdownPath, renderMarkdown(queue));
}

function writeStagedMessage(paths, message) {
  if (!message) return;
  fs.writeFileSync(paths.stagedMessagePath, `${message}\n`);
}

function classifyLikeTargets(snapshot) {
  const likeTargets = snapshot?.likeTargets || [];
  return {
    photoTargets: likeTargets.filter((label) => /photo|video/i.test(label)),
    answerTargets: likeTargets.filter((label) => /answer/i.test(label)),
    otherTargets: likeTargets.filter((label) => !/photo|video|answer/i.test(label))
  };
}

function stablePercentSeed(value) {
  const input = String(value || '');
  let hash = 0;
  for (let index = 0; index < input.length; index += 1) {
    hash = (hash * 31 + input.charCodeAt(index)) % 2147483647;
  }
  return Math.abs(hash) % 100;
}

function stableHashSeed(value) {
  const input = String(value || '');
  let hash = 0;
  for (let index = 0; index < input.length; index += 1) {
    hash = (hash * 33 + input.charCodeAt(index)) % 2147483647;
  }
  return Math.abs(hash);
}

function targetPreferenceSeed(snapshot) {
  const promptSeed = (snapshot?.prompts || [])
    .slice(0, 2)
    .map((prompt) => `${prompt.prompt || ''}:${prompt.answer || ''}`)
    .join('|');
  return `${snapshot?.currentProfile?.name || ''}|${promptSeed}`;
}

function pickRotatedTarget(snapshot, targets, bucket, rotationStep = 0) {
  const items = (targets || []).filter(Boolean);
  if (!items.length) return '';
  if (items.length === 1) return items[0];
  const seed = `${targetPreferenceSeed(snapshot)}|${bucket}|${rotationStep}`;
  const index = stableHashSeed(seed) % items.length;
  return items[index];
}

function chooseWeightedLikeTarget(snapshot, photoRatio = 0.7, rotationStep = 0) {
  if (!snapshot) return '';
  const groups = classifyLikeTargets(snapshot);
  const threshold = Math.max(0, Math.min(100, Math.round(photoRatio * 100)));
  const preferPhoto = stablePercentSeed(`${targetPreferenceSeed(snapshot)}|${rotationStep}`) < threshold;

  if (preferPhoto && groups.photoTargets.length) {
    return pickRotatedTarget(snapshot, groups.photoTargets, 'photo', rotationStep);
  }
  if (!preferPhoto && groups.answerTargets.length) {
    return pickRotatedTarget(snapshot, groups.answerTargets, 'answer', rotationStep);
  }
  return (
    pickRotatedTarget(snapshot, groups.photoTargets, 'photo', rotationStep) ||
    pickRotatedTarget(snapshot, groups.answerTargets, 'answer', rotationStep) ||
    pickRotatedTarget(snapshot, groups.otherTargets, 'other', rotationStep) ||
    pickRotatedTarget(snapshot, snapshot.likeTargets || [], 'any', rotationStep) ||
    ''
  );
}

function chooseVisibleLikeTarget(snapshot, photoRatio = 0.7, rotationStep = 0) {
  return chooseWeightedLikeTarget(snapshot, photoRatio, rotationStep);
}

function choosePromptTarget(snapshot, photoRatio = 0.7, rotationStep = 0) {
  return chooseWeightedLikeTarget(snapshot, photoRatio, rotationStep);
}

function choosePlainLikeTarget(preferredTarget, rotationStep, ...snapshots) {
  if (preferredTarget) {
    for (const snapshot of snapshots) {
      if ((snapshot?.likeTargets || []).includes(preferredTarget)) {
        return preferredTarget;
      }
    }
  }
  for (const snapshot of snapshots) {
    const groups = classifyLikeTargets(snapshot);
    const target =
      pickRotatedTarget(snapshot, groups.photoTargets, 'plain-photo', rotationStep) ||
      pickRotatedTarget(snapshot, groups.answerTargets, 'plain-answer', rotationStep) ||
      pickRotatedTarget(snapshot, groups.otherTargets, 'plain-other', rotationStep) ||
      pickRotatedTarget(snapshot, snapshot?.likeTargets || [], 'plain-any', rotationStep) ||
      '';
    if (target) return target;
  }
  return '';
}

function promptForTarget(snapshot, targetLabel) {
  const prompts = snapshot?.prompts || [];
  if (!prompts.length) return {};
  const normalizedTarget = String(targetLabel || '').toLowerCase();
  const matched = prompts.find((prompt) => {
    const promptText = String(prompt.prompt || '').toLowerCase();
    const answerText = String(prompt.answer || '').toLowerCase();
    return (
      (promptText && normalizedTarget.includes(promptText.slice(0, 18))) ||
      (answerText && normalizedTarget.includes(answerText.slice(0, 18)))
    );
  });
  return matched || prompts[0] || {};
}

function buildLikedComponent(snapshot, targetLabel) {
  if (!snapshot || !targetLabel) return null;
  const label = String(targetLabel || '');
  const kind = /answer/i.test(label) ? 'answer' : /photo/i.test(label) ? 'photo' : /video/i.test(label) ? 'video' : 'profile';
  const targetPrompt = promptForTarget(snapshot, label);
  return {
    targetLabel: label,
    type: kind,
    prompt: targetPrompt.prompt || '',
    answer: targetPrompt.answer || '',
    profileName: snapshot.currentProfile?.name || ''
  };
}

function chooseLikedComponent(photoRatio, rotationStep, ...snapshots) {
  for (const snapshot of snapshots) {
    const targetLabel = chooseWeightedLikeTarget(snapshot, photoRatio, rotationStep);
    if (!targetLabel) continue;
    return buildLikedComponent(snapshot, targetLabel);
  }
  return null;
}

function queueEntryFromEvaluation(sourceTab, snapshot, evaluation) {
  const firstPrompt = (snapshot.prompts || [])[0] || {};
  return {
    profileId: deriveProfileId(`${sourceTab}-${snapshot.currentProfile?.name || 'profile'}`),
    name: snapshot.currentProfile?.name || '',
    sourceTab,
    fit: normalizeFit(evaluation.fit),
    status: evaluation.actionStatus || (evaluation.fit === 'pass' ? 'passed' : 'staged'),
    score: evaluation.score,
    beautyScore: evaluation.visualAttractionScore,
    beautyScoreSource: evaluation.beautyScoreSource || '',
    compatibilityScore: evaluation.compatibilityScore,
    commonGround: evaluation.commonGround || [],
    matchingSignals: evaluation.matchingSignals || [],
    hook: firstPrompt.prompt || '',
    bestOpener: evaluation.recommendedMessage || '',
    note: evaluation.explanation || '',
    promptAnswer: firstPrompt.answer || '',
    selectedTarget: evaluation.selectedTarget || '',
    promptCount: (snapshot.prompts || []).length,
    inspectedViews: snapshot.inspectedViews || 1,
    seenAt: nowIso(),
    imagePath: evaluation.imagePath || ''
  };
}

function safeUnlink(filePath) {
  if (!filePath) return;
  try {
    fs.unlinkSync(filePath);
  } catch (error) {
    // Best-effort cleanup.
  }
}

function buildArtifactPath(paths, prefix, label, extension = '.png') {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const stem = [timestamp, prefix, slugify(label || 'artifact')].filter(Boolean).join('-');
  return path.join(paths.activityImagesDir, `${stem}${extension}`);
}

function persistArtifact(paths, sourcePath, prefix, label) {
  if (!sourcePath || !fs.existsSync(sourcePath)) return '';
  ensureDir(paths.activityImagesDir);
  const extension = path.extname(sourcePath) || '.png';
  const targetPath = buildArtifactPath(paths, prefix, label, extension);
  fs.copyFileSync(sourcePath, targetPath);
  return targetPath;
}

function recordActivity(workspace, entry) {
  const saved = appendActivityEntry(workspace.activityLog, entry);
  saveWorkspace(
    workspace.paths,
    workspace.queue,
    workspace.tasteModel,
    workspace.threadState,
    workspace.activityLog
  );
  return saved;
}

function buildUserProfileText(config) {
  const user = config.user || {};
  const prompts = (user.profilePrompts || []).flatMap(prompt => [prompt.prompt, prompt.answer].filter(Boolean));
  return [
    user.personalitySummary || '',
    user.observationSummary || '',
    user.goals || '',
    user.profileSummary || '',
    ...(user.coreInterests || []),
    ...(user.likesToLeadWith || []),
    ...(user.observedInterestHints || []),
    ...(user.chatStyleExamples || []),
    ...(user.idealFirstDate || []),
    ...(user.attractionPreferences || []),
    ...(user.dealmakerTraits || []),
    ...prompts
  ]
    .map(value => String(value || '').trim())
    .filter(Boolean)
    .join(' ');
}

function finalizeOutgoingMessage(mode, context, workspace, screenshotPath, candidateMessage) {
  if (!candidateMessage) return '';

  try {
    const extraArgs = ['--web-validate', '--candidate-message', candidateMessage];
    if (workspace.config?.ai?.blockFallback !== false) {
      extraArgs.push('--block-fallback', 'true');
    }
    const analysis = runAi(
      mode,
      context,
      workspace.paths.root,
      screenshotPath,
      extraArgs,
      workspace.runtimeEnv
    );
    return analysis?.recommendedMessage || candidateMessage;
  } catch (error) {
    return candidateMessage;
  }
}

function deriveComposerLikedComponent(baseContext, composerSnapshot, selectedTarget) {
  const lines = composerSnapshot?.composer?.componentLines || [];
  const imageLabel = composerSnapshot?.composer?.imageLabel || '';
  const baseComponent = baseContext?.likedComponent || null;
  const targetLabel = selectedTarget || baseComponent?.targetLabel || '';
  const normalizedTarget = String(targetLabel || '').toLowerCase();
  const profileName = String(baseContext?.currentProfile?.name || '').trim().toLowerCase();
  const normalizedLines = lines
    .map((line) => String(line || '').trim())
    .filter(Boolean)
    .filter((line) => String(line).toLowerCase() !== profileName)
    .filter((line) => !/^(send like|send rose|cancel|done|add a comment)$/i.test(line));

  if (/answer/i.test(normalizedTarget) || (normalizedLines.length >= 2 && !/photo|video/i.test(normalizedTarget))) {
    const prompt = normalizedLines[0] || baseComponent?.prompt || '';
    const answer = (
      normalizedLines.length >= 2
        ? normalizedLines.slice(1).join(' ')
        : normalizedLines[0] || baseComponent?.answer || ''
    ).trim();
    return {
      type: 'answer',
      targetLabel,
      prompt,
      answer
    };
  }

  if (/video/i.test(normalizedTarget)) {
    return {
      type: 'video',
      targetLabel,
      prompt: lines.join(' ').trim(),
      answer: ''
    };
  }

  if (/photo/i.test(normalizedTarget) || imageLabel) {
    return {
      type: 'photo',
      targetLabel,
      prompt: lines.join(' ').trim(),
      answer: ''
    };
  }

  return baseComponent;
}

function composerAnchoredContext(baseContext, composerSnapshot, selectedTarget) {
  const likedComponent = deriveComposerLikedComponent(baseContext, composerSnapshot, selectedTarget);
  const context = {
    ...baseContext,
    likedTarget: selectedTarget || baseContext.likedTarget || '',
    likedComponent
  };

  if (likedComponent?.type === 'answer') {
    context.prompts = [
      {
        prompt: likedComponent.prompt || '',
        answer: likedComponent.answer || ''
      }
    ];
  }

  return context;
}

const COMPONENT_ANCHOR_STOP_WORDS = new Set([
  'about',
  'after',
  'again',
  'all',
  'also',
  'and',
  'any',
  'are',
  'be',
  'been',
  'being',
  'could',
  'for',
  'from',
  'have',
  'how',
  'into',
  'its',
  'just',
  'like',
  'more',
  'really',
  'same',
  'some',
  'that',
  'the',
  'their',
  'them',
  'then',
  'there',
  'they',
  'thing',
  'this',
  'to',
  'way',
  'want',
  'what',
  'when',
  'who',
  'with',
  'would',
  'your',
  'youre',
  'year',
  'one',
  'over'
]);

function anchorTokensFromComponent(component) {
  return unique(
    tokenize([component?.answer || '', component?.prompt || ''].join(' ')).filter(
      (token) => token.length >= 3 && !COMPONENT_ANCHOR_STOP_WORDS.has(token)
    )
  ).slice(0, 10);
}

function isAnchoredLikeMessage(message, component) {
  if (!component) return true;
  if (component.type === 'photo' || component.type === 'video') return true;
  const line = String(message || '').toLowerCase();
  const anchors = anchorTokensFromComponent(component);
  if (!anchors.length) return true;
  return anchors.some((anchor) => line.includes(anchor));
}

function titleCaseToken(token) {
  const value = String(token || '').trim();
  if (!value) return '';
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function deterministicAnswerComment(component) {
  if (!component || component.type !== 'answer') return '';
  const prompt = String(component.prompt || '');
  const answer = String(component.answer || '').trim();
  const blob = `${prompt} ${answer}`.toLowerCase();

  if (/\b(run|running|half|marathon|5k|10k)\b/.test(blob)) {
    return "What's your half-marathon target pace?";
  }
  if (/\b(food|restaurant|cook|cooking|coffee|brunch|dessert|pizza|sushi)\b/.test(blob)) {
    return 'Food pick respected, what spot are we trying first?';
  }
  if (/\b(show up|real|guess|feel)\b/.test(blob)) {
    return 'Real and direct? Good, I like that.';
  }
  if (/\b(animal|fight)\b/.test(blob)) {
    return "What's your most realistic animal pick?";
  }
  if (/\b(movie|film|cinema|letterboxd)\b/.test(blob)) {
    return 'Movie taste check: what is your all-time top one?';
  }
  if (/\b(travel|trip|passport|flight|vacation)\b/.test(blob)) {
    return 'Travel answer is strong, best trip story so far?';
  }
  if (/\b(swim|swimming|gym|workout|fitness|pilates|lift)\b/.test(blob)) {
    return 'Active answer, I rate it, favorite workout lately?';
  }
  if (/\b(music|concert|playlist|song)\b/.test(blob)) {
    return 'Music answer is valid, current song on repeat?';
  }

  const anchors = anchorTokensFromComponent(component);
  const lead = titleCaseToken(anchors[0] || '');
  if (!lead) return '';
  return `${lead} caught my eye, what is the backstory?`;
}

function enforceAnchoredComment(message, anchoredContext) {
  const component = anchoredContext?.likedComponent || null;
  const candidate = String(message || '').trim();
  if (!component) {
    return weakFirstLikeMessage(candidate) ? '' : candidate;
  }
  if (!weakFirstLikeMessage(candidate) && isAnchoredLikeMessage(candidate, component)) {
    return candidate;
  }
  const fallback = deterministicAnswerComment(component);
  if (fallback && isAnchoredLikeMessage(fallback, component)) {
    return fallback;
  }
  return '';
}

function weakFirstLikeMessage(message) {
  const normalized = String(message || '').trim().toLowerCase();
  if (!normalized) return true;
  if (normalized.length < 8) return true;
  return (
    /elaborate/.test(normalized) ||
    /^really\??$/.test(normalized) ||
    /what does that mean/.test(normalized) ||
    /what.?s the story behind it/.test(normalized) ||
    /what inspired your choice/.test(normalized) ||
    /what inspired/.test(normalized) ||
    /can you elaborate/.test(normalized) ||
    /tell me more about/.test(normalized) ||
    /what made you choose/.test(normalized) ||
    /how did you decide/.test(normalized) ||
    /for (this|the) photo/.test(normalized) ||
    /stunning dress/.test(normalized) ||
    /context here/.test(normalized) ||
    /is trouble in that photo/.test(normalized) ||
    /has menace/.test(normalized) ||
    /i respect it/.test(normalized)
  );
}

function normalizeMessageFingerprint(message) {
  return String(message || '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function recentSentCommentFingerprints(workspace, limit = 18) {
  return (workspace.activityLog?.entries || [])
    .filter((entry) => entry.actionStatus === 'sent')
    .filter((entry) => ['discover', 'likes', 'standouts'].includes(entry.sourceTab))
    .filter((entry) => String(entry.message || '').trim())
    .slice(0, limit)
    .map((entry) => normalizeMessageFingerprint(entry.message))
    .filter(Boolean);
}

function dedupeOutgoingComment(workspace, candidate, backups, anchoredContext) {
  const component = anchoredContext?.likedComponent || null;
  const current = String(candidate || '').trim();
  if (!current) return '';

  const recentFingerprints = recentSentCommentFingerprints(workspace);
  const currentFingerprint = normalizeMessageFingerprint(current);
  if (!currentFingerprint) return '';
  if (!recentFingerprints.includes(currentFingerprint)) {
    return current;
  }

  const alternatives = [...new Set((backups || []).map((line) => String(line || '').trim()).filter(Boolean))];
  for (const alternative of alternatives) {
    if (alternative === current) continue;
    if (weakFirstLikeMessage(alternative)) continue;
    if (component && !isAnchoredLikeMessage(alternative, component)) continue;
    const alternativeFingerprint = normalizeMessageFingerprint(alternative);
    if (!alternativeFingerprint || recentFingerprints.includes(alternativeFingerprint)) continue;
    return alternative;
  }

  return '';
}

function buildCommonGround(snapshot, config) {
  const user = config.user || {};
  const candidateTexts = extractSignalTexts(snapshot);
  const candidateBlob = candidateTexts.join(' ').toLowerCase();
  const explicitPhrases = unique([
    ...(user.coreInterests || []),
    ...(user.likesToLeadWith || []),
    ...(user.observedInterestHints || []),
    ...(user.idealFirstDate || []),
    ...(user.profilePrompts || []).flatMap(prompt => [prompt.prompt, prompt.answer].filter(Boolean))
  ])
    .map(value => String(value || '').trim())
    .filter(Boolean);

  const phraseMatches = explicitPhrases.filter((phrase) => candidateBlob.includes(phrase.toLowerCase())).slice(0, 8);
  const userTokens = tokenize(buildUserProfileText(config));
  const candidateTokens = tokenize(candidateTexts.join(' '));
  const candidateTokenSet = new Set(candidateTokens);
  const tokenMatches = unique(userTokens.filter((token) => candidateTokenSet.has(token))).slice(0, 12);

  return {
    phraseMatches,
    tokenMatches
  };
}

function scoreTasteFit(snapshot, tasteModel) {
  const candidateTokens = new Set(tokenize(extractSignalTexts(snapshot).join(' ')));
  const matchingSignals = [];
  let weight = 0;

  for (const signal of tasteModel.signals || []) {
    if (candidateTokens.has(signal.token)) {
      matchingSignals.push(signal.token);
      weight += signal.weight;
    }
  }

  return {
    matchingSignals: unique(matchingSignals).slice(0, 10),
    weight
  };
}

function hasDealbreaker(snapshot, config) {
  const candidateBlob = extractSignalTexts(snapshot).join(' ').toLowerCase();
  return (config.user?.dealbreakers || []).some((dealbreaker) =>
    candidateBlob.includes(String(dealbreaker || '').toLowerCase())
  );
}

function clampScore(value, min = 1, max = 10) {
  return Math.max(min, Math.min(max, Number(value)));
}

function deriveBeautyFallbackScore(sourceTab, snapshot, overlap, tasteFit) {
  const promptCount = (snapshot?.prompts || []).length;
  const badgeCount = (snapshot?.statusBadges || []).length;
  const phraseCount = overlap?.phraseMatches?.length || 0;
  const tokenCount = overlap?.tokenMatches?.length || 0;
  const tasteWeight = toNumber(tasteFit?.weight, 0);

  const base = sourceTab === 'standouts' ? 7.6 : sourceTab === 'likes' ? 6.8 : 5.2;
  const qualityBoost = Math.min(1.4, promptCount * 0.28 + badgeCount * 0.22);
  const overlapBoost = Math.min(0.9, phraseCount * 0.35 + tokenCount * 0.06);
  const tasteBoost = Math.min(0.7, tasteWeight / 16);
  return Math.round(clampScore(base + qualityBoost + overlapBoost + tasteBoost));
}

function computeFinalEvaluation(sourceTab, snapshot, analysis, tasteFit, overlap, config) {
  const parsedVisualScore = Number(analysis?.visualAttractionScore);
  const hasModelBeautyScore = Number.isFinite(parsedVisualScore) && parsedVisualScore >= 1;
  const beautyScore = hasModelBeautyScore
    ? Math.round(clampScore(parsedVisualScore))
    : deriveBeautyFallbackScore(sourceTab, snapshot, overlap, tasteFit);
  const beautyScoreSource = hasModelBeautyScore
    ? String(analysis?.source || 'model')
    : `heuristic:${String(analysis?.source || 'local')}`;
  const compatibilityScore = toNumber(
    analysis?.compatibilityScore,
    Math.min(10, 4 + overlap.phraseMatches.length * 2 + Math.min(overlap.tokenMatches.length, 4))
  );
  const profileQualityScore = toNumber(
    analysis?.profileQualityScore,
    Math.min(10, 4 + Math.min(3, (snapshot.prompts || []).length) + Math.min(2, (snapshot.statusBadges || []).length))
  );
  const commonGround = unique([...(analysis?.commonGround || []), ...overlap.phraseMatches, ...overlap.tokenMatches]).slice(0, 10);
  const tasteScore = Math.min(10, 4 + Math.ceil(tasteFit.weight / 2));
  const score = Number(
    (
      beautyScore * 0.35 +
      compatibilityScore * 0.28 +
      profileQualityScore * 0.15 +
      Math.min(10, 4 + commonGround.length) * 0.12 +
      tasteScore * 0.10
    ).toFixed(2)
  );
  const beautyFloor = toNumber(config.automation?.beautyFloor, 6);
  const strongYesThreshold = toNumber(config.automation?.strongYesScoreThreshold, 7);
  const maybeThreshold = toNumber(config.automation?.maybeScoreThreshold, 5);
  const dealbreakerHit = analysis?.dealbreakerHit === true || hasDealbreaker(snapshot, config);

  let fit = 'pass';
  if (!dealbreakerHit && beautyScore >= beautyFloor) {
    fit = score >= strongYesThreshold ? 'strong yes' : score >= maybeThreshold ? 'maybe' : 'pass';
  }

  return {
    score,
    fit,
    visualAttractionScore: beautyScore,
    beautyScoreSource,
    compatibilityScore,
    profileQualityScore,
    commonGround,
    matchingSignals: tasteFit.matchingSignals,
    recommendedMessage: analysis?.recommendedMessage || '',
    backupMessages: analysis?.backupMessages || [],
    explanation: analysis?.explanation || '',
    summary: analysis?.summary || '',
    dealbreakerHit
  };
}

function shouldSendLike(evaluation, options) {
  if (options.trustMode !== 'send') return false;
  if (evaluation.fit === 'strong yes') return true;
  const requireComment = false;
  const maybeSendScoreThreshold = toNumber(options.maybeSendScoreThreshold, 5.6);
  const discoverBeautySendThreshold = toNumber(options.discoverBeautySendThreshold, 6);
  const hasPromptHook = evaluation.profileQualityScore >= 6;
  const hasSharedHook = evaluation.commonGround.length > 0 || (evaluation.matchingSignals || []).length > 0;
  return (
    evaluation.fit === 'maybe' &&
    evaluation.score >= maybeSendScoreThreshold &&
    evaluation.visualAttractionScore >= discoverBeautySendThreshold &&
    (hasSharedHook || hasPromptHook || evaluation.visualAttractionScore >= 7) &&
    (!requireComment || Boolean(evaluation.recommendedMessage))
  );
}

function shouldAttachLikeComment(workspace, sourceTab, evaluation, options) {
  if (options.allowLikeComments === false) return false;
  if (!String(evaluation?.recommendedMessage || '').trim()) return false;
  const ratio = clampScore(toNumber(options.likeCommentRatio, 0.3), 0, 1);
  const boostedRatio = evaluation?.fit === 'strong yes' ? Math.min(0.75, ratio + 0.15) : ratio;
  const seed = [
    sourceTab,
    evaluation?.name || '',
    evaluation?.selectedTarget || '',
    evaluation?.score || '',
    workspace.activityLog?.entries?.length || 0
  ].join('|');
  return stablePercentSeed(seed) < Math.round(boostedRatio * 100);
}

function shouldSendPlainLike(evaluation, options) {
  if (options.trustMode !== 'send') return false;
  if (evaluation.fit === 'strong yes') return true;
  const maybeSendScoreThreshold = toNumber(options.maybeSendScoreThreshold, 5.6);
  const discoverBeautySendThreshold = toNumber(options.discoverBeautySendThreshold, 6);
  return (
    evaluation.fit === 'maybe' &&
    evaluation.score >= maybeSendScoreThreshold &&
    evaluation.visualAttractionScore >= discoverBeautySendThreshold
  );
}

function shouldSendRose(evaluation, options, rosesRemaining) {
  if (options.trustMode !== 'send') return false;
  if (!rosesRemaining) return false;
  const requireComment = options.allowRoseComments !== false;
  const roseThreshold = toNumber(options.roseScoreThreshold, 8);
  return (
    evaluation.score >= roseThreshold &&
    evaluation.visualAttractionScore >= 8 &&
    (!requireComment || Boolean(evaluation.recommendedMessage))
  );
}

function sampleThreadNames(chatSnapshot, count) {
  const threads = (chatSnapshot.chats?.threads || []).filter(thread => thread.name);
  const nonStarter = threads.filter((thread) => !thread.isStarter);
  const preferred = nonStarter.length ? nonStarter : threads;
  return preferred.slice(0, count).map(thread => thread.name);
}

function hasCachedSelfProfile(workspace) {
  const prompts = workspace.config.user?.profilePrompts || [];
  return prompts.length >= 3 && Boolean(workspace.config.user?.profileSummary);
}

function threadStateKey(thread) {
  return String(thread?.name || '').trim().toLowerCase();
}

function threadFingerprint(thread) {
  return [thread?.section || '', thread?.name || '', thread?.preview || ''].join('::');
}

function shouldSkipReplyThread(workspace, thread, options) {
  const key = threadStateKey(thread);
  if (!key) return true;
  const previous = workspace.threadState?.threads?.[key];
  if (!previous) return false;
  if (previous.fingerprint !== threadFingerprint(thread)) return false;

  const processedAt = Date.parse(previous.processedAt || '');
  if (!Number.isFinite(processedAt)) return false;
  const cooldownMs = Math.max(1, options.replyCooldownMinutes) * 60 * 1000;
  return Date.now() - processedAt < cooldownMs;
}

function rememberReplyThread(workspace, thread, action, message) {
  const key = threadStateKey(thread);
  if (!key) return;
  workspace.threadState.threads[key] = {
    name: thread.name,
    section: thread.section || '',
    preview: thread.preview || '',
    fingerprint: threadFingerprint(thread),
    action,
    processedAt: nowIso(),
    message: message || ''
  };
  workspace.threadState.updatedAt = nowIso();
}

function recentActivityNotes(workspace, limit = 8) {
  return (workspace.activityLog?.entries || [])
    .slice(0, limit)
    .map((entry) => `${entry.type}:${entry.name || entry.title || ''}:${entry.actionStatus || ''}`);
}

function likeTargetRotationStep(workspace, sourceTab, profileName = '') {
  const tabEntries = (workspace.activityLog?.entries || []).filter((entry) => entry.sourceTab === sourceTab);
  const sameProfileEntries = profileName
    ? tabEntries.filter((entry) => String(entry.name || '').toLowerCase() === String(profileName || '').toLowerCase())
    : [];
  return tabEntries.length + sameProfileEntries.length * 2;
}

function remainingBudgetMs(options) {
  if (!options?.sweepStartedAt || !options?.screenActionBudgetMs) return Infinity;
  return Math.max(0, options.screenActionBudgetMs - (Date.now() - options.sweepStartedAt));
}

function budgetExpired(options) {
  return remainingBudgetMs(options) <= 0;
}

function normalizeTabOrder(orderedTabs, fallbackTabs) {
  const fallback = fallbackTabs || [];
  const valid = new Set(['chats', 'likes', 'discover', 'standouts']);
  const merged = [];
  for (const tab of [...(orderedTabs || []), ...fallback]) {
    if (!valid.has(tab) || merged.includes(tab)) continue;
    merged.push(tab);
  }
  return merged;
}

function orderedReplyCandidates(chatSnapshot, plannerReplyTargets = []) {
  const threads = (chatSnapshot?.chats?.threads || [])
    .filter((thread) => thread.name)
    .filter((thread) => thread.section.startsWith('Your turn') || thread.section.startsWith('Hidden'));
  const byKey = new Map(threads.map((thread) => [threadStateKey(thread), thread]));
  const ordered = [];

  for (const name of plannerReplyTargets) {
    const thread = byKey.get(threadStateKey({ name }));
    if (thread && !ordered.includes(thread)) {
      ordered.push(thread);
    }
  }

  for (const thread of threads) {
    if (!ordered.includes(thread)) {
      ordered.push(thread);
    }
  }

  return ordered;
}

function shouldReplyToOpenedThread(threadSnapshot, thread = null) {
  const messages = threadSnapshot.thread?.messages || [];
  const nonSystemMessages = messages.filter((message) => !message.isSystem);
  const systemTexts = messages.map((message) => message.text || '');
  const hasStarterPrompt =
    Boolean(thread?.isStarter) ||
    /^Start the chat with /i.test(String(thread?.preview || '')) ||
    systemTexts.some((text) => /^Start the chat with /i.test(text));
  const hasLikeInitiatedSystem =
    systemTexts.some((text) => /^You liked /i.test(text) || /^You sent a rose/i.test(text)) ||
    /^You liked /i.test(String(thread?.preview || ''));

  // Allow first outreach on your pending matches when no one has sent a real message yet.
  if (nonSystemMessages.length === 0 && (hasStarterPrompt || hasLikeInitiatedSystem)) {
    return true;
  }

  const newestNonSystem = nonSystemMessages[0];
  if (newestNonSystem?.side === 'you') return false;
  if (newestNonSystem?.side === 'them') return true;

  const lastSpeaker = threadSnapshot.thread?.lastSpeaker || '';
  if (lastSpeaker === 'you') return false;
  if (lastSpeaker === 'them') return true;

  const latestText = threadSnapshot.thread?.lastMessageText || '';
  if (/^You /.test(latestText)) return false;
  return Boolean(latestText);
}

function planSweep(workspace, options, chatSnapshot) {
  const visibleThreads = chatSnapshot?.chats?.threads || [];
  const replyCandidates = orderedReplyCandidates(chatSnapshot);
  const fallbackTabs =
    replyCandidates.length > 0
      ? options.activeTabs
      : ['likes', 'discover', 'standouts', 'chats'].filter((tab) => options.activeTabs.includes(tab));

  const context = {
    currentTab: chatSnapshot?.currentTab || '',
    activeTabs: options.activeTabs,
    visibleThreads: visibleThreads.map((thread) => ({
      name: thread.name,
      section: thread.section,
      preview: thread.preview,
      isStarter: thread.isStarter
    })),
    recentActivity: recentActivityNotes(workspace),
    queueSummary: {
      queued: (workspace.queue?.entries || []).filter((entry) => entry.status === 'staged').length,
      passed: (workspace.queue?.entries || []).filter((entry) => entry.status === 'passed').length
    }
  };

  if (!chatSnapshot || remainingBudgetMs(options) < 22000 || visibleThreads.length <= 1) {
    return {
      mode: 'planner',
      source: 'fallback',
      orderedTabs: fallbackTabs,
      replyTargets: replyCandidates.map((thread) => thread.name),
      refreshTaste: replyCandidates.length > 0,
      explanation: 'Used fast local planner to preserve the on-screen time budget.'
    };
  }

  try {
    return runAi('planner', context, workspace.paths.root, '', [], workspace.runtimeEnv);
  } catch (error) {
    return {
      mode: 'planner',
      source: 'fallback',
      orderedTabs: fallbackTabs,
      replyTargets: replyCandidates.map((thread) => thread.name),
      refreshTaste: replyCandidates.length > 0,
      explanation: 'Fallback planner used.'
    };
  }
}

function safeSnapshot() {
  try {
    return runHinge(['--snapshot']);
  } catch (error) {
    return null;
  }
}

function safeEnsureChatList(workspace) {
  try {
    return ensureChatList();
  } catch (error) {
    updateAgentProgress(workspace, 'Chats unavailable, continuing with other tabs', {
      tab: 'chats',
      phase: 'skip-chats',
      tabError: error.message || String(error)
    });
    return null;
  }
}

function navigateBackIfNeeded(maxSteps = 2) {
  for (let step = 0; step < maxSteps; step += 1) {
    try {
      const dismissed = runHinge(['--dismiss-overlay']);
      if (dismissed?.dismissed) {
        continue;
      }
    } catch (error) {
      // Ignore missing overlay or transient tap failures.
    }

    const snapshot = runHinge(['--snapshot']);
    if (!['chat-thread', 'thread-profile'].includes(snapshot.screenType) && !['self-profile-editor', 'like-composer'].includes(snapshot.screenType)) {
      return snapshot;
    }

    if (snapshot.screenType === 'like-composer') {
      try {
        runHinge(['--cancel-open-interest']);
      } catch (error) {
        runHinge(['--tap-label', 'Cancel']);
      }
    } else if (snapshot.screenType === 'self-profile-editor') {
      runHinge(['--tap-label', 'Cancel']);
    } else {
      runHinge(['--tap-label', 'Back']);
    }
  }

  return runHinge(['--snapshot']);
}

function waitFor(predicate, attempts = 6) {
  let snapshot = runHinge(['--snapshot']);
  if (predicate(snapshot)) {
    return snapshot;
  }

  for (let attempt = 0; attempt < attempts; attempt += 1) {
    snapshot = runHinge(['--snapshot']);
    if (predicate(snapshot)) {
      return snapshot;
    }
  }

  return snapshot;
}

function nudgeBottomNav(actionId) {
  if (actionId === 'tap-bottom') {
    runHinge(['--tap-coordinates', '--x', '195', '--y', '812']);
    return;
  }
  if (actionId === 'scroll-up') {
    runHinge(['--scroll-up']);
    return;
  }
  if (actionId === 'scroll-down') {
    runHinge(['--scroll-down']);
    return;
  }
}

function ensureTab(tab, predicate) {
  const tabReady = (current) => current.currentTab === tab && (!predicate || predicate(current));

  try {
    runHinge(['--activate']);
  } catch (error) {
    // Keep going if activate is briefly unavailable.
  }

  try {
    runHinge(['--dismiss-overlay']);
  } catch (error) {
    // Best-effort overlay cleanup.
  }

  try {
    runHinge(['--go-tab', tab]);
  } catch (error) {
    // Fall through to fast recovery attempt.
  }

  let snapshot = waitFor(tabReady, 2);
  if (snapshot.currentTab === tab) {
    return snapshot;
  }

  try {
    nudgeBottomNav('tap-bottom');
    nudgeBottomNav('scroll-up');
    runHinge(['--dismiss-overlay']);
    runHinge(['--go-tab', tab]);
  } catch (error) {
    // Recovery attempt failed; throw below with latest snapshot.
  }

  snapshot = waitFor(tabReady, 2);
  if (snapshot.currentTab === tab) {
    return snapshot;
  }
  throw new Error(`Unable to reach ${tab} tab from screen ${snapshot.screenType || 'unknown'}`);
}

function ensureChatList() {
  navigateBackIfNeeded(2);
  const snapshot = ensureTab('chats', (current) => current.screenType === 'chat-list');
  if (snapshot.screenType !== 'chat-list') {
    throw new Error(`Unable to reach chat list from screen ${snapshot.screenType || 'unknown'}`);
  }
  return snapshot;
}

function ensureDiscoverProfile() {
  navigateBackIfNeeded(2);
  const snapshot = ensureTab('discover', (current) => current.screenType === 'profile');
  if (snapshot.screenType !== 'profile') {
    throw new Error(`Unable to reach Discover profile from screen ${snapshot.screenType || 'unknown'}`);
  }
  return snapshot;
}

function ensureLikesScreen() {
  navigateBackIfNeeded(2);
  return ensureTab('likes');
}

function ensureStandoutsScreen() {
  navigateBackIfNeeded(2);
  return ensureTab('standouts');
}

function buildFastProfileAnalysis(sourceTab, snapshot, overlap, tasteFit, reason) {
  const promptCount = (snapshot.prompts || []).length;
  const badgeCount = (snapshot.statusBadges || []).length;
  const compatibilityScore = Math.min(10, 3 + overlap.phraseMatches.length * 2 + Math.min(overlap.tokenMatches.length, 3));
  const profileQualityScore = Math.max(3, Math.min(8, 3 + promptCount + Math.min(2, badgeCount)));
  const visualAttractionScore = deriveBeautyFallbackScore(sourceTab, snapshot, overlap, tasteFit);
  return {
    mode: 'profile',
    source: 'fast-screen',
    summary: `Quick-screened ${snapshot.currentProfile?.name || 'profile'} before full AI analysis.`,
    signals: extractSignalTexts(snapshot).slice(0, 6),
    risks: [],
    recommendedMessage: '',
    visualAttractionScore,
    compatibilityScore,
    profileQualityScore,
    commonGround: unique([...overlap.phraseMatches, ...overlap.tokenMatches]).slice(0, 8),
    dealbreakerHit: false,
    backupMessages: [],
    explanation: reason || 'Low-signal profile skipped without a full model call.',
    matchingSignals: tasteFit.matchingSignals || []
  };
}

function shouldQuickScreenProfile(sourceTab, snapshot, overlap, tasteFit, options) {
  if (sourceTab === 'standouts' || sourceTab === 'likes') return false;
  const quickScreenBudgetMs = toNumber(options.quickScreenBudgetMs, 8000);
  const protectedProfileAnalysis = options.protectedProfileAnalysis === true;
  if (protectedProfileAnalysis && (snapshot.prompts || []).length > 0) {
    return false;
  }
  if (remainingBudgetMs(options) < quickScreenBudgetMs) return true;
  const promptCount = (snapshot.prompts || []).length;
  const badgeCount = (snapshot.statusBadges || []).length;
  const sharedSignalCount = overlap.phraseMatches.length + overlap.tokenMatches.length + (tasteFit.matchingSignals || []).length;
  return promptCount === 0 && badgeCount === 0 && sharedSignalCount === 0;
}

function inspectScrolledProfile(initialSnapshot, scrollSteps) {
  const snapshots = [initialSnapshot];
  const profileName = initialSnapshot.currentProfile?.name || '';

  for (let step = 0; step < scrollSteps; step += 1) {
    runHinge(['--scroll-down']);
    const snapshot = runHinge(['--snapshot']);
    if (snapshot.currentProfile?.name && profileName && snapshot.currentProfile.name !== profileName) {
      break;
    }
    snapshots.push(snapshot);
  }

  return {
    merged: mergeProfileSnapshots(snapshots),
    currentView: snapshots[snapshots.length - 1],
    views: snapshots
  };
}

function captureMatchExample(threadName, scrollSteps) {
  runHinge(['--open-thread', '--name', threadName]);
  runHinge(['--open-thread-profile']);
  const inspected = inspectScrolledProfile(runHinge(['--snapshot']), scrollSteps);
  const example = {
    matchName: threadName,
    prompts: (inspected.merged.prompts || []).map(prompt => ({
      prompt: prompt.prompt || '',
      answer: prompt.answer || ''
    })),
    signalTexts: extractSignalTexts(inspected.merged)
  };
  navigateBackIfNeeded(1);
  return example;
}

function refreshTasteModel(workspace, sampleCount, scrollSteps) {
  updateAgentProgress(workspace, 'Refreshing taste model from chats', { tab: 'chats', phase: 'refreshing-taste' });
  const chatSnapshot = ensureChatList();
  const threadNames = sampleThreadNames(chatSnapshot, sampleCount);
  const examples = [];

  for (const threadName of threadNames) {
    try {
      updateAgentProgress(workspace, `Sampling ${threadName} for taste model`, { tab: 'chats', threadName });
      examples.push(captureMatchExample(threadName, scrollSteps));
    } catch (error) {
      examples.push({
        matchName: threadName,
        prompts: [],
        signalTexts: []
      });
    }
  }

  const usableExamples = examples.filter(example => example.signalTexts.length > 0);
  if (!usableExamples.length) {
    return workspace.tasteModel;
  }

  const tasteModel = mergeTasteModel(workspace.tasteModel, usableExamples);
  workspace.tasteModel = tasteModel;
  writeJson(workspace.paths.tasteModelPath, tasteModel);
  recordActivity(workspace, {
    type: 'taste-refresh',
    title: 'Refreshed taste model',
    sourceTab: 'chats',
    summary: `Updated taste signals from ${usableExamples.length} match profile(s).`,
    notes: usableExamples.map((example) => example.matchName)
  });
  return tasteModel;
}

function bootstrapUserProfile(workspace) {
  if (hasCachedSelfProfile(workspace) && !hasFlag('--refresh-self-profile')) {
    return workspace.config.user.profilePrompts;
  }

  try {
    updateAgentProgress(workspace, 'Refreshing your profile cache', { tab: 'settings', phase: 'bootstrap-self-profile' });
    ensureTab('settings');
    try {
      runHinge(['--tap-label', 'My Hinge']);
    } catch (error) {
      // Already selected.
    }
    runHinge(['--open-self-profile-editor']);
    let snapshot = waitFor((current) => current.screenType === 'self-profile-editor');
    const collectedPrompts = [];
    const seen = new Set();

    for (let step = 0; step < 3; step += 1) {
      for (const prompt of snapshot.selfProfile?.prompts || []) {
        if (seen.has(prompt.label)) continue;
        seen.add(prompt.label);
        collectedPrompts.push(prompt);
      }
      runHinge(['--scroll-down']);
      snapshot = runHinge(['--snapshot']);
      if (snapshot.screenType !== 'self-profile-editor') {
        break;
      }
    }

    const prompts = collectedPrompts;
    if (!prompts.length) {
      runHinge(['--tap-label', 'Cancel']);
      return null;
    }

    workspace.config.user.profilePrompts = prompts.map((prompt) => ({
      prompt: prompt.prompt,
      answer: prompt.answer
    }));
    if (!workspace.config.user.coreInterests?.length) {
      workspace.config.user.coreInterests = unique(
        prompts.flatMap((prompt) => tokenize(`${prompt.prompt} ${prompt.answer}`)).slice(0, 24)
      );
    }
    if (!workspace.config.user.profileSummary) {
      workspace.config.user.profileSummary = prompts.map((prompt) => `${prompt.prompt}: ${prompt.answer}`).join(' | ');
    }
    workspace.config.user.lastProfileBootstrapAt = nowIso();
    writeJson(workspace.paths.configPath, workspace.config);
    recordActivity(workspace, {
      type: 'self-profile',
      title: 'Refreshed self profile cache',
      sourceTab: 'settings',
      summary: `Cached ${workspace.config.user.profilePrompts.length} prompt(s) from your profile.`,
      notes: workspace.config.user.profilePrompts.map((prompt) => `${prompt.prompt}: ${prompt.answer}`)
    });
    runHinge(['--tap-label', 'Cancel']);
    return workspace.config.user.profilePrompts;
  } catch (error) {
    return null;
  }
}

function evaluateProfile(sourceTab, workspace, tasteModel, topSnapshot, inspected, screenshotPath, options) {
  const rotationStep = likeTargetRotationStep(workspace, sourceTab, topSnapshot.currentProfile?.name || '');
  const likedComponent = chooseLikedComponent(
    toNumber(options.photoLikeTargetRatio, 0.7),
    rotationStep,
    topSnapshot,
    inspected.currentView,
    inspected.merged
  );
  const selectedTarget = likedComponent?.targetLabel || '';
  const context = {
    ...inspected.merged,
    sourceTab,
    likedTarget: selectedTarget,
    likedComponent
  };
  const overlap = buildCommonGround(inspected.merged, workspace.config);
  const tasteFit = scoreTasteFit(inspected.merged, tasteModel);
  const analysis = shouldQuickScreenProfile(sourceTab, inspected.merged, overlap, tasteFit, options)
    ? buildFastProfileAnalysis(
        sourceTab,
        inspected.merged,
        overlap,
        tasteFit,
        remainingBudgetMs(options) < 12000
          ? 'Budget running low, used fast profile screen.'
          : 'Low-signal profile skipped without full AI analysis.'
      )
    : runAi('profile', context, workspace.paths.root, screenshotPath, ['--use-rizz', 'false'], workspace.runtimeEnv);
  const evaluation = computeFinalEvaluation(sourceTab, inspected.merged, analysis, tasteFit, overlap, workspace.config);
  return {
    ...evaluation,
    analysis,
    selectedTarget
  };
}

function recordProfileDecision(workspace, sourceTab, snapshot, evaluation) {
  const queueEntry = queueEntryFromEvaluation(sourceTab, snapshot, evaluation);
  workspace.queue = upsertEntry(workspace.queue, queueEntry);
  saveWorkspace(workspace.paths, workspace.queue, workspace.tasteModel, workspace.threadState, workspace.activityLog);
  return queueEntry;
}

function processReplyThreads(workspace, options, planner = null) {
  const results = [];
  if (!options.allowReplies) {
    return results;
  }
  if (budgetExpired(options)) {
    return results;
  }
  updateAgentProgress(workspace, 'Processing chats', { tab: 'chats', phase: 'processing-chats' });
  const chatSnapshot = ensureChatList();
  const candidateThreads = orderedReplyCandidates(chatSnapshot, planner?.replyTargets || [])
    .filter((thread) => !shouldSkipReplyThread(workspace, thread, options));
  const limit = Math.min(candidateThreads.length, options.maxRepliesPerCycle);

  for (let index = 0; index < limit; index += 1) {
    if (budgetExpired(options)) break;
    const thread = candidateThreads[index];
    updateAgentProgress(workspace, `Opening chat with ${thread.name}`, { tab: 'chats', threadName: thread.name });
    runHinge(['--open-thread', '--name', thread.name]);
    const threadSnapshot = waitFor((current) => current.screenType === 'chat-thread');
    if (!shouldReplyToOpenedThread(threadSnapshot, thread)) {
      rememberReplyThread(workspace, thread, 'skipped-last-speaker-you', '');
      results.push({ name: thread.name, action: 'skipped-last-speaker-you', message: '', imagePath: '' });
      recordActivity(workspace, {
        type: 'reply-skip',
        title: `Skipped ${thread.name}`,
        sourceTab: 'chats',
        name: thread.name,
        actionStatus: 'skipped-last-speaker-you',
        summary: 'Did not send a message because you were the last speaker in the thread.'
      });
      navigateBackIfNeeded(2);
      continue;
    }

    const screenshotPath = captureScreenshot('hinge-reply');
    const imagePath = persistArtifact(workspace.paths, screenshotPath, 'reply', thread.name);
    updateAgentProgress(workspace, `Drafting reply for ${thread.name}`, { tab: 'chats', threadName: thread.name, phase: 'ai-reply' });
    const analysis = runAi('reply', threadSnapshot, workspace.paths.root, screenshotPath, [], workspace.runtimeEnv);
    const message = analysis?.recommendedMessage || '';
    let action = 'staged';

    if (options.trustMode === 'send' && options.allowAutoSendReplies && message) {
      updateAgentProgress(workspace, `Finalizing reply for ${thread.name}`, { tab: 'chats', threadName: thread.name, phase: 'web-validate-reply' });
      const finalMessage = finalizeOutgoingMessage('reply', threadSnapshot, workspace, screenshotPath, message);
      runHinge(['--send-reply', '--message', finalMessage]);
      safeUnlink(screenshotPath);
      rememberReplyThread(workspace, thread, 'replied', finalMessage);
      results.push({ name: thread.name, action: 'replied', message: finalMessage, imagePath });
      recordActivity(workspace, {
        type: 'reply',
        title: `Replied to ${thread.name}`,
        sourceTab: 'chats',
        name: thread.name,
        actionStatus: 'replied',
        message: finalMessage,
        summary: `Sent a reply in ${thread.name}'s thread.`,
        notes: analysis?.signals || [],
        imagePath
      });
      action = 'replied';
      navigateBackIfNeeded(2);
      continue;
    } else {
      safeUnlink(screenshotPath);
      writeStagedMessage(workspace.paths, message);
      rememberReplyThread(workspace, thread, 'staged', message);
    }
    results.push({ name: thread.name, action, message, imagePath });
    recordActivity(workspace, {
      type: 'reply',
      title: `${action === 'replied' ? 'Replied to' : 'Staged reply for'} ${thread.name}`,
      sourceTab: 'chats',
      name: thread.name,
      actionStatus: action,
      message,
      summary:
        action === 'replied'
          ? `Sent a reply in ${thread.name}'s thread.`
          : `Staged a reply in ${thread.name}'s thread without sending.`,
      notes: analysis?.signals || [],
      imagePath
    });

    navigateBackIfNeeded(2);
  }

  return results;
}

function processProfileLikeFlow(sourceTab, workspace, tasteModel, options) {
  let topSnapshot = runHinge(['--snapshot']);
  if (topSnapshot.screenType === 'unknown' || topSnapshot.screenType === 'like-composer') {
    try {
      const dismissed = runHinge(['--dismiss-overlay']);
      if (!dismissed?.dismissed && topSnapshot.screenType === 'like-composer') {
        runHinge(['--cancel-open-interest']);
      }
      topSnapshot = runHinge(['--snapshot']);
    } catch (error) {
      // Leave snapshot unchanged and let the caller safely skip this pass.
    }
  }
  if (topSnapshot.screenType !== 'profile' || !topSnapshot.currentProfile?.name) {
    return null;
  }
  updateAgentProgress(workspace, `Inspecting ${topSnapshot.currentProfile.name} on ${sourceTab}`, {
    tab: sourceTab,
    profileName: topSnapshot.currentProfile.name,
    phase: 'inspecting-profile'
  });

  const screenshotPath = captureScreenshot(`hinge-${sourceTab}`);
  const imagePath = persistArtifact(
    workspace.paths,
    screenshotPath,
    sourceTab,
    topSnapshot.currentProfile?.name || 'profile'
  );
  const inspected = inspectScrolledProfile(topSnapshot, options.profileScrollSteps);
  const rotationStep = likeTargetRotationStep(workspace, sourceTab, topSnapshot.currentProfile?.name || '');
  const likedComponent = chooseLikedComponent(
    toNumber(options.photoLikeTargetRatio, 0.7),
    rotationStep,
    topSnapshot,
    inspected.currentView,
    inspected.merged
  );
  const selectedTarget = likedComponent?.targetLabel || '';
  const context = {
    ...inspected.merged,
    sourceTab,
    likedTarget: selectedTarget,
    likedComponent
  };
  const evaluation = evaluateProfile(sourceTab, workspace, tasteModel, topSnapshot, inspected, screenshotPath, options);
  evaluation.selectedTarget = evaluation.selectedTarget || selectedTarget;

  let actionStatus = 'reviewed';
  let sendDetail = '';
  if (sourceTab === 'standouts' && options.allowAutoSendRoses && shouldSendRose(evaluation, options, options.rosesRemaining)) {
    if (options.allowRoseComments && evaluation.recommendedMessage) {
      updateAgentProgress(workspace, `Finalizing rose for ${topSnapshot.currentProfile.name}`, {
        tab: sourceTab,
        profileName: topSnapshot.currentProfile.name,
        phase: 'web-validate-rose'
      });
      evaluation.recommendedMessage = finalizeOutgoingMessage(
        'rose',
        context,
        workspace,
        screenshotPath,
        evaluation.recommendedMessage
      );
      evaluation.recommendedMessage = enforceAnchoredComment(evaluation.recommendedMessage, context);
      evaluation.recommendedMessage = dedupeOutgoingComment(
        workspace,
        evaluation.recommendedMessage,
        evaluation.backupMessages,
        context
      );
      if (!evaluation.recommendedMessage) {
        const plainRoseTarget = choosePlainLikeTarget(
          evaluation.selectedTarget,
          rotationStep,
          topSnapshot,
          inspected.currentView,
          inspected.merged
        );
        runHinge(['--send-rose', '--target-label', plainRoseTarget]);
        evaluation.selectedTarget = plainRoseTarget;
        sendDetail = 'rose-plain';
      } else {
        runHinge(['--send-rose-with-comment', '--comment', evaluation.recommendedMessage, '--target-label', evaluation.selectedTarget]);
        sendDetail = 'rose-comment';
      }
    } else {
      const plainRoseTarget = choosePlainLikeTarget(
        evaluation.selectedTarget,
        rotationStep,
        topSnapshot,
        inspected.currentView,
        inspected.merged
      );
      runHinge(['--send-rose', '--target-label', plainRoseTarget]);
      evaluation.recommendedMessage = '';
      evaluation.selectedTarget = plainRoseTarget;
      sendDetail = 'rose-plain';
    }
    actionStatus = 'sent';
  } else if (options.allowAutoSendLikes && shouldSendLike(evaluation, options)) {
    if (!shouldAttachLikeComment(workspace, sourceTab, evaluation, options)) {
      const plainLikeTarget = choosePlainLikeTarget(
        evaluation.selectedTarget,
        rotationStep,
        topSnapshot,
        inspected.currentView,
        inspected.merged
      );
      runHinge(['--send-like', '--target-label', plainLikeTarget]);
      evaluation.recommendedMessage = '';
      evaluation.selectedTarget = plainLikeTarget;
      actionStatus = 'sent';
      sendDetail = 'like-plain';
    } else {
      updateAgentProgress(workspace, `Finalizing like for ${topSnapshot.currentProfile.name}`, {
        tab: sourceTab,
        profileName: topSnapshot.currentProfile.name,
        phase: 'web-validate-like'
      });
      try {
        runHinge(['--open-interest-composer', '--target-label', evaluation.selectedTarget]);
        const composerSnapshot = runHinge(['--snapshot']);
        const anchoredContext = composerAnchoredContext(context, composerSnapshot, evaluation.selectedTarget);
        const finalizedMessage = finalizeOutgoingMessage(
          'profile',
          anchoredContext,
          workspace,
          screenshotPath,
          evaluation.recommendedMessage
        );
        evaluation.recommendedMessage = enforceAnchoredComment(finalizedMessage, anchoredContext);
        evaluation.recommendedMessage = dedupeOutgoingComment(
          workspace,
          evaluation.recommendedMessage,
          evaluation.backupMessages,
          anchoredContext
        );

        if (!evaluation.recommendedMessage) {
          runHinge(['--replace-open-interest-comment', '--comment', '']);
          runHinge(['--complete-open-interest']);
          evaluation.selectedTarget = evaluation.selectedTarget || selectedTarget;
          sendDetail = 'like-plain';
          actionStatus = 'sent';
        } else {
          runHinge(['--replace-open-interest-comment', '--comment', evaluation.recommendedMessage]);
          runHinge(['--complete-open-interest']);
          sendDetail = 'like-comment';
          actionStatus = 'sent';
        }
      } catch (error) {
        const finalizedMessage = finalizeOutgoingMessage(
          'profile',
          context,
          workspace,
          screenshotPath,
          evaluation.recommendedMessage
        );
        evaluation.recommendedMessage = enforceAnchoredComment(finalizedMessage, context);
        evaluation.recommendedMessage = dedupeOutgoingComment(
          workspace,
          evaluation.recommendedMessage,
          evaluation.backupMessages,
          context
        );
        if (!evaluation.recommendedMessage) {
          const plainLikeTarget = choosePlainLikeTarget(
            evaluation.selectedTarget,
            rotationStep,
            topSnapshot,
            inspected.currentView,
            inspected.merged
          );
          runHinge(['--send-like', '--target-label', plainLikeTarget]);
          evaluation.selectedTarget = plainLikeTarget;
          sendDetail = 'like-plain';
          actionStatus = 'sent';
        } else {
          runHinge(['--send-like-with-comment', '--comment', evaluation.recommendedMessage, '--target-label', evaluation.selectedTarget]);
          sendDetail = 'like-comment';
          actionStatus = 'sent';
        }
      }
    }
  } else if (options.allowAutoSendLikes && shouldSendPlainLike(evaluation, options)) {
    const plainLikeTarget = choosePlainLikeTarget(
      evaluation.selectedTarget,
      rotationStep,
      topSnapshot,
      inspected.currentView,
      inspected.merged
    );
    runHinge(['--send-like', '--target-label', plainLikeTarget]);
    evaluation.recommendedMessage = '';
    evaluation.selectedTarget = plainLikeTarget;
    actionStatus = 'sent';
    sendDetail = 'like-plain';
  } else if (options.allowAutoSkipPasses) {
    runHinge(['--skip-current']);
    actionStatus = evaluation.fit === 'pass' ? 'passed' : 'skipped';
  }
  safeUnlink(screenshotPath);

  const queueEntry = recordProfileDecision(workspace, sourceTab, inspected.merged, {
    ...evaluation,
    imagePath,
    actionStatus
  });

  recordActivity(workspace, {
    type: sourceTab === 'standouts' ? 'standout' : sourceTab === 'likes' ? 'like-review' : 'discover-review',
    title:
      actionStatus === 'sent'
        ? `Sent ${sourceTab === 'standouts' ? 'rose' : 'like'} to ${queueEntry.name}`
        : actionStatus === 'passed'
          ? `Passed on ${queueEntry.name}`
          : `Reviewed ${queueEntry.name}`,
    sourceTab,
    name: queueEntry.name,
    fit: queueEntry.fit,
    score: queueEntry.score,
    beautyScore: queueEntry.beautyScore,
    beautyScoreSource: queueEntry.beautyScoreSource,
    compatibilityScore: queueEntry.compatibilityScore,
    commonGround: queueEntry.commonGround,
    actionStatus,
    message: queueEntry.bestOpener,
    summary:
      actionStatus === 'sent'
        ? sendDetail === 'rose-plain'
          ? 'Sent a rose without a comment.'
          : sendDetail === 'rose-comment'
            ? 'Sent a rose with a contextual comment.'
            : sendDetail === 'like-comment'
              ? 'Sent a like with a contextual comment.'
              : 'Sent a plain like without a comment.'
        : actionStatus === 'passed'
          ? 'Passed after scrolling and scoring the profile.'
          : 'Reviewed and queued this profile without sending.',
    notes: [
      `Prompt count: ${queueEntry.promptCount}`,
      `Inspected views: ${queueEntry.inspectedViews}`,
      `Beauty source: ${queueEntry.beautyScoreSource || 'unknown'}`,
      ...(queueEntry.matchingSignals || [])
    ],
    imagePath
  });

  return {
    name: queueEntry.name,
    fit: queueEntry.fit,
    score: queueEntry.score,
    beautyScore: queueEntry.beautyScore,
    beautyScoreSource: queueEntry.beautyScoreSource,
    compatibilityScore: queueEntry.compatibilityScore,
    commonGround: queueEntry.commonGround,
    actionStatus
  };
}

function processLikesTab(workspace, tasteModel, options) {
  if (budgetExpired(options)) {
    return { mode: 'budget-expired', decisions: [] };
  }
  updateAgentProgress(workspace, 'Checking Likes', { tab: 'likes', phase: 'processing-likes' });
  const likesSnapshot = ensureLikesScreen();
  if (likesSnapshot.screenType === 'likes-empty' || likesSnapshot.likes?.empty) {
    recordActivity(workspace, {
      type: 'likes-empty',
      title: 'Likes inbox empty',
      sourceTab: 'likes',
      summary: 'Checked Likes and found no incoming likes.'
    });
    return { mode: 'empty', decisions: [] };
  }

  if (likesSnapshot.screenType === 'profile') {
    const decision = processProfileLikeFlow('likes', workspace, tasteModel, options);
    return { mode: 'profile', decisions: decision ? [decision] : [] };
  }

  return { mode: likesSnapshot.screenType, decisions: [] };
}

function processDiscoverTab(workspace, tasteModel, options) {
  const decisions = [];
  for (let index = 0; index < options.maxDiscoverProfilesPerCycle; index += 1) {
    if (budgetExpired(options)) break;
    updateAgentProgress(workspace, `Checking Discover (${index + 1}/${options.maxDiscoverProfilesPerCycle})`, {
      tab: 'discover',
      phase: 'processing-discover'
    });
    ensureDiscoverProfile();
    const decision = processProfileLikeFlow('discover', workspace, tasteModel, options);
    if (decision) {
      decisions.push(decision);
    }
  }
  return { mode: 'discover', decisions };
}

function processStandoutsTab(workspace, tasteModel, options) {
  if (budgetExpired(options)) {
    return { mode: 'budget-expired', decisions: [] };
  }
  updateAgentProgress(workspace, 'Checking Standouts', { tab: 'standouts', phase: 'processing-standouts' });
  const standoutsSnapshot = ensureStandoutsScreen();
  const standouts = standoutsSnapshot.standouts || { cards: [], rosesRemaining: 0 };
  if (!standouts.cards.length) {
    recordActivity(workspace, {
      type: 'standouts-empty',
      title: 'No standouts available',
      sourceTab: 'standouts',
      summary: 'Checked Standouts and found no visible cards.'
    });
    return { mode: 'empty', decisions: [] };
  }

  const limit = Math.min(standouts.cards.length, options.maxStandoutsPerCycle);
  const decisions = [];

  for (let index = 0; index < limit; index += 1) {
    if (budgetExpired(options)) break;
    const latestStandouts = ensureStandoutsScreen();
    const card = latestStandouts.standouts?.cards?.[0];
    const rosesRemaining = latestStandouts.standouts?.rosesRemaining ?? 0;
    if (!card?.label) break;
    runHinge(['--open-first-standout']);
    const profileSnapshot = waitFor((current) => current.screenType === 'profile');
    if (profileSnapshot.screenType !== 'profile') {
      break;
    }

    const decision = processProfileLikeFlow('standouts', workspace, tasteModel, {
      ...options,
      rosesRemaining
    });
    if (decision) {
      decisions.push(decision);
    }
  }

  return { mode: 'standouts', decisions };
}

function readOptions(config) {
  const preferredTabs = config.automation?.activeTabs || ['chats', 'likes', 'discover', 'standouts'];
  const agentMode = normalizeAgentMode(getArg('--agent-mode', config.automation?.agentMode || 'full_access'));
  const modePolicy = buildAgentModePolicy(agentMode, preferredTabs);
  return {
    agentMode: modePolicy.agentMode,
    agentModeLabel: modePolicy.label,
    agentModeDescription: modePolicy.description,
    sampleCount: toNumber(getArg('--sample-matches', String(config.automation?.sampleMatches || 8)), 8),
    maxProfiles: toNumber(getArg('--max-profiles', '1'), 1),
    profileScrollSteps: toNumber(getArg('--profile-scroll-steps', String(config.automation?.profileScrollSteps || 3)), 3),
    trustMode: getArg('--trust-mode', config.automation?.trustMode || 'queue'),
    runForever: hasFlag('--run-forever'),
    sleepMs: toNumber(getArg('--sleep-ms', String(config.automation?.runForeverSleepMs || 4000)), 4000),
    tasteRefreshEveryCycles: toNumber(
      getArg('--taste-refresh-every-cycles', String(config.automation?.tasteRefreshEveryCycles || 5)),
      5
    ),
    skipTasteRefresh: hasFlag('--skip-taste-refresh'),
    activeTabs: modePolicy.activeTabs,
    allowReplies: modePolicy.allowReplies,
    allowLikeComments: modePolicy.allowLikeComments,
    allowRoseComments: modePolicy.allowRoseComments,
    allowAutoSendReplies: modePolicy.allowReplies,
    allowAutoSendLikes: modePolicy.allowLikes,
    allowAutoSendRoses: modePolicy.allowRoses,
    allowAutoSkipPasses: config.automation?.allowAutoSkipPasses !== false,
    maxRepliesPerCycle: toNumber(getArg('--max-replies', String(config.automation?.maxRepliesPerCycle || 2)), 2),
    replyCooldownMinutes: toNumber(
      getArg('--reply-cooldown-minutes', String(config.automation?.replyCooldownMinutes || 360)),
      360
    ),
    maxDiscoverProfilesPerCycle: toNumber(
      getArg('--max-discover-profiles', String(config.automation?.maxDiscoverProfilesPerCycle || Math.max(1, toNumber(getArg('--max-profiles', '1'), 1)))),
      Math.max(1, toNumber(getArg('--max-profiles', '1'), 1))
    ),
    maxLikesPerCycle: toNumber(getArg('--max-likes', String(config.automation?.maxLikesPerCycle || 2)), 2),
    maxStandoutsPerCycle: toNumber(getArg('--max-standouts', String(config.automation?.maxStandoutsPerCycle || 1)), 1),
    roseScoreThreshold: toNumber(getArg('--rose-score-threshold', String(config.automation?.roseScoreThreshold || 8)), 8),
    maybeSendScoreThreshold: toNumber(
      getArg('--maybe-send-score-threshold', String(config.automation?.maybeSendScoreThreshold || 5.6)),
      5.6
    ),
    photoLikeTargetRatio: Math.max(
      0,
      Math.min(
        1,
        toNumber(getArg('--photo-like-target-ratio', String(config.automation?.photoLikeTargetRatio || 0.7)), 0.7)
      )
    ),
    likeCommentRatio: Math.max(
      0,
      Math.min(1, toNumber(getArg('--like-comment-ratio', String(config.automation?.likeCommentRatio ?? 0.3)), 0.3))
    ),
    discoverBeautySendThreshold: toNumber(
      getArg('--discover-beauty-send-threshold', String(config.automation?.discoverBeautySendThreshold || 6)),
      6
    ),
    quickScreenBudgetMs: toNumber(
      getArg('--quick-screen-budget-ms', String(config.automation?.quickScreenBudgetMs || 8000)),
      8000
    ),
    defaultSource: config.automation?.defaultSource || 'discover',
    screenActionBudgetMs: toNumber(getArg('--screen-action-budget-ms', '30000'), 30000)
  };
}

function runAgentSweep(workspace, tasteModel, options) {
  const tabs = {};
  const cycleOptions = {
    ...options,
    sweepStartedAt: Date.now()
  };
  updateAgentProgress(workspace, 'Planning sweep', { phase: 'planning' });
  const currentSnapshot = safeSnapshot();
  const currentDiscoverProfileVisible =
    currentSnapshot?.screenType === 'profile' && (!currentSnapshot.currentTab || currentSnapshot.currentTab === 'discover');
  const shouldAttemptChatsFirst =
    options.activeTabs.includes('chats') &&
    remainingBudgetMs(cycleOptions) > 20000 &&
    !currentDiscoverProfileVisible;
  const chatSnapshot = shouldAttemptChatsFirst ? safeEnsureChatList(workspace) : null;
  const planner = planSweep(workspace, cycleOptions, chatSnapshot);
  const orderedTabs = normalizeTabOrder(planner?.orderedTabs, options.activeTabs);

  if (remainingBudgetMs(cycleOptions) > 8000) {
    bootstrapUserProfile(workspace);
  }

  if (currentDiscoverProfileVisible && remainingBudgetMs(cycleOptions) > 0) {
    updateAgentProgress(workspace, `Processing visible profile ${currentSnapshot.currentProfile?.name || ''}`, {
      tab: 'discover',
      phase: 'processing-visible-profile'
    });
    const protectedOptions = {
      ...cycleOptions,
      protectedProfileAnalysis: true,
      quickScreenBudgetMs: Math.min(toNumber(cycleOptions.quickScreenBudgetMs, 8000), 3000)
    };
    const decision = processProfileLikeFlow('discover', workspace, tasteModel, protectedOptions);
    if (decision) {
      tabs.discover = {
        mode: 'visible-profile',
        decisions: [decision]
      };
    }
  }

  for (const tab of orderedTabs) {
    if (budgetExpired(cycleOptions)) {
      updateAgentProgress(workspace, 'Stopped sweep at budget limit', { phase: 'budget-expired' });
      break;
    }
    if (tabs[tab]?.decisions?.length) {
      continue;
    }
    try {
      if (tab === 'chats') {
        if (!chatSnapshot) {
          tabs.chats = { planner, skipped: true, reason: 'unreachable' };
        } else {
          tabs.chats = {
            planner,
            replies: processReplyThreads(workspace, cycleOptions, planner)
          };
        }
        continue;
      }

      if (tab === 'likes') {
        tabs.likes = processLikesTab(workspace, tasteModel, cycleOptions);
        continue;
      }

      if (tab === 'discover') {
        tabs.discover = processDiscoverTab(workspace, tasteModel, cycleOptions);
        continue;
      }

      if (tab === 'standouts') {
        tabs.standouts = processStandoutsTab(workspace, tasteModel, cycleOptions);
      }
    } catch (error) {
      tabs[tab] = {
        mode: 'error',
        decisions: [],
        error: error.message || String(error)
      };
      updateAgentProgress(workspace, `Skipping ${tab} after error`, {
        tab,
        phase: 'tab-error',
        tabError: error.message || String(error)
      });
    }
  }

  const flatDecisions = Object.values(tabs)
    .flatMap((tab) => tab?.decisions || [])
    .map((decision) => ({
      name: decision.name,
      fit: decision.fit,
      score: decision.score,
      beautyScore: decision.beautyScore,
      beautyScoreSource: decision.beautyScoreSource || '',
      compatibilityScore: decision.compatibilityScore,
      commonGround: decision.commonGround || [],
      actionStatus: decision.actionStatus || ''
    }));

  recordActivity(workspace, {
    type: 'sweep',
    title: 'Completed agent sweep',
    summary: `Processed tabs: ${orderedTabs.join(', ')}.`,
    notes: [
      `Agent mode: ${options.agentMode} (${options.agentModeLabel})`,
      `Planner: ${planner?.explanation || 'none'}`,
      `Budget remaining: ${remainingBudgetMs(cycleOptions)}ms`,
      ...flatDecisions.map((decision) => `${decision.name || 'unknown'} -> ${decision.actionStatus || decision.fit || 'reviewed'} (${decision.score ?? 'n/a'})`)
    ]
  });

  saveWorkspace(workspace.paths, workspace.queue, workspace.tasteModel, workspace.threadState, workspace.activityLog);

  return {
    mode: 'complete',
    tabs,
    decisions: flatDecisions
  };
}

async function runContinuousAgent(workspace, options) {
  let tasteModel = workspace.tasteModel;
  let cycle = 0;

  while (true) {
    const shouldRefresh =
      !options.skipTasteRefresh && (cycle === 0 || cycle % Math.max(options.tasteRefreshEveryCycles, 1) === 0);
    if (shouldRefresh) {
      tasteModel = refreshTasteModel(workspace, options.sampleCount, options.profileScrollSteps);
      workspace.tasteModel = tasteModel;
    }

    const result = runAgentSweep(workspace, tasteModel, options);
    const payload = {
      cycle,
      agentMode: options.agentMode,
      agentModeLabel: options.agentModeLabel,
      sampleCount: options.sampleCount,
      profileScrollSteps: options.profileScrollSteps,
      trustMode: options.trustMode,
      photoLikeTargetRatio: options.photoLikeTargetRatio,
      likeCommentRatio: options.likeCommentRatio,
      activeTabs: options.activeTabs,
      tasteSignals: (tasteModel.signals || []).slice(0, 16),
      ...result
    };

    if (!options.runForever || result.mode !== 'complete') {
      return payload;
    }

    cycle += 1;
    await sleep(options.sleepMs);
  }
}

async function main() {
  const dirPath = getArg('--dir', 'hinge-data');
  const workspace = loadWorkspace(dirPath);
  const options = readOptions(workspace.config);

  process.on('SIGINT', () => {
    saveWorkspace(workspace.paths, workspace.queue, workspace.tasteModel, workspace.threadState, workspace.activityLog);
    process.exit(130);
  });

  const result = await runContinuousAgent(workspace, options);
  console.log(JSON.stringify(result, null, 2));
}

main().catch(error => {
  console.error(error.message);
  process.exit(1);
});

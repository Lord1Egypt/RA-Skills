const fs = require('fs');
const path = require('path');

const KNOWN_AGENT_TABS = ['chats', 'likes', 'discover', 'standouts'];
const DEFAULT_AGENT_MODE = 'full_access';
const AGENT_MODE_DEFINITIONS = [
  {
    id: 'like_only',
    label: 'Like Only',
    description: 'Send plain likes and roses only (no chat replies or comments).',
    activeTabs: ['discover', 'likes', 'standouts'],
    allowReplies: false,
    allowLikes: true,
    allowLikeComments: false,
    allowRoses: true,
    allowRoseComments: false
  },
  {
    id: 'full_access',
    label: 'Full Access',
    description: 'Use all tabs with likes, like comments, roses, and chat replies.',
    activeTabs: ['chats', 'likes', 'discover', 'standouts'],
    allowReplies: true,
    allowLikes: true,
    allowLikeComments: true,
    allowRoses: true,
    allowRoseComments: true
  },
  {
    id: 'likes_with_comments_only',
    label: 'Likes + Comments',
    description: 'Send likes (with or without comments) only, no chat replies or roses.',
    activeTabs: ['discover', 'likes'],
    allowReplies: false,
    allowLikes: true,
    allowLikeComments: true,
    allowRoses: false,
    allowRoseComments: false
  }
];

function todayStamp() {
  return new Date().toISOString().slice(0, 10);
}

function nowIso() {
  return new Date().toISOString();
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function readJson(filePath, fallback) {
  if (!fs.existsSync(filePath)) return fallback;
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2) + '\n');
}

function resolvePaths(dirPath) {
  const root = path.resolve(dirPath || 'hinge-data');
  const activityRoot = path.join(root, 'activity');
  const activityDayRoot = path.join(activityRoot, todayStamp());
  return {
    root,
    configPath: path.join(root, 'profile-preferences.json'),
    queuePath: path.join(root, 'queue.json'),
    threadStatePath: path.join(root, 'thread-state.json'),
    markdownPath: path.join(root, `hinge-queue-${todayStamp()}.md`),
    stagedMessagePath: path.join(root, 'staged-message.txt'),
    tasteModelPath: path.join(root, 'taste-model.json'),
    rizzCachePath: path.join(root, 'rizz-cache.json'),
    agentStatePath: path.join(root, 'agent-state.json'),
    agentLogPath: path.join(root, 'agent.log'),
    appiumLogPath: path.join(root, 'appium.log'),
    analysisJsonPath: path.join(root, 'analysis-latest.json'),
    analysisMarkdownPath: path.join(root, 'analysis-latest.md'),
    activityJsonPath: path.join(root, 'activity-log.json'),
    activityMarkdownPath: path.join(root, `activity-log-${todayStamp()}.md`),
    observationPath: path.join(root, 'user-observation.json'),
    activityRoot,
    activityDayRoot,
    activityImagesDir: path.join(activityDayRoot, 'images')
  };
}

function defaultConfig() {
  return {
    user: {
      name: '',
      goals: '',
      tone: 'low-key',
      ageRange: '',
      location: '',
      personalitySummary: '',
      profileSummary: '',
      profilePrompts: [],
      coreInterests: [],
      idealFirstDate: [],
      attractionPreferences: [],
      dealmakerTraits: [],
      dealbreakers: [],
      likesToLeadWith: [],
      observedInterestHints: [],
      chatStyleExamples: [],
      observationSummary: '',
      appearanceCompliments: false
    },
    automation: {
      agentMode: DEFAULT_AGENT_MODE,
      observeBeforeTakeover: true,
      observeWarmupSeconds: 90,
      observeSnapshotIntervalMs: 1500,
      allowComposeFill: false,
      allowAutoSendReplies: false,
      allowAutoSendRoses: false,
      allowAutoSendLikes: true,
      allowAutoSkipPasses: true,
      defaultSource: 'discover',
      activeTabs: ['chats', 'likes', 'discover', 'standouts'],
      trustMode: 'send',
      sampleMatches: 8,
      profileScrollSteps: 3,
      strongYesScoreThreshold: 7,
      maybeScoreThreshold: 5,
      maybeSendScoreThreshold: 5.6,
      photoLikeTargetRatio: 0.7,
      likeCommentRatio: 0.3,
      beautyFloor: 6,
      discoverBeautySendThreshold: 6,
      roseScoreThreshold: 8,
      maxRepliesPerCycle: 2,
      replyCooldownMinutes: 360,
      maxDiscoverProfilesPerCycle: 2,
      maxLikesPerCycle: 2,
      maxStandoutsPerCycle: 1,
      quickScreenBudgetMs: 8000,
      runForeverSleepMs: 4000,
      tasteRefreshEveryCycles: 5
    },
    ai: {
      openaiModel: 'gpt-4.1-mini-2025-04-14',
      plannerModel: 'gpt-4.1-mini-2025-04-14',
      validatorModel: 'gpt-4.1-mini-2025-04-14',
      visionModel: 'gpt-4.1-mini-2025-04-14',
      blockFallback: true,
      useRizzApi: true,
      rizzApiBaseUrl: 'https://rizzapi.vercel.app',
      webValidateBeforeSend: true
    },
    ios: {
      appiumServer: 'http://127.0.0.1:4723',
      deviceName: '',
      platformVersion: '',
      udid: '',
      bundleId: '',
      automationName: 'XCUITest'
    }
  };
}

function defaultQueue() {
  const timestamp = nowIso();
  return {
    createdAt: timestamp,
    updatedAt: timestamp,
    entries: []
  };
}

function defaultActivityLog() {
  const timestamp = nowIso();
  return {
    createdAt: timestamp,
    updatedAt: timestamp,
    entries: []
  };
}

function normalizeFit(value) {
  const raw = String(value || '').trim().toLowerCase();
  if (!raw) return 'maybe';
  if (['strong yes', 'strong-yes', 'yes', 'strong_yes'].includes(raw)) return 'strong yes';
  if (['pass', 'no'].includes(raw)) return 'pass';
  return 'maybe';
}

function normalizeStatus(value) {
  const raw = String(value || '').trim().toLowerCase();
  if (!raw) return 'new';
  const allowed = new Set([
    'new',
    'revisit',
    'passed',
    'staged',
    'approved',
    'sent',
    'replied',
    'archived'
  ]);
  return allowed.has(raw) ? raw : 'new';
}

function slugify(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48);
}

function deriveProfileId(name) {
  return `${slugify(name || 'profile') || 'profile'}-${Date.now()}`;
}

function upsertEntry(queue, entry) {
  const index = queue.entries.findIndex(item => item.profileId === entry.profileId);
  if (index >= 0) {
    queue.entries[index] = {
      ...queue.entries[index],
      ...entry,
      updatedAt: nowIso()
    };
  } else {
    queue.entries.push({
      createdAt: nowIso(),
      updatedAt: nowIso(),
      ...entry
    });
  }
  queue.updatedAt = nowIso();
  return queue;
}

function renderMarkdown(queue) {
  const lines = [];
  lines.push('# Hinge Queue');
  lines.push('');
  lines.push(`Updated: ${queue.updatedAt}`);
  lines.push('');

  const activeEntries = queue.entries.filter(entry => entry.status !== 'archived');
  if (activeEntries.length === 0) {
    lines.push('No queued profiles yet.');
    lines.push('');
    return lines.join('\n');
  }

  lines.push('| Name | Fit | Status | Hook | Best opener | Note |');
  lines.push('| --- | --- | --- | --- | --- | --- |');

  for (const entry of activeEntries) {
    lines.push(
      `| ${escapeCell(entry.name)} | ${escapeCell(entry.fit)} | ${escapeCell(entry.status)} | ${escapeCell(entry.hook)} | ${escapeCell(entry.bestOpener)} | ${escapeCell(entry.note)} |`
    );
  }

  lines.push('');
  return lines.join('\n');
}

function appendActivityEntry(activityLog, entry) {
  const nextEntry = {
    id: entry.id || `${nowIso()}-${Math.random().toString(36).slice(2, 8)}`,
    createdAt: entry.createdAt || nowIso(),
    ...entry
  };
  activityLog.entries.unshift(nextEntry);
  activityLog.entries = activityLog.entries.slice(0, 500);
  activityLog.updatedAt = nowIso();
  return nextEntry;
}

function renderActivityMarkdown(activityLog) {
  const lines = [];
  lines.push('# Hinge Activity');
  lines.push('');
  lines.push(`Updated: ${activityLog.updatedAt}`);
  lines.push('');

  if (!activityLog.entries.length) {
    lines.push('No agent activity yet.');
    lines.push('');
    return lines.join('\n');
  }

  for (const entry of activityLog.entries) {
    const headerBits = [entry.createdAt, entry.type, entry.sourceTab].filter(Boolean).join(' | ');
    lines.push(`## ${entry.title || entry.type || 'Activity'}`);
    lines.push('');
    if (headerBits) {
      lines.push(headerBits);
      lines.push('');
    }
    if (entry.summary) {
      lines.push(entry.summary);
      lines.push('');
    }
    if (entry.name) {
      lines.push(`Name: ${entry.name}`);
    }
    if (entry.fit) {
      lines.push(`Fit: ${entry.fit}`);
    }
    if (entry.actionStatus) {
      lines.push(`Action: ${entry.actionStatus}`);
    }
    if (entry.score !== undefined && entry.score !== null) {
      lines.push(`Score: ${entry.score}`);
    }
    if (entry.beautyScore !== undefined && entry.beautyScore !== null) {
      lines.push(`Beauty: ${entry.beautyScore}`);
    }
    if (entry.compatibilityScore !== undefined && entry.compatibilityScore !== null) {
      lines.push(`Compatibility: ${entry.compatibilityScore}`);
    }
    if (entry.commonGround?.length) {
      lines.push(`Common ground: ${entry.commonGround.join(', ')}`);
    }
    if (entry.message) {
      lines.push(`Message: ${entry.message}`);
    }
    if (entry.imagePath) {
      lines.push(`![${escapeCell(entry.name || entry.title || entry.type || 'activity')}](${entry.imagePath})`);
      lines.push('');
      lines.push(`Image: ${entry.imagePath}`);
    }
    if (entry.notes?.length) {
      lines.push(`Notes: ${entry.notes.join(' | ')}`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

function escapeCell(value) {
  return String(value || '').replace(/\|/g, '\\|').replace(/\n/g, ' ').trim();
}

function normalizeAgentMode(value) {
  const raw = String(value || '')
    .trim()
    .toLowerCase()
    .replace(/[\s-]+/g, '_');

  if (!raw) return DEFAULT_AGENT_MODE;
  if (['1', 'like', 'likes', 'like_only', 'likes_only'].includes(raw)) return 'like_only';
  if (['2', 'full', 'full_access', 'default'].includes(raw)) return 'full_access';
  if (['3', 'likes_with_comments_only', 'likes_with_comments', 'likes_comments', 'likes_comment'].includes(raw)) {
    return 'likes_with_comments_only';
  }
  return AGENT_MODE_DEFINITIONS.some((mode) => mode.id === raw) ? raw : DEFAULT_AGENT_MODE;
}

function sanitizeTabs(preferredTabs) {
  const values = Array.isArray(preferredTabs) ? preferredTabs : [];
  return [...new Set(values.map((tab) => String(tab || '').trim().toLowerCase()).filter((tab) => KNOWN_AGENT_TABS.includes(tab)))];
}

function buildAgentModePolicy(mode, preferredTabs = []) {
  const normalizedMode = normalizeAgentMode(mode);
  const definition =
    AGENT_MODE_DEFINITIONS.find((item) => item.id === normalizedMode) ||
    AGENT_MODE_DEFINITIONS.find((item) => item.id === DEFAULT_AGENT_MODE);

  const preferred = sanitizeTabs(preferredTabs);
  const allowedTabs = new Set(definition.activeTabs);
  const filteredPreferred = preferred.filter((tab) => allowedTabs.has(tab));
  const activeTabs = filteredPreferred.length
    ? definition.activeTabs.filter((tab) => filteredPreferred.includes(tab))
    : [...definition.activeTabs];

  return {
    agentMode: definition.id,
    label: definition.label,
    description: definition.description,
    activeTabs,
    allowReplies: definition.allowReplies,
    allowLikes: definition.allowLikes,
    allowLikeComments: definition.allowLikeComments,
    allowRoses: definition.allowRoses,
    allowRoseComments: definition.allowRoseComments
  };
}

module.exports = {
  AGENT_MODE_DEFINITIONS,
  DEFAULT_AGENT_MODE,
  appendActivityEntry,
  buildAgentModePolicy,
  defaultConfig,
  defaultActivityLog,
  defaultQueue,
  deriveProfileId,
  ensureDir,
  normalizeAgentMode,
  normalizeFit,
  normalizeStatus,
  nowIso,
  readJson,
  renderActivityMarkdown,
  renderMarkdown,
  resolvePaths,
  slugify,
  todayStamp,
  upsertEntry,
  writeJson
};

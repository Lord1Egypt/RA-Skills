#!/usr/bin/env node

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const {
  defaultConfig,
  ensureDir,
  readJson,
  resolvePaths,
  writeJson
} = require('./session-utils');

const args = process.argv.slice(2);
const MAX_WORDS = {
  profile: 14,
  reply: 10,
  rose: 14
};
const CHEESY_RIZZ_TERMS = [
  'wifi',
  'wi-fi',
  'black hole',
  'derivative',
  'sunburn',
  'adenine',
  'nft',
  'screen brightness',
  'algorithm',
  'vision board',
  'chatroom',
  'hello world',
  'i-mac',
  'apple of my'
];
const CHEESY_RIZZ_PATTERNS = [
  /^what'?s a nice girl like you/i,
  /you had me at ["']?hello world/i,
  /you are the apple of my/i,
  /are you a .* because/i
];
const WEB_RIZZ_STYLE_GUIDE = [
  'One punchy sentence only.',
  'Use one specific hook, not a profile recap.',
  'Favor compliment plus twist, observation plus question, or playful challenge.',
  'If complimenting, keep it brief and specific.',
  'Replies should read like a text, not a speech.',
  'Do not jump to date plans, logistics, or mini-itineraries.'
];
const DIRECT_FLIRTY_REFERENCE_LINES = [
  'White looks good on you.',
  'Where you wanna travel baby',
  'I know a guy, but are you a lover girl tho?',
  'Lemme get your number then, make it happen',
  'That should be our 2nd date, who says no?'
];
const WEAK_PROFILE_LINES = new Set([
  'date?',
  'you in?',
  'hey',
  'hi',
  'wyd',
  'what is your best hook here?',
  'okay wait, elaborate?',
  'okay wait, elaborate on that?',
  'really?',
  'what does that mean?'
]);
const PLAN_HEAVY_PATTERNS = [
  /\bdate\b/i,
  /\byou in\b/i,
  /\bwe should\b/i,
  /\blet'?s\b/i,
  /\btake you\b/i,
  /\bspot are we trying\b/i,
  /\bwhat'?s the move\b/i,
  /\bwhen are you free\b/i
];
const RIZZ_CACHE_TTL_MS = 6 * 60 * 60 * 1000;
const FETCH_TIMEOUT_MS = 7000;
const OPENAI_TIMEOUT_MS = 12000;
const WEB_VALIDATION_TIMEOUT_MS = 8000;
const DEFAULT_CHAT_MODEL = process.env.HINGE_DEFAULT_MODEL || 'gpt-4.1-mini-2025-04-14';
const DEFAULT_BASE_MODEL = 'gpt-4.1-mini-2025-04-14';
const DISALLOWED_MODEL_PREFIXES = ['ft:'];
const EMOJI_REGEX = /\p{Extended_Pictographic}/gu;
const FORMAL_PHOTO_PATTERNS = [
  /what inspired your choice/i,
  /inspired your choice/i,
  /choice of (this|that)/i,
  /for the photo/i,
  /for this photo/i,
  /\bstunning\b/i,
  /stunning dress/i,
  /\bwhat inspired\b.*\b(photo|dress|outfit)\b/i
];
const INTERVIEWER_PATTERNS = [
  /what inspired/i,
  /what does .* look like to you/i,
  /can you elaborate/i,
  /tell me more about/i,
  /what made you choose/i,
  /how did you decide/i,
  /for (this|the) photo/i
];
const COMPONENT_ANCHOR_STOP_WORDS = new Set([
  'about',
  'after',
  'again',
  'all',
  'also',
  'and',
  'any',
  'are',
  'back',
  'be',
  'been',
  'being',
  'both',
  'but',
  'can',
  'could',
  'did',
  'do',
  'does',
  'dont',
  'for',
  'from',
  'have',
  'hers',
  'him',
  'his',
  'how',
  'into',
  'its',
  'just',
  'like',
  'more',
  'much',
  'not',
  'one',
  'once',
  'only',
  'over',
  'ours',
  'really',
  'same',
  'some',
  'that',
  'than',
  'the',
  'their',
  'them',
  'then',
  'there',
  'they',
  'thing',
  'this',
  'to',
  'very',
  'want',
  'way',
  'what',
  'when',
  'where',
  'which',
  'who',
  'with',
  'would',
  'year',
  'you',
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

function useBaseModelsOnly() {
  return getArg('--use-base-model-only', process.env.HINGE_USE_BASE_MODELS_ONLY || 'true') !== 'false';
}

function normalizeModelId(value, fallback = DEFAULT_BASE_MODEL) {
  const candidate = String(value || '').trim();
  return candidate || fallback;
}

function isDisallowedModel(model) {
  const normalized = String(model || '').trim().toLowerCase();
  return DISALLOWED_MODEL_PREFIXES.some((prefix) => normalized.startsWith(prefix));
}

function resolveRuntimeModel(requestedModel, fallback = DEFAULT_BASE_MODEL) {
  const candidate = normalizeModelId(requestedModel, fallback);
  if (!useBaseModelsOnly()) return candidate;
  if (isDisallowedModel(candidate)) return fallback;
  return candidate;
}

function analysisModelForMode(mode, preferences) {
  if (mode === 'planner') {
    return resolveRuntimeModel(
      getArg('--planner-model', preferences.ai?.plannerModel || DEFAULT_BASE_MODEL),
      DEFAULT_BASE_MODEL
    );
  }
  return resolveRuntimeModel(
    getArg('--model', preferences.ai?.openaiModel || DEFAULT_CHAT_MODEL),
    DEFAULT_BASE_MODEL
  );
}

function validatorModel(preferences) {
  return resolveRuntimeModel(
    getArg('--validator-model', preferences.ai?.validatorModel || DEFAULT_BASE_MODEL),
    DEFAULT_BASE_MODEL
  );
}

function visionModel(preferences) {
  return resolveRuntimeModel(
    getArg('--vision-model', preferences.ai?.visionModel || DEFAULT_BASE_MODEL),
    DEFAULT_BASE_MODEL
  );
}

function modelSupportsImageInput(model) {
  return !String(model || '').startsWith('ft:');
}

function detectHumanizerCliPath() {
  const codexHome = process.env.CODEX_HOME || path.join(os.homedir(), '.codex');
  const candidates = [
    path.join(codexHome, 'skills', 'ai-humanizer', 'src', 'cli.js'),
    path.join(codexHome, 'skills', 'ai-humanizer-2.1.0', 'src', 'cli.js'),
    path.resolve(__dirname, '..', '..', 'ai-humanizer', 'src', 'cli.js')
  ];
  return candidates.find(candidate => fs.existsSync(candidate)) || '';
}

function humanizerCliPath() {
  const explicitPath = getArg('--humanizer-cli', process.env.HUMANIZER_CLI || '');
  if (explicitPath) return explicitPath;
  return detectHumanizerCliPath();
}

function summarizeHumanizerReport(report) {
  if (!report || typeof report !== 'object') return null;
  return {
    score: Number.isFinite(report.score) ? report.score : null,
    totalIssues: Number.isFinite(report.totalIssues) ? report.totalIssues : null,
    guidance: Array.isArray(report.guidance) ? report.guidance.slice(0, 4) : [],
    styleTips: Array.isArray(report.styleTips) ? report.styleTips.slice(0, 4) : [],
    autofixText: cleanOneLiner(report.autofix?.text || '')
  };
}

function runHumanizerReport(message) {
  const text = cleanOneLiner(message);
  if (!text) return null;
  const cliPath = humanizerCliPath();
  if (!cliPath || !fs.existsSync(cliPath)) return null;

  const result = spawnSync(process.execPath, [cliPath, 'humanize', '--json', '--autofix'], {
    encoding: 'utf-8',
    input: `${text}\n`,
    timeout: 5000
  });

  if (result.error || result.status !== 0) {
    return null;
  }

  const raw = String(result.stdout || '').trim();
  if (!raw) return null;

  try {
    return JSON.parse(raw);
  } catch (error) {
    return null;
  }
}

function applyHumanizerPass(mode, analysis, context) {
  if (!['profile', 'reply', 'rose'].includes(mode)) return analysis;
  const candidate = normalizeAwkwardCompliment(cleanOneLiner(analysis?.recommendedMessage || ''), context);
  if (!candidate) return analysis;
  const report = runHumanizerReport(candidate);
  const summary = summarizeHumanizerReport(report);
  if (!summary) return analysis;

  const rewritten = normalizeAwkwardCompliment(summary.autofixText || candidate, context);
  const backups = [...new Set([rewritten, candidate, ...(analysis.backupMessages || [])].filter(Boolean))]
    .map((line) => normalizeAwkwardCompliment(line, context))
    .filter(Boolean)
    .slice(0, 3);

  return {
    ...analysis,
    recommendedMessage: rewritten,
    backupMessages: backups,
    humanizer: summary
  };
}

function loadConfig(dir) {
  const paths = resolvePaths(dir);
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
    path.resolve(__dirname, '..', '..', '..', 'openclaw.json'),
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

function resolveOpenAiApiKey(preferences) {
  if (typeof process.env.OPENAI_API_KEY === 'string' && process.env.OPENAI_API_KEY.trim()) {
    return process.env.OPENAI_API_KEY.trim();
  }

  const keyCandidates = [
    preferences?.ai?.openaiApiKey,
    preferences?.ai?.openAiApiKey,
    preferences?.ai?.apiKey
  ];
  for (const candidate of keyCandidates) {
    if (typeof candidate === 'string' && candidate.trim().startsWith('sk-')) {
      return candidate.trim();
    }
  }

  return readOpenClawOpenAiApiKey();
}

function getOpenAiApiKey(preferences) {
  const key = resolveOpenAiApiKey(preferences);
  if (key && !process.env.OPENAI_API_KEY) {
    process.env.OPENAI_API_KEY = key;
  }
  return key;
}

function loadContext() {
  const contextFile = getArg('--context-file');
  const inlineContext = getArg('--context-json');

  if (contextFile) {
    return JSON.parse(fs.readFileSync(contextFile, 'utf-8'));
  }

  if (inlineContext) {
    return JSON.parse(inlineContext);
  }

  throw new Error('Missing --context-file or --context-json');
}

function normalizeRizzLine(payload) {
  if (!payload) return '';
  if (typeof payload === 'string') return payload.trim();

  const candidateKeys = ['line', 'pickupLine', 'pickup_line', 'text', 'message', 'quote', 'result'];
  for (const key of candidateKeys) {
    if (typeof payload[key] === 'string' && payload[key].trim()) {
      return payload[key].trim();
    }
  }

  if (payload.data) {
    return normalizeRizzLine(payload.data);
  }

  if (Array.isArray(payload.lines) && payload.lines.length > 0) {
    return normalizeRizzLine(payload.lines[0]);
  }

  return '';
}

async function fetchRizzLines(baseUrl, count) {
  const requests = Array.from({ length: Math.max(0, count) }, async () => {
    const response = await fetch(`${baseUrl.replace(/\/$/, '')}/random`, {
      signal: AbortSignal.timeout(FETCH_TIMEOUT_MS)
    });
    if (!response.ok) {
      throw new Error(`Rizz API failed with HTTP ${response.status}`);
    }
    const payload = await response.json();
    return normalizeRizzLine(payload);
  });

  const settled = await Promise.allSettled(requests);
  return settled
    .filter((item) => item.status === 'fulfilled')
    .map((item) => item.value)
    .filter(Boolean);
}

function readRizzCache(paths) {
  const cache = readJson(paths.rizzCachePath, { updatedAt: '', lines: [] });
  const updatedAt = Date.parse(cache.updatedAt || '');
  if (!Number.isFinite(updatedAt)) return [];
  if (Date.now() - updatedAt > RIZZ_CACHE_TTL_MS) return [];
  return Array.isArray(cache.lines) ? cache.lines.filter(Boolean) : [];
}

function writeRizzCache(paths, lines) {
  writeJson(paths.rizzCachePath, {
    updatedAt: new Date().toISOString(),
    lines: [...new Set((lines || []).filter(Boolean))].slice(0, 24)
  });
}

function summarizeContext(mode, context) {
  if (mode === 'planner') {
    return {
      currentTab: context.currentTab || '',
      activeTabs: context.activeTabs || [],
      visibleThreads: context.visibleThreads || [],
      likesState: context.likesState || '',
      standoutsState: context.standoutsState || '',
      recentActivity: context.recentActivity || [],
      queueSummary: context.queueSummary || {},
      rosesRemaining: context.rosesRemaining ?? null
    };
  }

  if (mode === 'reply') {
    const thread = context.thread || {};
    return {
      name: thread.matchName || context.currentProfile?.name || '',
      threadSummary: (thread.messages || []).map((message) => `${message.side}: ${message.text}`),
      activeSubtab: thread.activeSubtab || '',
      currentTab: context.currentTab || ''
    };
  }

  return {
    name: context.currentProfile?.name || context.thread?.matchName || '',
    prompts: context.prompts || [],
    statusBadges: context.statusBadges || [],
    filters: context.filters || [],
    likedTarget: context.likedTarget || '',
    likedComponent: context.likedComponent || null,
    photoInference: context.photoInference || null,
    sourceTab: context.sourceTab || context.currentTab || '',
    currentTab: context.currentTab || '',
    screenType: context.screenType || ''
  };
}

function extractPreferencePhrases(preferences) {
  const user = preferences.user || {};
  return [
    user.goals || '',
    user.personalitySummary || '',
    user.observationSummary || '',
    user.profileSummary || '',
    ...(user.coreInterests || []),
    ...(user.likesToLeadWith || []),
    ...(user.observedInterestHints || []),
    ...(user.chatStyleExamples || []),
    ...(user.idealFirstDate || []),
    ...(user.attractionPreferences || []),
    ...(user.dealmakerTraits || []),
    ...((user.profilePrompts || []).flatMap((prompt) => [prompt.prompt, prompt.answer]))
  ]
    .map((value) => String(value || '').trim())
    .filter(Boolean);
}

function tokenize(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .map((token) => token.trim())
    .filter((token) => token.length >= 3);
}

function words(value) {
  return String(value || '')
    .trim()
    .split(/\s+/)
    .filter(Boolean);
}

function firstSentence(value) {
  const raw = String(value || '').replace(/\s+/g, ' ').trim();
  if (!raw) return '';
  const match = raw.match(/^(.+?[!?\.])(?:\s|$)/);
  return (match ? match[1] : raw).trim();
}

function stripOuterQuotes(value) {
  return String(value || '')
    .trim()
    .replace(/^["'`]+/, '')
    .replace(/["'`]+$/, '');
}

function cleanOneLiner(value) {
  return stripOuterQuotes(firstSentence(value))
    .replace(/\s+/g, ' ')
    .replace(/\s+([?.!,])/g, '$1')
    .trim();
}

function extractEmojis(value) {
  return [...String(value || '').matchAll(EMOJI_REGEX)].map((match) => match[0]);
}

function stripEmojis(value) {
  return String(value || '')
    .replace(EMOJI_REGEX, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function sparsifyEmojis(value, allowEmoji) {
  const line = cleanOneLiner(value);
  const emojis = extractEmojis(line);
  if (!emojis.length) return line;
  if (!allowEmoji) return cleanOneLiner(stripEmojis(line));
  const base = cleanOneLiner(stripEmojis(line)).replace(/[.!?]+$/, '').trim();
  const one = emojis[0];
  return cleanOneLiner(`${base} ${one}`);
}

function isCheesyRizz(value) {
  const lower = String(value || '').toLowerCase();
  return CHEESY_RIZZ_TERMS.some((term) => lower.includes(term)) || CHEESY_RIZZ_PATTERNS.some((pattern) => pattern.test(String(value || '')));
}

function scoreRizzLine(value) {
  const line = cleanOneLiner(value);
  const count = words(line).length;
  if (!line) return -100;
  let score = 0;
  if (count >= 4 && count <= 11) score += 4;
  if (/[?]/.test(line)) score += 1;
  if (count <= 14) score += 1;
  if (isCheesyRizz(line)) score -= 5;
  return score;
}

function pickRizzExamples(lines, mode) {
  const limit = mode === 'reply' ? 2 : 3;
  return [...new Set((lines || []).map(cleanOneLiner).filter(Boolean))]
    .sort((left, right) => scoreRizzLine(right) - scoreRizzLine(left))
    .filter((line) => !isCheesyRizz(line))
    .slice(0, limit);
}

function clampMessage(value, maxWords) {
  const line = cleanOneLiner(value);
  const tokens = words(line);
  if (tokens.length <= maxWords) return line;
  return `${tokens.slice(0, maxWords).join(' ').replace(/[.,;:!?]+$/, '')}?`.replace(/\?\?+$/, '?');
}

function conciseEnough(value, maxWords) {
  const line = cleanOneLiner(value);
  if (!line) return false;
  if (words(line).length > maxWords) return false;
  if ((line.match(/[?.!]/g) || []).length > 1) return false;
  return true;
}

function compressAnswer(answer) {
  return String(answer || '')
    .replace(/^(a|an|the)\s+/i, '')
    .split(/[,.]/)[0]
    .trim();
}

function likedComponent(context) {
  return context?.likedComponent || null;
}

function hasPhotoLikedComponent(context) {
  const component = likedComponent(context);
  return component?.type === 'photo' || component?.type === 'video';
}

function likedComponentBlob(context) {
  const component = likedComponent(context);
  if (!component) return '';
  return [component.prompt || '', component.answer || '', component.targetLabel || ''].join(' ').trim();
}

function anchorTokensForLikedComponent(context) {
  const component = likedComponent(context);
  if (!component) return [];
  return [
    ...new Set(
      tokenize(likedComponentBlob(context)).filter(
        (token) => token.length >= 3 && !COMPONENT_ANCHOR_STOP_WORDS.has(token)
      )
    )
  ].slice(0, 8);
}

function isAnchoredToLikedComponent(message, context) {
  const component = likedComponent(context);
  if (!component) return true;
  const line = cleanOneLiner(message).toLowerCase();
  if (!line) return false;
  if (component.type === 'photo' || component.type === 'video') {
    return !/letterboxd|tiramisu|lane swim|finance|technology|succession|black mirror/i.test(line);
  }
  const tokens = anchorTokensForLikedComponent(context);
  if (!tokens.length) return true;
  return tokens.some((token) => line.includes(token));
}

function shortAnswerHook(prompt, answer) {
  const promptText = String(prompt || '').toLowerCase();
  const answerText = compressAnswer(answer);
  const blob = `${promptText} ${String(answerText || '').toLowerCase()}`;

  if (/\b(run|running|half|marathon|5k|10k)\b/.test(blob)) return "What's your half-marathon target pace?";
  if (/speak.*fast|fast/.test(blob)) return 'How fast are we talking here?';
  if (/\b(show up|real|guess|feel)\b/.test(blob)) {
    return 'Real and direct? Good, I like that.';
  }
  if (/\b(animal|fight)\b/.test(blob)) return "What's your most realistic animal pick?";
  if (/spontaneous|australia|nothing booked|booked ahead|alone for a month|solo/.test(blob)) {
    return 'Australia solo with nothing booked is wild, why Australia?';
  }
  if (/martini|cocktail|drink/.test(blob)) return 'Pornstar martinis is bold, elite order or chaos pick?';
  if (/table|order for the table|appetizer|share plate/.test(blob)) return 'That table order says trouble, accurate?';
  if (/movie|film|cinema/.test(blob)) return 'Late-night movie pick says a lot, what is it?';
  if (/drive/.test(blob)) return 'Late-night drive where, exactly?';
  if (/music|song|playlist|concert/.test(blob)) return 'What song is definitely on that playlist?';
  if (/travel|trip|passport/.test(blob)) return 'Best trip so far?';
  if (/food|cook|chef|restaurant|dessert|coffee/.test(blob)) return 'What are you weirdly hard to impress with?';
  if (/swim|swimming/.test(blob)) return 'Sprint person or endurance person?';
  const anchors = tokenize(`${answerText} ${promptText}`)
    .filter((token) => token.length >= 3 && !COMPONENT_ANCHOR_STOP_WORDS.has(token))
    .slice(0, 2);
  const anchorLead = anchors[0] || '';
  if (anchorLead) {
    const lead = anchorLead.charAt(0).toUpperCase() + anchorLead.slice(1);
    return `${lead} caught my eye, what's your best story there?`;
  }
  return answerText ? `${answerText} is bold, back that up for me.` : '';
}

function shortPhotoHook(context) {
  const candidates = [
    cleanOneLiner(context.photoInference?.questionHook || ''),
    cleanOneLiner(context.photoInference?.complimentAngle || ''),
    cleanOneLiner(context.photoInference?.visualObservation || '')
  ].filter(Boolean);

  const usableCandidates = candidates.filter(looksLikePhotoMessageLine);

  const complimentFirst = candidates.find(
    (candidate) =>
      looksLikePhotoMessageLine(candidate) &&
      !isFormalPhotoLine(candidate) &&
      !isInterviewerStyleLine(candidate) &&
      /\b(gorgeous|pretty|beautiful|cute|hot|looks good|fire|hard|fit|dress|smile)\b/i.test(candidate)
  );
  if (complimentFirst) return complimentFirst;

  const directStatement = usableCandidates.find(
    (candidate) => !isFormalPhotoLine(candidate) && !isInterviewerStyleLine(candidate) && !/[?]/.test(candidate)
  );
  if (directStatement) return directStatement;

  for (const candidate of usableCandidates) {
    if (isFormalPhotoLine(candidate) || isInterviewerStyleLine(candidate)) continue;
    if (/[?]/.test(candidate)) return candidate;
  }

  const promptBlob = `${context.prompts?.[0]?.prompt || ''} ${context.prompts?.[0]?.answer || ''}`.toLowerCase();
  if (/woke up like this/.test(promptBlob)) return 'Woke up like this is an outrageous claim.';
  if (/golden hour|sunset|beach|ocean/.test(promptBlob)) return 'That lighting is doing a suspicious amount of work.';
  return directPhotoCompliment(context);
}

function shortProfileHook(context) {
  const component = likedComponent(context);
  if (component?.type === 'answer') {
    return shortAnswerHook(component.prompt, component.answer) || '';
  }
  if (component?.type === 'photo' || component?.type === 'video') {
    return shortPhotoHook(context);
  }

  const prompt = (context.prompts || [])[0];
  const answer = compressAnswer(prompt?.answer || '');
  const blob = `${prompt?.prompt || ''} ${answer}`.toLowerCase();

  if (/letterboxd|movie|film|cinema/.test(blob)) return 'Letterboxd top 4? No safe picks.';
  if (/tiramisu|dessert|coffee/.test(blob)) return 'Best tiramisu spot?';
  if (/lane swim|swim|swimming/.test(blob)) return 'Lane swim is elite. Sprint or glide?';
  if (/yearner|mentally/.test(blob)) return 'Define "stimulating," briefly.';
  if (/travel|trip|passport/.test(blob)) return 'Best trip so far?';
  if (/music|concert|playlist/.test(blob)) return 'Best song on repeat?';
  if (/tech|startup|founder|product/.test(blob)) return 'Tech brain, or just pretending?';
  if (/finance|stocks|investing/.test(blob)) return 'Finance girl, or finance meme page?';
  if (/restaurant|foodie|chef|cooking/.test(blob)) return 'Best place you keep gatekept?';
  return '';
}

function shortReplyHook(context) {
  const lastIncoming = [...(context.thread?.messages || [])].find((message) => message.side === 'them');
  const text = String(lastIncoming?.text || '').toLowerCase();
  if (/weekend|outta town|out of town|back/.test(text)) return 'Cute. When are you back?';
  if (/work|busy/.test(text)) return 'Busy, or just mysterious?';
  if (/drink|bar|food|dinner/.test(text)) return 'What is the actual recommendation?';
  if (/start the chat/.test(text)) return '';
  return 'Go on then.';
}

function genericProfileMessage(value) {
  const line = cleanOneLiner(value).toLowerCase();
  const count = words(line).length;
  if (count <= 3) return true;
  if (/^okay\b/.test(line)) return true;
  if (/^(really|seriously)\?*$/.test(line)) return true;
  if (/what does that mean/.test(line)) return true;
  if (/elaborate/.test(line)) return true;
  return WEAK_PROFILE_LINES.has(line);
}

function hasPlanHeavyLanguage(value) {
  return PLAN_HEAVY_PATTERNS.some((pattern) => pattern.test(String(value || '')));
}

function hasCannedStatementLead(value) {
  const line = cleanOneLiner(value).toLowerCase();
  return (
    /^direct energy\b/.test(line) ||
    /^no dodging\b/.test(line) ||
    /^.*\bcaught my eye\b/.test(line) ||
    /\bis attractive,\b/.test(line)
  );
}

function isFormalPhotoLine(value) {
  const line = cleanOneLiner(value);
  return FORMAL_PHOTO_PATTERNS.some((pattern) => pattern.test(line));
}

function isInterviewerStyleLine(value) {
  const line = cleanOneLiner(value);
  return INTERVIEWER_PATTERNS.some((pattern) => pattern.test(line));
}

function hasClearCompliment(value) {
  return /\b(gorgeous|pretty|beautiful|cute|hot|looks good|fire|hard|stunning)\b/i.test(cleanOneLiner(value));
}

function looksLikePhotoMessageLine(value) {
  const line = cleanOneLiner(value);
  if (!line) return false;
  if (words(line).length < 3) return false;
  if (/[?]/.test(line)) return true;
  if (/\b(you|your|look|looks|gorgeous|pretty|beautiful|cute|hot|fire|hard)\b/i.test(line)) return true;
  if (/\b(this|that)\s+(pic|photo|fit|outfit|dress|smile)\b/i.test(line)) return true;
  return false;
}

function directPhotoCompliment(context) {
  const blob = [
    context.photoInference?.visualObservation || '',
    context.photoInference?.complimentAngle || '',
    context.photoInference?.questionHook || '',
    context.prompts?.[0]?.prompt || '',
    context.prompts?.[0]?.answer || '',
    context.likedComponent?.prompt || '',
    context.likedComponent?.answer || ''
  ]
    .join(' ')
    .toLowerCase();

  if (/\bwhite\b/.test(blob)) return 'White looks good on you.';
  if (/\bblack\b/.test(blob)) return 'Black looks good on you.';
  if (/\bred\b/.test(blob)) return 'Red looks good on you.';
  if (/\bblue\b/.test(blob)) return 'Blue looks good on you.';
  if (/dress|fit|outfit/.test(blob)) return 'This looks good on you.';
  if (/smile/.test(blob)) return 'That smile looks dangerous.';
  if (/mirror/.test(blob)) return 'Mirror pic goes hard.';
  if (/golden hour|sunset|beach|ocean/.test(blob)) return 'This pic is doing damage.';
  return 'You look good.';
}

function casualPhotoFallback(context) {
  const direct = directPhotoCompliment(context);
  if (direct) return direct;
  return 'This pic is fire.';
}

function normalizeAwkwardCompliment(value, context) {
  const line = cleanOneLiner(value);
  if (!line) return '';

  if (/\byou look good in this (post|photo|pic)\b/i.test(line)) {
    return hasPhotoLikedComponent(context) ? directPhotoCompliment(context) : 'You look good.';
  }

  if (/\bthis post\b/i.test(line) && /\blooks? good\b/i.test(line)) {
    return hasPhotoLikedComponent(context) ? directPhotoCompliment(context) : 'You look good.';
  }

  if (/\b(stunning|beautiful)\s+photo\b/i.test(line) && /what inspired/i.test(line)) {
    return hasPhotoLikedComponent(context) ? directPhotoCompliment(context) : line;
  }

  return line;
}

function soundsTooFormalForHinge(value) {
  return /\b(resonate|authenticity|demonstrate|mantra|consistency)\b/i.test(String(value || ''));
}

function lacksFlirtySignal(value) {
  const line = cleanOneLiner(value);
  if (!line) return true;
  if (/[?]/.test(line)) return false;
  if (/\b(gorgeous|pretty|beautiful|cute|stunning|hot|wild|bold|elite|chaos|trouble|looks good|goes hard|doing damage)\b/i.test(line)) return false;
  return true;
}

function buildComplimentQuestion(fallback) {
  const question = cleanOneLiner(fallback);
  if (!question) return "You're gorgeous, where was this taken?";
  if (/\b(gorgeous|pretty|beautiful|cute|stunning|hot)\b/i.test(question) && /[?]/.test(question)) {
    return question;
  }
  if (/\b(dress|fit|outfit|photo|pic|mirror)\b/i.test(question)) {
    return "You're gorgeous, where was this taken?";
  }
  if (/[?]/.test(question)) {
    return cleanOneLiner(`You're gorgeous, ${question.replace(/^[A-Z]/, (char) => char.toLowerCase())}`);
  }
  return "You're gorgeous, what's your best story here?";
}

function enforceMessageStyle(mode, analysis, context, preferences, rizzLines) {
  if (!['profile', 'reply', 'rose'].includes(mode)) return analysis;

  const maxWords = MAX_WORDS[mode] || 14;
  const allowFallback = analysis?.allowFallback !== false;
  const component = likedComponent(context);
  const fallback =
    mode === 'reply'
      ? shortReplyHook(context)
      : shortProfileHook(context);

  let recommended = cleanOneLiner(analysis.recommendedMessage || '');
  recommended = normalizeAwkwardCompliment(recommended, context);
  if (!conciseEnough(recommended, maxWords) || (mode !== 'reply' && hasPlanHeavyLanguage(recommended))) {
    recommended = allowFallback ? (fallback || clampMessage(recommended, maxWords)) : clampMessage(recommended, maxWords);
  } else {
    recommended = clampMessage(recommended, maxWords);
  }

  if (!allowFallback) {
    recommended = clampMessage(recommended, maxWords);
    if (mode !== 'reply' && (genericProfileMessage(recommended) || hasPlanHeavyLanguage(recommended))) {
      recommended = '';
    }
    if (mode !== 'reply' && (isInterviewerStyleLine(recommended) || soundsTooFormalForHinge(recommended))) {
      recommended = '';
    }
    if (mode === 'profile' && !isAnchoredToLikedComponent(recommended, context)) {
      recommended = '';
    }
    if (mode === 'profile' && hasPhotoLikedComponent(context) && recommended && !looksLikePhotoMessageLine(recommended) && !/[?]/.test(recommended)) {
      recommended = '';
    }

    const lastIncomingText = [...(context.thread?.messages || [])].find((message) => message.side === 'them')?.text || '';
    const allowEmoji =
      mode === 'reply'
        ? extractEmojis(lastIncomingText).length > 0
        : Boolean(context.photoInference?.complimentAngle && /\b(gorgeous|pretty|beautiful|cute|stunning|hot)\b/i.test(recommended));
    recommended = sparsifyEmojis(recommended, allowEmoji);

    const backups = [...(analysis.backupMessages || [])]
      .map((line) => clampMessage(line, maxWords))
      .map(cleanOneLiner)
      .map((line) => normalizeAwkwardCompliment(line, context))
      .filter(Boolean)
      .filter((line) => !isCheesyRizz(line))
      .filter((line) => !isInterviewerStyleLine(line))
      .filter((line) => !(mode === 'profile' && hasPhotoLikedComponent(context) && isFormalPhotoLine(line)));

    return {
      ...analysis,
      recommendedMessage: recommended,
      backupMessages: [...new Set(backups)].slice(0, 3),
      styleGuide: WEB_RIZZ_STYLE_GUIDE
    };
  }

  if (isInterviewerStyleLine(recommended) || soundsTooFormalForHinge(recommended)) {
    recommended = fallback || recommended;
  }

  if (mode === 'profile' && !isAnchoredToLikedComponent(recommended, context)) {
    recommended = fallback || recommended;
  }

  if (mode !== 'reply' && (genericProfileMessage(recommended) || hasPlanHeavyLanguage(recommended))) {
    recommended = fallback || recommended;
  }

  if (mode === 'profile' && hasCannedStatementLead(recommended) && fallback) {
    recommended = clampMessage(fallback, maxWords);
  }

  if (mode === 'profile' && component?.type === 'answer' && (soundsTooFormalForHinge(recommended) || isInterviewerStyleLine(recommended)) && fallback) {
    recommended = clampMessage(fallback, maxWords);
  }

  if (mode === 'profile' && hasPhotoLikedComponent(context) && (isFormalPhotoLine(recommended) || isInterviewerStyleLine(recommended))) {
    recommended = clampMessage(directPhotoCompliment(context), maxWords);
  }

  if (mode === 'profile' && hasPhotoLikedComponent(context) && !hasClearCompliment(recommended) && !/[?]/.test(recommended)) {
    recommended = clampMessage(casualPhotoFallback(context), maxWords);
  }

  if (mode !== 'reply' && lacksFlirtySignal(recommended) && fallback) {
    recommended = clampMessage(hasPhotoLikedComponent(context) ? directPhotoCompliment(context) : fallback, maxWords);
  }

  if (mode === 'profile' && hasPhotoLikedComponent(context) && context.photoInference) {
    const lower = recommended.toLowerCase();
    const observation = String(context.photoInference.visualObservation || '').toLowerCase();
    const observationTokens = tokenize(observation).slice(0, 5);
    const referencesPhotoDetail = observationTokens.some((token) => lower.includes(token));
    if (!referencesPhotoDetail && fallback) {
      recommended = clampMessage(fallback, maxWords);
    }
  }

  if (mode !== 'reply' && preferences.user?.appearanceCompliments && analysis.visualAttractionScore >= 8) {
    if (hasPhotoLikedComponent(context)) {
      if (!hasClearCompliment(recommended)) {
        recommended = clampMessage(directPhotoCompliment(context), maxWords);
      }
    } else if (!/[?]/.test(recommended) || !/\b(gorgeous|pretty|beautiful|cute|stunning|hot)\b/i.test(recommended)) {
      recommended = clampMessage(buildComplimentQuestion(fallback || recommended), maxWords);
    }
  }

  if (mode === 'profile' && hasPhotoLikedComponent(context) && !isAnchoredToLikedComponent(recommended, context)) {
    recommended = clampMessage(directPhotoCompliment(context), maxWords);
  }

  if (mode !== 'reply' && isInterviewerStyleLine(recommended)) {
    recommended = clampMessage(hasPhotoLikedComponent(context) ? directPhotoCompliment(context) : fallback || recommended, maxWords);
  }

  const lastIncomingText = [...(context.thread?.messages || [])].find((message) => message.side === 'them')?.text || '';
  const allowEmoji =
    mode === 'reply'
      ? extractEmojis(lastIncomingText).length > 0
      : Boolean(context.photoInference?.complimentAngle && /\b(gorgeous|pretty|beautiful|cute|stunning|hot)\b/i.test(recommended));
  recommended = sparsifyEmojis(recommended, allowEmoji);

  const backups = [...(analysis.backupMessages || []), fallback]
    .map((line) => clampMessage(line, maxWords))
    .map(cleanOneLiner)
    .map((line) => normalizeAwkwardCompliment(line, context))
    .filter(Boolean)
    .filter((line) => !isCheesyRizz(line))
    .filter((line) => !isInterviewerStyleLine(line))
    .filter((line) => !(mode === 'profile' && hasPhotoLikedComponent(context) && isFormalPhotoLine(line)));

  return {
    ...analysis,
    recommendedMessage: recommended,
    backupMessages: [...new Set(backups)].slice(0, 3),
    styleGuide: WEB_RIZZ_STYLE_GUIDE
  };
}

function buildProfileFallbackScores(context, preferences) {
  const preferencePhrases = extractPreferencePhrases(preferences);
  const candidateTexts = [
    ...((context.prompts || []).flatMap((prompt) => [prompt.prompt, prompt.answer])),
    ...(context.filters || []),
    ...(context.statusBadges || [])
  ]
    .map((value) => String(value || '').trim())
    .filter(Boolean);
  const candidateBlob = candidateTexts.join(' ').toLowerCase();
  const commonGround = preferencePhrases.filter((phrase) => candidateBlob.includes(phrase.toLowerCase())).slice(0, 6);
  const candidateTokens = new Set(tokenize(candidateTexts.join(' ')));
  const sharedTokens = tokenize(preferencePhrases.join(' ')).filter((token) => candidateTokens.has(token));
  const compatibilityScore = Math.max(3, Math.min(9, 4 + commonGround.length + Math.ceil(sharedTokens.length / 2)));
  const profileQualityScore = Math.max(
    4,
    Math.min(9, 4 + Math.min(3, (context.prompts || []).length) + Math.min(2, (context.statusBadges || []).length))
  );
  const sourceTab = context.sourceTab || context.currentTab || '';
  const visualAttractionScore = Math.max(
    5,
    Math.min(9, sourceTab === 'standouts' ? 8 : sourceTab === 'likes' ? 7 : 6)
  );

  return {
    commonGround,
    sharedTokens: [...new Set(sharedTokens)].slice(0, 10),
    compatibilityScore,
    profileQualityScore,
    visualAttractionScore
  };
}

function heuristicMessage(mode, context, rizzLines) {
  if (mode === 'planner') {
    return '';
  }

  if (mode === 'reply') {
    return shortReplyHook(context) || 'Go on then.';
  }

  if (hasPhotoLikedComponent(context)) {
    return shortProfileHook(context) || directPhotoCompliment(context);
  }

  return shortProfileHook(context) || '';
}

function buildFallbackAnalysis(mode, context, rizzLines, preferences) {
  const summaryContext = summarizeContext(mode, context);
  if (mode === 'planner') {
    const visibleThreads = summaryContext.visibleThreads || [];
    const prioritizedThreads = visibleThreads
      .filter((thread) => thread.section?.startsWith('Your turn') || thread.section?.startsWith('Hidden'))
      .slice(0, 5)
      .map((thread) => thread.name);
    const orderedTabs = ['chats', 'likes', 'discover', 'standouts'].filter((tab) =>
      (summaryContext.activeTabs || []).includes(tab)
    );

    return {
      mode,
      source: 'fallback',
      summary: `Planned next sweep using ${visibleThreads.length} visible chat thread(s).`,
      orderedTabs,
      replyTargets: prioritizedThreads,
      refreshTaste: visibleThreads.some((thread) => !thread.isStarter),
      explanation: 'Prioritizes visible chats first, including hidden chats, then the remaining active tabs.'
    };
  }

  const summary =
    mode === 'reply'
      ? `Visible thread with ${summaryContext.name || 'this match'} and ${summaryContext.threadSummary?.length || 0} recent messages.`
      : `Visible profile for ${summaryContext.name || 'this match'} with ${summaryContext.prompts?.length || 0} prompt hooks.`;

  const recommendedMessage = heuristicMessage(mode, context, rizzLines);
  const backupCandidates =
    mode === 'reply'
      ? [shortReplyHook(context), 'Go on then.']
      : hasPhotoLikedComponent(context)
        ? [directPhotoCompliment(context), casualPhotoFallback(context)]
        : [shortProfileHook(context)];
  const backupMessages = [...new Set([recommendedMessage, ...backupCandidates].map(cleanOneLiner).filter(Boolean))].slice(0, 3);

  const fallback = {
    mode,
    source: 'fallback',
    summary,
    signals:
      mode === 'reply'
        ? summaryContext.threadSummary?.slice(-3) || []
        : (summaryContext.prompts || []).map((prompt) => `${prompt.prompt}: ${prompt.answer}`),
    risks: [],
    recommendedMessage,
    backupMessages,
    explanation:
      mode === 'reply'
        ? 'Keeps the existing thread moving without resetting the tone.'
        : 'References visible profile details and asks one easy follow-up.',
    rizzReferences: rizzLines
  };

  if (mode !== 'reply') {
    const profileScores = buildProfileFallbackScores(context, preferences);
    return {
      ...fallback,
      commonGround: profileScores.commonGround,
      compatibilityScore: profileScores.compatibilityScore,
      profileQualityScore: profileScores.profileQualityScore,
      visualAttractionScore: profileScores.visualAttractionScore,
      dealbreakerHit: false
    };
  }

  return fallback;
}

function buildOpenAiPrompts(mode, context, preferences, rizzLines) {
  if (mode === 'planner') {
    const system = [
      'You plan the next Hinge agent actions.',
      'Prioritize meaningful progress, not random navigation.',
      'Do not ignore visible hidden chats.',
      'Never recommend replying again if our side was the last to text.',
      'Return a compact plan for tab order, reply targets, and whether to refresh taste from match profiles.'
    ].join(' ');

    const user = JSON.stringify(
      {
        mode,
        preferences: {
          tone: preferences.user?.tone || 'low-key',
          goals: preferences.user?.goals || ''
        },
        context: summarizeContext(mode, context)
      },
      null,
      2
    );

    return { system, user };
  }

  const system = [
    'You write Hinge comments and replies.',
    'Default voice: playful, flirty, confident, and specific.',
    'Avoid flat, corporate, therapist-like, interviewer, or reporter phrasing.',
    'Use only visible profile or thread context.',
    'Do not invent shared history, facts, or plans.',
    'Return strict JSON matching the schema.',
    'RecommendedMessage must be one sentence only.',
    'Profile openers must usually be 5 to 14 words. Replies must usually be 3 to 10 words.',
    'Never write a paragraph, speech, recap, or two-part essay.',
    'Use one of these shapes: compliment plus twist, observation plus quick question, playful challenge.',
    'Prefer flirty banter over neutral Q&A whenever possible.',
    'Do not ask interview-style questions like "what inspired your choice" or "can you elaborate".',
    'Keep wording casual and conversational, not corporate or therapy-like.',
    'Never use generic fillers like "really?", "what does that mean?", or "elaborate".',
    'Use at most one hook. Do not stack multiple prompts or themes into one line.',
    'For initial likes, prefer a brief compliment, a shared-interest hook, or a specific question tied to the liked prompt or photo.',
    'For photo likes, default to a short direct compliment first; question is optional.',
    'If a likedTarget is provided, anchor the message to that exact component.',
    'If likedComponent.type is answer, the message must clearly relate to likedComponent.answer or likedComponent.prompt.',
    'If likedComponent.type is photo or video, the message must relate to the image, vibe, or composition, not a different prompt.',
    'If likedComponent.type is photo or video and photoInference is provided, use at least one concrete visual detail from photoInference.',
    'Do not pivot from likedTarget into a different prompt or topic.',
    'Do not suggest a date, itinerary, meetup, or logistics unless they already raised it first.',
    'Do not repeat the whole prompt answer back to them.',
    'If they are visually striking and the image clearly supports it, a very short compliment is allowed.',
    'If there is a specific hook on the profile, use it briefly and directly.',
    'Emoji policy: most messages should have no emoji. If used, max one emoji at the end.',
    'If rizz examples are provided, treat them only as inspiration and do not copy them verbatim.',
    `Style anchors for cadence only (do not copy verbatim): ${DIRECT_FLIRTY_REFERENCE_LINES.join(' | ')}`
  ].join(' ');

  const user = JSON.stringify(
    {
      mode,
      preferences: {
        tone: preferences.user?.tone || 'sharp-flirty',
        goals: preferences.user?.goals || '',
        personalitySummary: preferences.user?.personalitySummary || '',
        observationSummary: preferences.user?.observationSummary || '',
        dealbreakers: preferences.user?.dealbreakers || [],
        likesToLeadWith: preferences.user?.likesToLeadWith || [],
        observedInterestHints: preferences.user?.observedInterestHints || [],
        profileSummary: preferences.user?.profileSummary || '',
        profilePrompts: preferences.user?.profilePrompts || [],
        coreInterests: preferences.user?.coreInterests || [],
        idealFirstDate: preferences.user?.idealFirstDate || [],
        attractionPreferences: preferences.user?.attractionPreferences || [],
        dealmakerTraits: preferences.user?.dealmakerTraits || [],
        appearanceCompliments: preferences.user?.appearanceCompliments || false
      },
      context: summarizeContext(mode, context),
      constraints: {
        maxWords: MAX_WORDS[mode] || 14,
        anchorTokens: anchorTokensForLikedComponent(context),
        oneSentenceOnly: true,
        oneHookOnly: true
      },
      promptChain: {
        step: 'draft',
        next: ['rewrite', 'humanize', 'quality-gate']
      },
      styleGuide: WEB_RIZZ_STYLE_GUIDE,
      rizzExamples: pickRizzExamples(rizzLines, mode),
      hardStyleRules: [
        'Direct and playful, never interviewer or reporter tone.',
        'Tease lightly when possible; never pander.',
        'One sentence only, no paragraph energy.',
        'For photo likes, short compliment-first comments are preferred.'
      ],
      styleAnchors: DIRECT_FLIRTY_REFERENCE_LINES,
      userChatStyleExamples: preferences.user?.chatStyleExamples || []
    },
    null,
    2
  );

  return { system, user };
}

function extractWebSources(payload) {
  const sources = [];
  for (const item of payload.output || []) {
    if (item.type !== 'web_search_call') continue;
    for (const source of item.action?.sources || []) {
      if (!source?.url) continue;
      sources.push({
        title: source.title || '',
        url: source.url
      });
    }
  }
  return [...new Map(sources.map((source) => [source.url, source])).values()].slice(0, 6);
}

async function fetchPhotoInference(context, preferences, screenshotFile) {
  const apiKey = getOpenAiApiKey(preferences);
  if (!apiKey || !screenshotFile || !fs.existsSync(screenshotFile) || !hasPhotoLikedComponent(context)) {
    return null;
  }

  const model = visionModel(preferences);
  const response = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey}`
    },
    signal: AbortSignal.timeout(OPENAI_TIMEOUT_MS),
    body: JSON.stringify({
      model,
      input: [
        {
          role: 'system',
          content: [
            {
              type: 'input_text',
              text: [
                'You analyze a dating profile photo for message writing.',
                'Return concise, concrete visual details and one playful hook.',
                'Do not infer protected traits or sensitive attributes.'
              ].join(' ')
            }
          ]
        },
        {
          role: 'user',
          content: [
            {
              type: 'input_text',
              text: JSON.stringify(
                {
                  task: 'Describe visible image details useful for a short, respectful compliment or question.',
                  likedComponent: context.likedComponent || null,
                  visiblePrompts: context.prompts || []
                },
                null,
                2
              )
            },
            {
              type: 'input_image',
              image_url: `data:image/png;base64,${fs.readFileSync(screenshotFile, 'base64')}`
            }
          ]
        }
      ],
      text: {
        format: {
          type: 'json_schema',
          name: 'photo_inference',
          schema: {
            type: 'object',
            additionalProperties: false,
            properties: {
              visualObservation: { type: 'string' },
              complimentAngle: { type: 'string' },
              questionHook: { type: 'string' },
              visualAttractionScoreEstimate: {
                anyOf: [{ type: 'integer', minimum: 1, maximum: 10 }, { type: 'null' }]
              }
            },
            required: ['visualObservation', 'complimentAngle', 'questionHook', 'visualAttractionScoreEstimate']
          }
        }
      }
    })
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Photo inference failed with HTTP ${response.status}: ${errorBody}`);
  }

  const payload = await response.json();
  const parsed = JSON.parse(extractResponseText(payload) || '{}');
  return {
    visualObservation: cleanOneLiner(parsed.visualObservation || ''),
    complimentAngle: cleanOneLiner(parsed.complimentAngle || ''),
    questionHook: cleanOneLiner(parsed.questionHook || ''),
    visualAttractionScoreEstimate: Number.isFinite(Number(parsed.visualAttractionScoreEstimate))
      ? Math.max(1, Math.min(10, Math.round(Number(parsed.visualAttractionScoreEstimate))))
      : null
  };
}

async function validateMessageWithWebSearch(mode, analysis, context, preferences) {
  const apiKey = getOpenAiApiKey(preferences);
  const priorCandidate = cleanOneLiner(analysis.candidateMessage || '');
  const modelDraft = cleanOneLiner(analysis.recommendedMessage || '');
  const candidate = modelDraft || priorCandidate;
  const humanizerSummary = analysis.humanizer || summarizeHumanizerReport(runHumanizerReport(candidate));
  const humanizedCandidate = cleanOneLiner(humanizerSummary?.autofixText || '');
  const effectiveCandidate = humanizedCandidate || candidate;
  if (!apiKey || !candidate || !['profile', 'reply', 'rose'].includes(mode)) {
    return analysis;
  }

  const maxWords = MAX_WORDS[mode] || 14;
  const model = validatorModel(preferences);
  const response = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey}`
    },
    signal: AbortSignal.timeout(OPENAI_TIMEOUT_MS),
    body: JSON.stringify({
      model,
      tools: [
        {
          type: 'web_search'
        }
      ],
      tool_choice: 'auto',
      include: ['web_search_call.action.sources'],
      input: [
        {
          role: 'system',
          content: [
            {
              type: 'input_text',
              text: [
                'You are a final-pass Hinge message editor.',
                'Do a brief web search for examples or advice on short, punchy flirting or dating-app openers.',
                'Then approve or rewrite the candidate message so it feels sharp, concise, and current.',
                'Keep the tone flirty and playful, not neutral, formal, interviewer-like, or reporter-like.',
                'You may receive a humanizer report with rewrite guidance; use it when useful.',
                'You can fully rewrite the candidate when it improves fit, tone, and relevance.',
                'Keep it to one sentence.',
                'Profile and rose comments should stay under 14 words. Replies should stay under 10 words.',
                'Use only one hook. If the candidate stacks multiple hooks, cut it to the strongest one.',
                'If likedTarget is present, keep the line anchored to that liked component.',
                'Do not switch from likedTarget to a different prompt or topic.',
                'Do not make plans, pitch a date, propose logistics, or write a paragraph.',
                'Avoid interview templates like "what inspired your choice" and "can you elaborate".',
                'Use emoji rarely: usually none, at most one if it clearly fits.',
                'Prefer editorial or advice sources over Reddit or pickup-line dump pages.',
                'You may receive both a modelDraftMessage and a priorCandidateMessage. Pick or rewrite the stronger one.',
                'Prefer a brief direct compliment if the person is visually striking, otherwise use a specific hook or shared interest plus a quick question.',
                'When likedComponent exists, final output must match that exact liked component.',
                `Style anchors for cadence only (do not copy verbatim): ${DIRECT_FLIRTY_REFERENCE_LINES.join(' | ')}`
              ].join(' ')
            }
          ]
        },
        {
          role: 'user',
          content: [
            {
              type: 'input_text',
              text: JSON.stringify(
                {
                  mode,
                  modelDraftMessage: modelDraft,
                  priorCandidateMessage: priorCandidate,
                  humanizedCandidateMessage: humanizedCandidate || null,
                  humanizer: humanizerSummary,
                  context: summarizeContext(mode, context),
                  preferences: {
                    tone: preferences.user?.tone || 'sharp-flirty',
                    goals: preferences.user?.goals || '',
                    personalitySummary: preferences.user?.personalitySummary || '',
                    observationSummary: preferences.user?.observationSummary || '',
                    coreInterests: preferences.user?.coreInterests || [],
                    likesToLeadWith: preferences.user?.likesToLeadWith || [],
                    observedInterestHints: preferences.user?.observedInterestHints || [],
                    appearanceCompliments: preferences.user?.appearanceCompliments || false
                  },
                  styleGuide: WEB_RIZZ_STYLE_GUIDE,
                  hardStyleRules: [
                    'Direct and playful, never interviewer or reporter tone.',
                    'Tease lightly when possible; never pander.',
                    'One sentence only, no paragraph energy.',
                    'For photo likes, short compliment-first comments are preferred.'
                  ],
                  styleAnchors: DIRECT_FLIRTY_REFERENCE_LINES,
                  userChatStyleExamples: preferences.user?.chatStyleExamples || []
                },
                null,
                2
              )
            }
          ]
        }
      ],
      text: {
        format: {
          type: 'json_schema',
          name: 'hinge_web_validation',
          schema: {
            type: 'object',
            additionalProperties: false,
            properties: {
              approvedMessage: { type: 'string' },
              reason: { type: 'string' },
              checks: {
                type: 'array',
                items: { type: 'string' }
              }
            },
            required: ['approvedMessage', 'reason', 'checks']
          }
        }
      }
    })
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`OpenAI web validation failed with HTTP ${response.status}: ${errorBody}`);
  }

  const payload = await response.json();
  const parsed = JSON.parse(extractResponseText(payload) || '{}');
  const lastIncomingText = [...(context.thread?.messages || [])].find((message) => message.side === 'them')?.text || '';
  const allowEmoji =
    mode === 'reply'
      ? extractEmojis(lastIncomingText).length > 0
      : Boolean(context.photoInference?.complimentAngle && /\b(gorgeous|pretty|beautiful|cute|stunning|hot)\b/i.test(parsed.approvedMessage || effectiveCandidate));
  const approvedMessage = sparsifyEmojis(clampMessage(parsed.approvedMessage || effectiveCandidate, maxWords), allowEmoji);

  return {
    ...analysis,
    recommendedMessage: approvedMessage,
    backupMessages: [...new Set([approvedMessage, effectiveCandidate, modelDraft, priorCandidate, ...(analysis.backupMessages || [])].filter(Boolean))].slice(0, 3),
    humanizer: humanizerSummary || analysis.humanizer || null,
    webValidation: {
      reason: parsed.reason || '',
      checks: parsed.checks || [],
      sources: extractWebSources(payload)
    }
  };
}

async function chainModelRewrite(mode, analysis, context, preferences) {
  if (!['profile', 'reply', 'rose'].includes(mode)) return analysis;
  const apiKey = getOpenAiApiKey(preferences);
  const candidate = cleanOneLiner(analysis?.recommendedMessage || '');
  if (!apiKey || !candidate) return analysis;

  const model = analysisModelForMode(mode, preferences);
  const maxWords = MAX_WORDS[mode] || 14;
  const response = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey}`
    },
    signal: AbortSignal.timeout(OPENAI_TIMEOUT_MS),
    body: JSON.stringify({
      model,
      input: [
        {
          role: 'system',
          content: [
            {
              type: 'input_text',
              text: [
                'You are a rewrite pass for Hinge lines.',
                'Upgrade specificity, flirt energy, and relevance to the liked component.',
                'Never switch topics away from likedComponent.',
                'One sentence only.',
                'No interviewer language, no formal language, no date logistics.',
                'No filler lines like "really?", "elaborate", or "what does that mean?".',
                'Use one hook only.',
                `Word limit: ${maxWords}.`,
                'Return concise JSON.'
              ].join(' ')
            }
          ]
        },
        {
          role: 'user',
          content: [
            {
              type: 'input_text',
              text: JSON.stringify(
                {
                  mode,
                  candidate,
                  backups: analysis.backupMessages || [],
                  context: summarizeContext(mode, context),
                  constraints: {
                    maxWords,
                    anchorTokens: anchorTokensForLikedComponent(context),
                    oneHookOnly: true,
                    oneSentenceOnly: true
                  },
                  promptChain: {
                    step: 'rewrite',
                    next: ['humanize', 'quality-gate']
                  },
                  styleGuide: WEB_RIZZ_STYLE_GUIDE,
                  styleAnchors: DIRECT_FLIRTY_REFERENCE_LINES
                },
                null,
                2
              )
            }
          ]
        }
      ],
      text: {
        format: {
          type: 'json_schema',
          name: 'hinge_chain_rewrite',
          schema: {
            type: 'object',
            additionalProperties: false,
            properties: {
              recommendedMessage: { type: 'string' },
              backupMessages: {
                type: 'array',
                items: { type: 'string' }
              },
              reason: { type: 'string' }
            },
            required: ['recommendedMessage', 'backupMessages', 'reason']
          }
        }
      }
    })
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Chain rewrite failed with HTTP ${response.status}: ${errorBody}`);
  }

  const payload = await response.json();
  const parsed = JSON.parse(extractResponseText(payload) || '{}');
  const recommendedMessage = clampMessage(cleanOneLiner(parsed.recommendedMessage || candidate), maxWords);
  const backupMessages = [...new Set([recommendedMessage, ...(parsed.backupMessages || []), ...(analysis.backupMessages || [])].map(cleanOneLiner).filter(Boolean))].slice(0, 3);

  return {
    ...analysis,
    recommendedMessage,
    backupMessages,
    chainRewrite: {
      reason: parsed.reason || '',
      model
    }
  };
}

async function chainQualityGate(mode, analysis, context, preferences) {
  if (!['profile', 'reply', 'rose'].includes(mode)) return analysis;
  const apiKey = getOpenAiApiKey(preferences);
  const candidate = cleanOneLiner(analysis?.recommendedMessage || '');
  if (!apiKey || !candidate) return analysis;

  const model = validatorModel(preferences);
  const maxWords = MAX_WORDS[mode] || 14;
  const response = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey}`
    },
    signal: AbortSignal.timeout(OPENAI_TIMEOUT_MS),
    body: JSON.stringify({
      model,
      input: [
        {
          role: 'system',
          content: [
            {
              type: 'input_text',
              text: [
                'You are the final quality gate for a Hinge message.',
                'Keep one sentence only.',
                'Keep it playful, flirty, and specific.',
                'No interview style, no formal tone, no date logistics.',
                'No generic fillers like "really?" or "what does that mean?".',
                'If likedComponent exists, line must match that exact component.',
                `Hard word limit: ${maxWords}.`,
                'Return strict JSON.'
              ].join(' ')
            }
          ]
        },
        {
          role: 'user',
          content: [
            {
              type: 'input_text',
              text: JSON.stringify(
                {
                  mode,
                  candidate,
                  context: summarizeContext(mode, context),
                  constraints: {
                    maxWords,
                    anchorTokens: anchorTokensForLikedComponent(context),
                    oneHookOnly: true,
                    oneSentenceOnly: true
                  },
                  styleGuide: WEB_RIZZ_STYLE_GUIDE
                },
                null,
                2
              )
            }
          ]
        }
      ],
      text: {
        format: {
          type: 'json_schema',
          name: 'hinge_quality_gate',
          schema: {
            type: 'object',
            additionalProperties: false,
            properties: {
              approvedMessage: { type: 'string' },
              reason: { type: 'string' }
            },
            required: ['approvedMessage', 'reason']
          }
        }
      }
    })
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Quality gate failed with HTTP ${response.status}: ${errorBody}`);
  }

  const payload = await response.json();
  const parsed = JSON.parse(extractResponseText(payload) || '{}');
  const approvedMessage = clampMessage(cleanOneLiner(parsed.approvedMessage || candidate), maxWords);
  const backupMessages = [...new Set([approvedMessage, candidate, ...(analysis.backupMessages || [])].map(cleanOneLiner).filter(Boolean))].slice(0, 3);

  return {
    ...analysis,
    recommendedMessage: approvedMessage,
    backupMessages,
    qualityGate: {
      reason: parsed.reason || '',
      model
    }
  };
}

function extractResponseText(payload) {
  if (typeof payload.output_text === 'string' && payload.output_text.trim()) {
    return payload.output_text.trim();
  }

  const chunks = [];
  for (const item of payload.output || []) {
    for (const content of item.content || []) {
      if (content.type === 'output_text' && typeof content.text === 'string') {
        chunks.push(content.text);
      }
    }
  }
  return chunks.join('\n').trim();
}

async function fetchOpenAiAnalysis(mode, context, preferences, rizzLines) {
  const apiKey = getOpenAiApiKey(preferences);
  if (!apiKey) {
    throw new Error('Missing OPENAI_API_KEY');
  }

  const { system, user } = buildOpenAiPrompts(mode, context, preferences, rizzLines);
  const model = analysisModelForMode(mode, preferences);
  const screenshotFile = getArg('--screenshot-file');
  const attachImage = screenshotFile && fs.existsSync(screenshotFile) && modelSupportsImageInput(model);
  const schema =
    mode === 'planner'
      ? {
          type: 'object',
          additionalProperties: false,
          properties: {
            mode: { type: 'string' },
            summary: { type: 'string' },
            orderedTabs: {
              type: 'array',
              items: { type: 'string' }
            },
            replyTargets: {
              type: 'array',
              items: { type: 'string' }
            },
            refreshTaste: { type: 'boolean' },
            explanation: { type: 'string' }
          },
          required: ['mode', 'summary', 'orderedTabs', 'replyTargets', 'refreshTaste', 'explanation']
        }
      : {
          type: 'object',
          additionalProperties: false,
          properties: {
            mode: { type: 'string' },
            summary: { type: 'string' },
            signals: {
              type: 'array',
              items: { type: 'string' }
            },
            risks: {
              type: 'array',
              items: { type: 'string' }
            },
            recommendedMessage: { type: 'string' },
            visualAttractionScore: {
              anyOf: [
                { type: 'integer', minimum: 1, maximum: 10 },
                { type: 'null' }
              ]
            },
            compatibilityScore: {
              anyOf: [
                { type: 'integer', minimum: 1, maximum: 10 },
                { type: 'null' }
              ]
            },
            profileQualityScore: {
              anyOf: [
                { type: 'integer', minimum: 1, maximum: 10 },
                { type: 'null' }
              ]
            },
            commonGround: {
              anyOf: [
                {
                  type: 'array',
                  items: { type: 'string' }
                },
                { type: 'null' }
              ]
            },
            dealbreakerHit: {
              anyOf: [
                { type: 'boolean' },
                { type: 'null' }
              ]
            },
            backupMessages: {
              type: 'array',
              items: { type: 'string' }
            },
            explanation: { type: 'string' }
          },
          required: [
            'mode',
            'summary',
            'signals',
            'risks',
            'recommendedMessage',
            'visualAttractionScore',
            'compatibilityScore',
            'profileQualityScore',
            'commonGround',
            'dealbreakerHit',
            'backupMessages',
            'explanation'
          ]
        };

  const response = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey}`
    },
    signal: AbortSignal.timeout(OPENAI_TIMEOUT_MS),
    body: JSON.stringify({
      model,
      input: [
        {
          role: 'system',
          content: [{ type: 'input_text', text: system }]
        },
        {
          role: 'user',
          content: [
            { type: 'input_text', text: user },
            ...(attachImage
              ? [
                  {
                    type: 'input_image',
                    image_url: `data:image/png;base64,${fs.readFileSync(screenshotFile, 'base64')}`
                  }
                ]
              : [])
          ]
        }
      ],
      text: {
        format: {
          type: 'json_schema',
          name: 'hinge_analysis',
          schema
        }
      }
    })
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`OpenAI API failed with HTTP ${response.status}: ${errorBody}`);
  }

  const payload = await response.json();
  const text = extractResponseText(payload);
  if (!text) {
    throw new Error('OpenAI response was empty');
  }

  const parsed = JSON.parse(text);
  return {
    ...parsed,
    source: 'openai',
    commonGround: parsed.commonGround || [],
    dealbreakerHit: parsed.dealbreakerHit === true,
    rizzReferences: rizzLines
  };
}

function renderMarkdown(analysis) {
  const lines = [];
  lines.push('# Hinge Analysis');
  lines.push('');
  lines.push(`Mode: ${analysis.mode}`);
  lines.push(`Source: ${analysis.source}`);
  lines.push('');
  lines.push('## Summary');
  lines.push(analysis.summary);
  lines.push('');
  lines.push('## Signals');
  for (const signal of analysis.signals || []) {
    lines.push(`- ${signal}`);
  }
  if (!analysis.signals?.length) {
    lines.push('- None captured');
  }
  lines.push('');
  lines.push('## Recommended');
  lines.push(analysis.recommendedMessage);
  lines.push('');
  lines.push('## Backups');
  for (const backup of analysis.backupMessages || []) {
    lines.push(`- ${backup}`);
  }
  if (!analysis.backupMessages?.length) {
    lines.push('- None');
  }
  lines.push('');
  lines.push('## Risks');
  for (const risk of analysis.risks || []) {
    lines.push(`- ${risk}`);
  }
  if (!analysis.risks?.length) {
    lines.push('- None called out');
  }
  lines.push('');
  lines.push('## Why');
  lines.push(analysis.explanation);
  lines.push('');
  return lines.join('\n');
}

async function main() {
  const mode = getArg('--mode').toLowerCase();
  if (!['profile', 'reply', 'rose', 'planner'].includes(mode)) {
    throw new Error('Missing or invalid --mode (profile|reply|rose|planner)');
  }

  const dir = getArg('--dir', 'hinge-data');
  const { paths, config } = loadConfig(dir);
  const context = loadContext();
  const rizzEnabled = getArg('--use-rizz', String(config.ai?.useRizzApi ?? true)) !== 'false';
  const rizzBaseUrl = getArg('--rizz-base-url', process.env.RIZZ_API_BASE_URL || config.ai?.rizzApiBaseUrl || 'https://rizzapi.vercel.app');
  const rizzCount = Number(getArg('--rizz-count', '3'));
  const candidateMessage = getArg('--candidate-message');
  const screenshotFile = getArg('--screenshot-file');
  const shouldWebValidate =
    getArg('--web-validate', hasFlag('--web-validate') ? 'true' : String(config.ai?.webValidateBeforeSend ?? false)) === 'true';
  const blockFallback =
    getArg('--block-fallback', String(config.ai?.blockFallback ?? true)) === 'true';

  let rizzLines = [];
  if (rizzEnabled && mode !== 'planner') {
    try {
      rizzLines = readRizzCache(paths);
      if (rizzLines.length < Math.max(2, rizzCount)) {
        rizzLines = await fetchRizzLines(rizzBaseUrl, rizzCount);
        if (rizzLines.length) {
          writeRizzCache(paths, rizzLines);
        } else {
          rizzLines = readRizzCache(paths);
        }
      }
    } catch (error) {
      rizzLines = readRizzCache(paths);
    }
    rizzLines = rizzLines.map(cleanOneLiner).filter(Boolean).filter((line) => !isCheesyRizz(line));
  }

  if (mode === 'profile' && !hasFlag('--skip-photo-inference')) {
    try {
      context.photoInference = await fetchPhotoInference(context, config, screenshotFile);
    } catch (error) {
      context.photoInferenceError = error.message || String(error);
    }
  }

  let analysis;
  let openAiError = '';
  try {
    analysis = await fetchOpenAiAnalysis(mode, context, config, rizzLines);
  } catch (error) {
    openAiError = error.message || String(error);
    if (mode !== 'planner' && blockFallback) {
      analysis = {
        mode,
        source: 'openai-error',
        summary: 'Primary model unavailable; fallback blocked by policy.',
        signals: [],
        risks: [openAiError],
        recommendedMessage: '',
        visualAttractionScore: null,
        compatibilityScore: null,
        profileQualityScore: null,
        commonGround: [],
        dealbreakerHit: false,
        backupMessages: [],
        explanation: 'No message emitted because fallback generation is disabled.',
        allowFallback: false
      };
    } else {
      analysis = buildFallbackAnalysis(mode, context, rizzLines, config);
    }
    if (hasFlag('--debug-openai-error')) {
      analysis.openAiError = openAiError;
    }
  }

  if (mode !== 'planner' && blockFallback) {
    analysis.allowFallback = false;
  }

  if (mode === 'profile') {
    const parsedVisualScore = Number(analysis?.visualAttractionScore);
    if (Number.isFinite(parsedVisualScore) && parsedVisualScore >= 1) {
      analysis.visualAttractionScore = Math.max(1, Math.min(10, Math.round(parsedVisualScore)));
    } else {
      const visionFallbackScore = Number(context.photoInference?.visualAttractionScoreEstimate);
      if (Number.isFinite(visionFallbackScore) && visionFallbackScore >= 1) {
        analysis.visualAttractionScore = Math.max(1, Math.min(10, Math.round(visionFallbackScore)));
        analysis.source = `${analysis.source || 'unknown'}+vision-score`;
      }
    }
  }

  analysis = enforceMessageStyle(mode, analysis, context, config, rizzLines);
  try {
    analysis = await chainModelRewrite(mode, analysis, context, config);
  } catch (error) {
    analysis.chainRewriteError = error.message || String(error);
  }
  analysis = enforceMessageStyle(mode, analysis, context, config, rizzLines);
  analysis = applyHumanizerPass(mode, analysis, context);
  analysis = enforceMessageStyle(mode, analysis, context, config, rizzLines);
  if (candidateMessage) {
    analysis.candidateMessage = cleanOneLiner(candidateMessage);
    analysis.backupMessages = [...new Set([analysis.recommendedMessage, analysis.candidateMessage, ...(analysis.backupMessages || [])].filter(Boolean))].slice(0, 3);
    try {
      analysis = await chainModelRewrite(mode, analysis, context, config);
    } catch (error) {
      analysis.chainRewriteError = error.message || String(error);
    }
    analysis = enforceMessageStyle(mode, analysis, context, config, rizzLines);
    analysis = applyHumanizerPass(mode, analysis, context);
    analysis = enforceMessageStyle(mode, analysis, context, config, rizzLines);
  }
  if (shouldWebValidate) {
    try {
      analysis = await validateMessageWithWebSearch(mode, analysis, context, config);
      analysis = enforceMessageStyle(mode, analysis, context, config, rizzLines);
      try {
        analysis = await chainModelRewrite(mode, analysis, context, config);
      } catch (error) {
        analysis.chainRewriteError = error.message || String(error);
      }
      analysis = enforceMessageStyle(mode, analysis, context, config, rizzLines);
      analysis = applyHumanizerPass(mode, analysis, context);
      analysis = enforceMessageStyle(mode, analysis, context, config, rizzLines);
    } catch (error) {
      analysis.webValidationError = error.message || String(error);
    }
  }
  try {
    analysis = await chainQualityGate(mode, analysis, context, config);
  } catch (error) {
    analysis.qualityGateError = error.message || String(error);
  }
  analysis = enforceMessageStyle(mode, analysis, context, config, rizzLines);

  const jsonOut = getArg('--out-json', paths.analysisJsonPath);
  const markdownOut = getArg('--out-markdown', paths.analysisMarkdownPath);
  writeJson(jsonOut, analysis);
  fs.writeFileSync(markdownOut, renderMarkdown(analysis));
  if (hasFlag('--debug-openai-error') && openAiError) {
    console.error(openAiError);
  }
  console.log(JSON.stringify(analysis, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});

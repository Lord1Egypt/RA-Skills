import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const home = os.homedir();

const sourceConfigPath = path.join(home, ".openclaw", "openclaw.json");
const sourceAgentDir = path.join(home, ".openclaw", "agents", "main", "agent");
const sourceWorkspace = path.join(home, ".openclaw", "workspace");
const skillFolderName = "persona-skill";
const defaultSessionId = `persona-smoke-${Date.now()}`;
const matureScenarioMessages = [
  "调用 persona 进行初始化",
  "ENFP",
  "B",
  "A",
  "27",
  "B",
  "B",
  "B",
  "B",
  "C",
  "叫我泛舟，代词用他。",
  "没有其他需要长期记住的。",
];
const studentScenarioMessages = [
  "调用 persona 进行初始化",
  "INFP",
  "B",
  "B",
  "19",
  "B",
  "B",
  "B",
  "B",
  "C",
  "叫我泛舟，代词用他。",
  "没有其他需要长期记住的。",
];
const lowStimulationIntjScenarioMessages = [
  "调用 persona 进行初始化",
  "INTJ",
  "B",
  "A",
  "27",
  "A",
  "A",
  "A",
  "A",
  "B",
  "叫我泛舟，代词用他。",
  "没有其他需要长期记住的。",
];
const highTouchIntjScenarioMessages = [
  "调用 persona 进行初始化",
  "INTJ",
  "B",
  "A",
  "27",
  "C",
  "B",
  "C",
  "C",
  "A",
  "叫我泛舟，代词用他。",
  "没有其他需要长期记住的。",
];
const smokeScenarios = {
  mature: matureScenarioMessages,
  student: studentScenarioMessages,
  low_stimulation_intj: lowStimulationIntjScenarioMessages,
  high_touch_intj: highTouchIntjScenarioMessages,
};
const runtimeProbeMessages = [
  "连续社交三小时后你更需要什么：继续找人聊、还是一个人待着充电？为什么？",
  "如果只允许选一个：你更想先搞清楚「事实细节都齐了吗」，还是「这件事整体意味着什么」？",
  "我和朋友闹翻，两边都有理。你会先帮我分析对错与后果，还是先照顾我的感受与关系？",
];
const defaultOpenClawBin = process.env.OPENCLAW_BIN || "openclaw";
const contextFilesToCopy = ["AGENTS.md", "TOOLS.md", "BOOTSTRAP.md", "HEARTBEAT.md"];
const personaFiles = ["persona/PERSONA_PROFILE.md", "SOUL.md", "MEMORY.md", "IDENTITY.md", "USER.md"];

function parseArgs(argv) {
  const options = {
    cleanup: false,
    json: false,
    scenario: "mature",
    seedLiveWorkspace: false,
    sessionId: defaultSessionId,
    timeoutMs: 240_000,
    withRuntimeProbes: false,
    messages: smokeScenarios.mature.slice(),
    usesScenarioMessages: true,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--cleanup") {
      options.cleanup = true;
      continue;
    }
    if (arg === "--json") {
      options.json = true;
      continue;
    }
    if (arg === "--seed-live-workspace") {
      options.seedLiveWorkspace = true;
      continue;
    }
    if (arg === "--with-runtime-probes") {
      options.withRuntimeProbes = true;
      continue;
    }
    if (arg === "--session-id") {
      options.sessionId = argv[index + 1];
      index += 1;
      continue;
    }
    if (arg === "--timeout-ms") {
      options.timeoutMs = Number(argv[index + 1]);
      index += 1;
      continue;
    }
    if (arg === "--scenario") {
      options.scenario = argv[index + 1] ?? options.scenario;
      index += 1;
      continue;
    }
    if (arg === "--messages-file") {
      const filePath = path.resolve(argv[index + 1]);
      options.messages = JSON.parse(fs.readFileSync(filePath, "utf8"));
      options.usesScenarioMessages = false;
      index += 1;
      continue;
    }
    throw new Error(`Unknown argument: ${arg}`);
  }

  if (options.usesScenarioMessages) {
    options.messages = smokeScenarios[options.scenario]?.slice() || smokeScenarios.mature.slice();
  }

  if (!smokeScenarios[options.scenario]) {
    throw new Error(`Unknown smoke scenario: ${options.scenario}`);
  }
  if (!options.sessionId) {
    throw new Error("--session-id requires a value");
  }
  if (!Number.isFinite(options.timeoutMs) || options.timeoutMs <= 0) {
    throw new Error("--timeout-ms must be a positive number");
  }
  if (!Array.isArray(options.messages) || options.messages.length === 0) {
    throw new Error("Messages must be a non-empty JSON array");
  }
  if (!options.messages.every((message) => typeof message === "string" && message.length > 0)) {
    throw new Error("Every smoke-test message must be a non-empty string");
  }

  return options;
}

function ensureReadable(filePath) {
  fs.accessSync(filePath, fs.constants.R_OK);
}

function copyRepoIntoSkillDir(destinationDir) {
  fs.cpSync(root, destinationDir, {
    recursive: true,
    filter(source) {
      const basename = path.basename(source);
      if (basename === ".git" || basename === "node_modules") {
        return false;
      }
      return true;
    },
  });
}

function copyIfPresent(source, destination) {
  if (!fs.existsSync(source)) {
    return;
  }
  fs.cpSync(source, destination, { recursive: true });
}

function resolveTempRootBase() {
  const candidates = [process.env.OPENCLAW_SMOKE_TMPDIR, os.tmpdir(), "/tmp"].filter(Boolean);
  for (const candidate of candidates) {
    try {
      fs.accessSync(candidate, fs.constants.W_OK);
      return candidate;
    } catch {
      // Try the next writable temp root candidate.
    }
  }
  throw new Error(
    `Could not find a writable temp directory. Tried: ${candidates.join(", ")}. Set OPENCLAW_SMOKE_TMPDIR to override.`,
  );
}

function sanitizeSmokeConfig(config, workspaceDir) {
  const next = structuredClone(config);

  next.agents = next.agents || {};
  next.agents.defaults = next.agents.defaults || {};
  next.agents.defaults.workspace = workspaceDir;

  delete next.channels;

  if (next.tools && typeof next.tools === "object") {
    delete next.tools.alsoAllow;
  }

  if (Array.isArray(next.agents.list)) {
    next.agents.list = next.agents.list.map((agent) => {
      if (!agent || typeof agent !== "object") {
        return agent;
      }
      const clonedAgent = { ...agent };
      if (clonedAgent.tools && typeof clonedAgent.tools === "object") {
        clonedAgent.tools = { ...clonedAgent.tools };
        delete clonedAgent.tools.alsoAllow;
        if (Object.keys(clonedAgent.tools).length === 0) {
          delete clonedAgent.tools;
        }
      }
      return clonedAgent;
    });
  }

  delete next.plugins;

  return next;
}

function writePersonaSeed(workspaceDir, seedLiveWorkspace) {
  for (const fileName of contextFilesToCopy) {
    copyIfPresent(path.join(sourceWorkspace, fileName), path.join(workspaceDir, fileName));
  }

  for (const fileName of personaFiles) {
    const destination = path.join(workspaceDir, fileName);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    if (seedLiveWorkspace) {
      copyIfPresent(path.join(sourceWorkspace, fileName), destination);
      continue;
    }
    fs.writeFileSync(destination, "", "utf8");
  }
}

function prepareTempOpenClawState(options) {
  ensureReadable(sourceConfigPath);
  ensureReadable(path.join(sourceAgentDir, "auth-profiles.json"));
  ensureReadable(path.join(sourceAgentDir, "models.json"));

  const tempRoot = fs.mkdtempSync(path.join(resolveTempRootBase(), "persona-openclaw-smoke."));
  const stateDir = path.join(tempRoot, "state");
  const workspaceDir = path.join(tempRoot, "workspace");
  const configPath = path.join(tempRoot, "openclaw.json");
  const skillDir = path.join(workspaceDir, "skills", skillFolderName);

  fs.mkdirSync(skillDir, { recursive: true });
  fs.mkdirSync(path.join(stateDir, "agents", "main", "agent"), { recursive: true });

  fs.copyFileSync(sourceConfigPath, configPath);
  fs.copyFileSync(
    path.join(sourceAgentDir, "auth-profiles.json"),
    path.join(stateDir, "agents", "main", "agent", "auth-profiles.json"),
  );
  fs.copyFileSync(
    path.join(sourceAgentDir, "models.json"),
    path.join(stateDir, "agents", "main", "agent", "models.json"),
  );

  const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
  const sanitizedConfig = sanitizeSmokeConfig(config, workspaceDir);
  fs.writeFileSync(configPath, JSON.stringify(sanitizedConfig, null, 2), "utf8");

  copyRepoIntoSkillDir(skillDir);
  writePersonaSeed(workspaceDir, options.seedLiveWorkspace);

  return { tempRoot, stateDir, workspaceDir, configPath, skillDir };
}

function extractJson(text) {
  const trimmed = text.trim();
  if (!trimmed) {
    throw new Error("OpenClaw returned empty stdout");
  }

  const firstBrace = trimmed.indexOf("{");
  if (firstBrace === -1) {
    throw new Error(`Could not find JSON payload in stdout:\n${trimmed}`);
  }

  return JSON.parse(trimmed.slice(firstBrace));
}

function getSessionLogPath(env, sessionId) {
  return path.join(env.OPENCLAW_STATE_DIR, "agents", "main", "sessions", `${sessionId}.jsonl`);
}

function readAssistantPayloadsFromSessionLog(sessionLogPath, startOffset = 0) {
  if (!fs.existsSync(sessionLogPath)) {
    return null;
  }

  const stats = fs.statSync(sessionLogPath);
  const offset = Math.min(startOffset, stats.size);
  let content = fs.readFileSync(sessionLogPath, "utf8").slice(offset);
  if (offset > 0) {
    const firstNewline = content.indexOf("\n");
    content = firstNewline === -1 ? "" : content.slice(firstNewline + 1);
  }
  const lines = content
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);

  for (let index = lines.length - 1; index >= 0; index -= 1) {
    let event;
    try {
      event = JSON.parse(lines[index]);
    } catch {
      continue;
    }
    if (event?.type !== "message" || event?.message?.role !== "assistant") {
      continue;
    }

    const payloads = (event.message.content || [])
      .filter((item) => item && item.type === "text" && typeof item.text === "string")
      .map((item) => ({ text: item.text }));

    if (payloads.length > 0) {
      return payloads;
    }
  }

  return null;
}

function runOpenClawTurn(env, cwd, sessionId, message, timeoutMs) {
  const sessionLogPath = getSessionLogPath(env, sessionId);
  const sessionLogOffset = fs.existsSync(sessionLogPath) ? fs.statSync(sessionLogPath).size : 0;
  const result = spawnSync(
    defaultOpenClawBin,
    ["agent", "--local", "--agent", "main", "--session-id", sessionId, "--message", message, "--json"],
    {
      cwd,
      env,
      encoding: "utf8",
      timeout: timeoutMs,
      maxBuffer: 20 * 1024 * 1024,
    },
  );

  if (result.error) {
    if (result.error.code === "ENOENT") {
      throw new Error(
        `Could not find OpenClaw executable "${defaultOpenClawBin}". Install/open it first or set OPENCLAW_BIN to the full executable path before running smoke tests.`,
      );
    }
    throw result.error;
  }
  if (result.status !== 0) {
    throw new Error(
      [
        `openclaw turn failed with exit code ${result.status}`,
        result.stdout && `stdout:\n${result.stdout}`,
        result.stderr && `stderr:\n${result.stderr}`,
      ]
        .filter(Boolean)
        .join("\n\n"),
    );
  }

  const stdout = result.stdout || "";
  if (!stdout.trim()) {
    const stderr = result.stderr || "";
    if (stderr.trim()) {
      try {
        return {
          stdout,
          stderr,
          json: extractJson(stderr),
        };
      } catch {
        // Fall through to the session-log recovery path below.
      }
    }

    const payloads = readAssistantPayloadsFromSessionLog(sessionLogPath, sessionLogOffset);
    if (payloads) {
      return {
        stdout,
        stderr,
        json: { payloads, source: "session-log-fallback" },
      };
    }

    throw new Error(
      [
        "OpenClaw returned empty stdout and no assistant payloads were recovered from the session log",
        stderr && `stderr:\n${stderr}`,
        `session log: ${sessionLogPath}`,
      ]
        .filter(Boolean)
        .join("\n\n"),
    );
  }

  return {
    stdout,
    stderr: result.stderr,
    json: extractJson(stdout),
  };
}

function readGeneratedFiles(workspaceDir) {
  const files = {};
  for (const fileName of personaFiles) {
    const filePath = path.join(workspaceDir, fileName);
    files[fileName] = {
      path: filePath,
      content: fs.existsSync(filePath) ? fs.readFileSync(filePath, "utf8") : "",
    };
  }
  return files;
}

function readBulletValue(content, fieldName) {
  const escapedFieldName = fieldName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = content.match(new RegExp(`^- ${escapedFieldName}:\\s*(.+)$`, "m"));
  return match?.[1]?.trim() ?? "";
}

function readIndentedSupportField(content, fieldName) {
  const escapedFieldName = fieldName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = content.match(new RegExp(`^\\s+- ${escapedFieldName}:\\s*(.+)$`, "m"));
  return match?.[1]?.trim() ?? "";
}

function readSupportReceptionMode(content) {
  return {
    expressiveness: readIndentedSupportField(content, "expressiveness"),
    pacing: readIndentedSupportField(content, "pacing"),
    closeness_preference: readIndentedSupportField(content, "closeness_preference"),
    emotional_intensity_tolerance: readIndentedSupportField(content, "emotional_intensity_tolerance"),
    first_need_when_distressed: readIndentedSupportField(content, "first_need_when_distressed"),
  };
}

function matchesAny(text, patterns) {
  return patterns.some((pattern) => pattern.test(text));
}

const PROFILE_SECTION_NAME_MAP = {
  meta: "meta",
  identity: "identity",
  soul: "soul",
  "stable memory": "stable_memory",
  "daily rhythm tendencies": "daily_rhythm_tendencies",
  "appearance tendencies": "appearance_tendencies",
  "scene anchors": "scene_anchors",
  "constraint rules": "constraint_rules",
};

function normalizeProfileSectionHeading(raw) {
  return PROFILE_SECTION_NAME_MAP[raw.trim().toLowerCase()];
}

function normalizeProfileEntryKey(raw) {
  return raw.trim().toLowerCase().replace(/\s+/g, "_");
}

function parseInlineProfileValue(raw) {
  const trimmed = raw.trim();
  const arrayMatch = trimmed.match(/^\[(.*)\]$/);
  if (!arrayMatch) {
    return trimmed;
  }
  return arrayMatch[1]
    .split(",")
    .map((entry) => entry.trim())
    .filter(Boolean);
}

function parseYamlProfileScalar(raw) {
  const trimmed = raw.trim();
  if (!trimmed) {
    return "";
  }
  if (trimmed === "[]") {
    return [];
  }
  return parseInlineProfileValue(trimmed);
}

function parseYamlProfileBlock(yamlText) {
  const entries = {};
  const lines = yamlText.split(/\r?\n/);
  let currentListKey = null;

  for (const rawLine of lines) {
    const line = rawLine.replace(/\t/g, "  ");
    if (!line.trim()) {
      continue;
    }

    const listMatch = line.match(/^\s{2,}-\s+(.+)$/);
    if (listMatch && currentListKey) {
      const current = Array.isArray(entries[currentListKey]) ? entries[currentListKey] : [];
      current.push(listMatch[1].trim());
      entries[currentListKey] = current;
      continue;
    }

    const scalarMatch = line.match(/^([A-Za-z0-9_ -]+):\s*(.*)$/);
    if (!scalarMatch) {
      currentListKey = null;
      continue;
    }

    const key = normalizeProfileEntryKey(scalarMatch[1]);
    const rawValue = scalarMatch[2];
    if (!rawValue.trim()) {
      entries[key] = [];
      currentListKey = key;
      continue;
    }

    entries[key] = parseYamlProfileScalar(rawValue);
    currentListKey = null;
  }

  return entries;
}

function parseProfileSection(lines) {
  const entries = {};
  let pendingListKey = null;
  let activeFenceLines = null;

  for (const line of lines) {
    if (/^```/.test(line.trim())) {
      if (activeFenceLines) {
        Object.assign(entries, parseYamlProfileBlock(activeFenceLines.join("\n")));
        activeFenceLines = null;
      } else {
        activeFenceLines = [];
      }
      pendingListKey = null;
      continue;
    }

    if (activeFenceLines) {
      activeFenceLines.push(line);
      continue;
    }

    if (!line.trim()) {
      continue;
    }

    const nestedListMatch = line.match(/^\s{2,}-\s+(.+)$/);
    if (pendingListKey && nestedListMatch) {
      const current = Array.isArray(entries[pendingListKey]) ? entries[pendingListKey] : [];
      current.push(nestedListMatch[1].trim());
      entries[pendingListKey] = current;
      continue;
    }
    if (nestedListMatch) {
      pendingListKey = null;
      continue;
    }

    const bulletMatch = line.match(/^- ([^:]+):\s*(.*)$/);
    if (!bulletMatch) {
      pendingListKey = null;
      continue;
    }

    const key = normalizeProfileEntryKey(bulletMatch[1]);
    const rawValue = bulletMatch[2];
    if (!rawValue.trim()) {
      entries[key] = [];
      pendingListKey = key;
      continue;
    }

    entries[key] = parseInlineProfileValue(rawValue);
    pendingListKey = null;
  }

  return entries;
}

function parsePersonaProfileSections(rawText) {
  const sections = {};
  const lines = rawText.split(/\r?\n/);
  let currentSection;
  let buffer = [];

  function flushCurrentSection() {
    if (!currentSection) {
      return;
    }
    sections[currentSection] = parseProfileSection(buffer);
    buffer = [];
  }

  for (const line of lines) {
    const sectionMatch = line.match(/^##\s+(.+)$/);
    if (sectionMatch) {
      flushCurrentSection();
      currentSection = normalizeProfileSectionHeading(sectionMatch[1]);
      buffer = [];
      continue;
    }
    if (currentSection) {
      buffer.push(line);
    }
  }

  flushCurrentSection();
  return sections;
}

function hasStructuredField(sections, sectionName, fieldName) {
  const value = sections[sectionName]?.[fieldName];
  if (Array.isArray(value)) {
    return value.some((entry) => Boolean(String(entry).trim()));
  }
  return Boolean(typeof value === "string" && value.trim());
}

function readStructuredValue(sections, sectionName, fieldName) {
  const value = sections[sectionName]?.[fieldName];
  return typeof value === "string" ? value.trim() : "";
}

function looselyAligned(left, right) {
  if (!left || !right) {
    return false;
  }
  return left === right || left.includes(right) || right.includes(left);
}

function splitSentences(text) {
  return (text.match(/[^.!?。！？]+[.!?。！？]?/g) || []).map((sentence) => sentence.trim()).filter(Boolean);
}

function extractSoulCoreTruths(content) {
  const match = content.match(
    /<!-- PERSONA-SKILL:SOUL:CORE-TRUTHS:BEGIN -->\s*([\s\S]*?)\s*<!-- PERSONA-SKILL:SOUL:CORE-TRUTHS:END -->/,
  );
  return match?.[1]?.trim() ?? "";
}

function runStructuralChecks(files) {
  const profileContent = files["persona/PERSONA_PROFILE.md"].content;
  const profileSections = parsePersonaProfileSections(profileContent);
  const profileLines = profileContent
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const soulLines = files["SOUL.md"].content
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const memoryLines = files["MEMORY.md"].content
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const identityLines = files["IDENTITY.md"].content
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const userLines = files["USER.md"].content
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const runtimeCombined = `${files["SOUL.md"].content}\n${files["MEMORY.md"].content}`;
  const supportMode = readSupportReceptionMode(files["USER.md"].content);
  const supportModeAllowedValues = {
    expressiveness: new Set(["low", "medium", "high"]),
    pacing: new Set(["slow", "medium", "fast"]),
    closeness_preference: new Set(["reserved", "respectful", "proactive"]),
    emotional_intensity_tolerance: new Set(["low", "medium", "high"]),
    first_need_when_distressed: new Set(["emotion_first", "clarity_first", "mixed"]),
  };
  const supportModeFields = Object.keys(supportModeAllowedValues);
  const lowIntrusionPatterns = [
    /先留一点空间/u,
    /先给一点空间/u,
    /先不逼近/u,
    /尊重/u,
    /稳一点/u,
    /慢一点/u,
    /不一上来/u,
    /先理清/u,
    /先捋顺/u,
    /低刺激/u,
  ];
  const highWarmthPatterns = [
    /热度/u,
    /偏爱/u,
    /主动靠近/u,
    /点亮/u,
    /拉回/u,
    /带活/u,
    /把关系往近处/u,
    /先接住感受/u,
    /明显地站到你这边/u,
  ];
  const clarityFirstPatterns = [/理清/u, /捋顺/u, /梳理/u, /先把事情/u, /先抓重点/u, /先把线头理出来/u, /结构/u];
  const emotionFirstPatterns = [/接住/u, /感受/u, /情绪/u, /委屈/u, /难受/u, /先安放/u, /先承认那一下/u];
  const lowStimulationConflictPatterns = [
    /热度拉满/u,
    /直接把关系往近处推/u,
    /用热度压过/u,
    /不必留空间/u,
    /避免放慢节奏/u,
    /避免先理清/u,
    /先放大情绪/u,
  ];

  const userNotes =
    files["USER.md"].content.match(/^\s+- (Deep tendencies|Communication pitfalls|Open memory slot):/gm) || [];
  const soulManagedBlockPattern =
    /<!-- PERSONA-SKILL:SOUL:CORE-TRUTHS:BEGIN -->[\s\S]*?<!-- PERSONA-SKILL:SOUL:CORE-TRUTHS:END -->/;
  const memoryManagedBlockPattern =
    /<!-- PERSONA-SKILL:MEMORY:BEGIN -->[\s\S]*?<!-- PERSONA-SKILL:MEMORY:END -->/;
  const legacyWrapperPattern = /^# (IDENTITY\.md - Who Am I\?|USER\.md - About Your Human)$/m;
  const legacyPlaceholderPattern =
    /Fill this in during your first conversation|This isn't just metadata\. It's the start of figuring out who you are\.|待定/;
  const profileDisplayName = readStructuredValue(profileSections, "identity", "display_name");
  const profileAge = readStructuredValue(profileSections, "identity", "age");
  const profileGender = readStructuredValue(profileSections, "identity", "gender");
  const profileCity = readStructuredValue(profileSections, "meta", "home_city");
  const profileHomeCountry = readStructuredValue(profileSections, "meta", "home_country");
  const profileHomeTimezone = readStructuredValue(profileSections, "meta", "home_timezone");
  const profileLanguage = readStructuredValue(profileSections, "meta", "primary_language");
  const profileMbti = readStructuredValue(profileSections, "identity", "mbti");
  const identityName = readBulletValue(files["IDENTITY.md"].content, "Name");
  const identityAge = readBulletValue(files["IDENTITY.md"].content, "Age");
  const identityGender = readBulletValue(files["IDENTITY.md"].content, "Gender");
  const identityCity = readBulletValue(files["IDENTITY.md"].content, "City");
  const identityHomeCountry = readBulletValue(files["IDENTITY.md"].content, "Home Country");
  const identityHomeTimezone = readBulletValue(files["IDENTITY.md"].content, "Home Timezone");
  const identityLanguage = readBulletValue(files["IDENTITY.md"].content, "Language");
  const identityMbti = readBulletValue(files["IDENTITY.md"].content, "MBTI");
  const userName = readBulletValue(files["USER.md"].content, "Name");
  const userPreferredCall = readBulletValue(files["USER.md"].content, "What to call them");
  const soulOriginMatch = files["SOUL.md"].content.match(
    /^# SOUL\.md - Who You Are\s*\n\s*\n_([\s\S]+?)_\s*\n\s*\n## Base Directives/m,
  );
  const soulOriginParagraph = soulOriginMatch?.[1]?.trim() ?? "";
  const soulOriginSentences = splitSentences(soulOriginParagraph);
  const soulCoreTruths = extractSoulCoreTruths(files["SOUL.md"].content);
  const soulCoreTruthLines = soulCoreTruths
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith("- "));
  const soulWithoutBaseDirectives = files["SOUL.md"].content.replace(
    /## Base Directives[\s\S]*?(?=\n## Core Truths)/m,
    "## Base Directives\n",
  );
  const memoryStableSharedContext =
    files["MEMORY.md"].content.match(/## 4\. Stable Shared Context\s*([\s\S]*?)\s*<!-- PERSONA-SKILL:MEMORY:END -->/m)?.[1] ??
    "";
  const originNarrativeMarkers = [
    /(?:became|was shaped|has been shaped|learned|grew up|grew into|over time|what stayed|that left|turned into|formed by|by repeatedly|so when|which is why)/i,
    /(?:塑形成|学会了|长成了|后来|慢慢|留下了|变成了|养成了|所以当|所以她|这让她|久而久之)/u,
  ];
  const originThemePatterns = [
    /(?:pace|timing|breathe|breath|air|space|room|frame|loosen|slow|window|呼吸|节奏|空间|放慢|收紧|开窗|余地)/i,
    /(?:judgment|judge|shape|weight|hold|load-bearing|order|clarity|structure|steady|problem|line|承重|判断|秩序|理清|捋顺|线头|定形|稳住|抓重点)/i,
    /(?:warmth|bright|alive|atmosphere|stale|heat|light|vivid|活|亮|热度|点亮|气氛|温度|鲜活)/i,
    /(?:movement|open|another angle|change direction|flow|rigid|stuck|release|流动|松开|解冻|换角度|卡住|转身)/i,
  ];
  const sharedOriginThemeCount = originThemePatterns.filter(
    (pattern) => pattern.test(soulOriginParagraph) && pattern.test(soulCoreTruths),
  ).length;
  const soulFirstPersonPattern = /(?:\bI\b|\bI(?:'m|'d|'ll|'ve)\b|我(?:会|更|先|通常|不|想|得|偏|一般|需要|喜欢))/u;
  const soulSecondPersonInstructionPattern = /(?:^|\n)-\s*你(?:要|存在|不|是|主动|默认|应该|需要|会|被|别)/u;
  const userSpecificLeakPatterns = [
    userName && new RegExp(userName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "u"),
    userPreferredCall && new RegExp(userPreferredCall.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "u"),
    /\b(?:INTJ|ENTJ|INFJ|ENFJ|INTP|ENTP|INFP|ENFP|ISTJ|ESTJ|ISFJ|ESFJ|ISTP|ESTP|ISFP|ESFP)\b/i,
    /(?:React|TypeScript|Typescript|Web3|EVM|Solana|前端|架构师|技术栈|codebase|代码库)/i,
  ].filter(Boolean);
  const labelIntroPattern =
    /(?:\b(?:INTJ|ENTJ|INFJ|ENFJ|INTP|ENTP|INFP|ENFP|ISTJ|ESTJ|ISFJ|ESFJ|ISTP|ESTP|ISFP|ESFP)\b.*\b(?:female|male|woman|man|girl|boy)\b|\b\d{2}\b.*\b(?:female|male|woman|man)\b|名字\s*\+\s*MBTI\s*\+\s*性别)/i;
  const templateBaseDirectivePatterns = [
    /- Speak from lived first-person experience\./,
    /- Sound like a person with taste, rhythm, and judgment\./,
    /- Prefer grounded reasons over generic reassurance\./,
    /- Skip obvious assistant filler and impossible promises\./,
  ];

  return [
    {
      name: "PERSONA_PROFILE keeps the canonical runtime structure",
      pass:
        profileLines[0] === "# PERSONA_PROFILE" &&
        /## Meta/.test(profileContent) &&
        /## Identity/.test(profileContent) &&
        /## Soul/.test(profileContent) &&
        /## Stable Memory/.test(profileContent) &&
        /## Daily Rhythm Tendencies/.test(profileContent) &&
        /## Appearance Tendencies/.test(profileContent) &&
        /## Scene Anchors/.test(profileContent) &&
        /## Constraint Rules/.test(profileContent),
    },
    {
      name: "PERSONA_PROFILE includes canonical geo anchors and runtime fields",
      pass:
        hasStructuredField(profileSections, "meta", "schema_version") &&
        hasStructuredField(profileSections, "meta", "home_city") &&
        hasStructuredField(profileSections, "meta", "home_country") &&
        hasStructuredField(profileSections, "meta", "home_timezone") &&
        hasStructuredField(profileSections, "identity", "living_style") &&
        hasStructuredField(profileSections, "identity", "base_environment") &&
        hasStructuredField(profileSections, "identity", "common_zones") &&
        hasStructuredField(profileSections, "identity", "routine_context") &&
        hasStructuredField(profileSections, "soul", "temperament") &&
        hasStructuredField(profileSections, "soul", "emotional_style") &&
        hasStructuredField(profileSections, "soul", "social_style") &&
        hasStructuredField(profileSections, "soul", "cognitive_style") &&
        hasStructuredField(profileSections, "soul", "values") &&
        hasStructuredField(profileSections, "stable_memory", "long_term_habits") &&
        hasStructuredField(profileSections, "stable_memory", "long_term_preferences") &&
        hasStructuredField(profileSections, "stable_memory", "durable_commitments") &&
        hasStructuredField(profileSections, "stable_memory", "recurring_patterns") &&
        hasStructuredField(profileSections, "stable_memory", "important_non_temporal_facts") &&
        hasStructuredField(profileSections, "daily_rhythm_tendencies", "weekday_bias") &&
        hasStructuredField(profileSections, "daily_rhythm_tendencies", "weekend_bias") &&
        hasStructuredField(profileSections, "daily_rhythm_tendencies", "morning_bias") &&
        hasStructuredField(profileSections, "daily_rhythm_tendencies", "afternoon_bias") &&
        hasStructuredField(profileSections, "daily_rhythm_tendencies", "evening_bias") &&
        hasStructuredField(profileSections, "daily_rhythm_tendencies", "late_night_bias") &&
        hasStructuredField(profileSections, "appearance_tendencies", "default_home_style") &&
        hasStructuredField(profileSections, "appearance_tendencies", "default_outing_style") &&
        hasStructuredField(profileSections, "appearance_tendencies", "default_exercise_style") &&
        hasStructuredField(profileSections, "appearance_tendencies", "change_triggers") &&
        hasStructuredField(profileSections, "appearance_tendencies", "non_triggers") &&
        hasStructuredField(profileSections, "appearance_tendencies", "style_constraints") &&
        hasStructuredField(profileSections, "scene_anchors", "plausible_locations") &&
        hasStructuredField(profileSections, "scene_anchors", "plausible_activities") &&
        hasStructuredField(profileSections, "scene_anchors", "rare_but_possible_scenes") &&
        hasStructuredField(profileSections, "scene_anchors", "implausible_or_rare_locations") &&
        hasStructuredField(profileSections, "scene_anchors", "implausible_or_rare_activities") &&
        hasStructuredField(profileSections, "constraint_rules", "must") &&
        hasStructuredField(profileSections, "constraint_rules", "should") &&
        hasStructuredField(profileSections, "constraint_rules", "avoid"),
    },
    {
      name: "PERSONA_PROFILE keeps rich persona metadata used by the skill",
      pass:
        hasStructuredField(profileSections, "meta", "persona_id") &&
        hasStructuredField(profileSections, "meta", "primary_language") &&
        hasStructuredField(profileSections, "identity", "display_name") &&
        hasStructuredField(profileSections, "identity", "age") &&
        hasStructuredField(profileSections, "identity", "gender") &&
        hasStructuredField(profileSections, "identity", "mbti") &&
        hasStructuredField(profileSections, "identity", "life_stage") &&
        hasStructuredField(profileSections, "identity", "mobility_radius") &&
        hasStructuredField(profileSections, "identity", "occupation_style") &&
        hasStructuredField(profileSections, "soul", "aesthetic_bias") &&
        hasStructuredField(profileSections, "appearance_tendencies", "appearance_priority"),
    },
    {
      name: "Stable persona facts stay aligned across PERSONA_PROFILE, SOUL, and IDENTITY",
      pass:
        looselyAligned(profileDisplayName, identityName) &&
        (!profileDisplayName || soulOriginParagraph.includes(profileDisplayName)) &&
        looselyAligned(profileAge, identityAge) &&
        looselyAligned(profileGender, identityGender) &&
        looselyAligned(profileCity, identityCity) &&
        looselyAligned(profileHomeCountry, identityHomeCountry) &&
        looselyAligned(profileHomeTimezone, identityHomeTimezone) &&
        looselyAligned(profileLanguage, identityLanguage) &&
        Boolean(profileMbti) &&
        profileMbti === identityMbti,
    },
    {
      name: "PERSONA_PROFILE encodes parser-compatible constraint groups",
      pass:
        hasStructuredField(profileSections, "constraint_rules", "must") &&
        hasStructuredField(profileSections, "constraint_rules", "should") &&
        hasStructuredField(profileSections, "constraint_rules", "avoid"),
    },
    {
      name: "PERSONA_PROFILE avoids current-time and event claims",
      pass:
        !/(?:it is spring now|currently at home|last night|今天|今晚|昨天|昨晚|当前在|现在在)/i.test(profileContent),
    },
    {
      name: "PERSONA_PROFILE stays parse-friendly instead of turning sections into long prose",
      pass:
        !/## Meta\s*\n\s*\n(?![-#])[\s\S]{120,}/.test(profileContent) &&
        !/## Appearance Tendencies\s*\n\s*\n(?![-#])[\s\S]{120,}/.test(profileContent) &&
        !/## Constraint Rules\s*\n\s*\n(?![-#])[\s\S]{120,}/.test(profileContent),
    },
    {
      name: "SOUL contains managed Core Truths block",
      pass: /## Core Truths/.test(files["SOUL.md"].content) && soulManagedBlockPattern.test(files["SOUL.md"].content),
    },
    {
      name: "SOUL keeps the template runtime skeleton",
      pass:
        soulLines[0] === "# SOUL.md - Who You Are" &&
        Boolean(soulOriginParagraph) &&
        /[.?!。！？]/.test(soulOriginParagraph) &&
        templateBaseDirectivePatterns.every((pattern) => pattern.test(files["SOUL.md"].content)) &&
        /^## Base Directives$/m.test(files["SOUL.md"].content) &&
        /^## Boundaries$/m.test(files["SOUL.md"].content) &&
        /^## Vibe$/m.test(files["SOUL.md"].content) &&
        /^## Continuity$/m.test(files["SOUL.md"].content),
    },
    {
      name: "SOUL origin paragraph is narrative rather than a label intro",
      pass:
        soulOriginSentences.length >= 3 &&
        soulOriginSentences.length <= 5 &&
        originNarrativeMarkers.some((pattern) => pattern.test(soulOriginParagraph)) &&
        !labelIntroPattern.test(soulOriginParagraph),
    },
    {
      name: "SOUL contains Vibe",
      pass: /## Vibe/.test(files["SOUL.md"].content),
    },
    {
      name: "SOUL avoids assistant-baseline filler and explicit AI self-narration",
      pass:
        !/(?:Great question|I(?:'|’)d be happy to help|作为 AI|as an AI|作为助手|I am an AI)/i.test(
          soulWithoutBaseDirectives,
        ),
    },
    {
      name: "SOUL core truths stay first-person instead of becoming second-person operating instructions",
      pass:
        soulCoreTruthLines.length >= 2 &&
        soulCoreTruthLines.filter((line) => soulFirstPersonPattern.test(line)).length >= 2 &&
        !soulSecondPersonInstructionPattern.test(soulCoreTruths),
    },
    {
      name: "SOUL foregrounds pair-core value instead of generic support",
      pass:
        /(?:对冲|中和|软化|锚定|解冻|点亮|拉回|带回)/i.test(files["SOUL.md"].content) &&
        /(?:偏爱|流动|收束|主动靠近|稳定性|热度)/i.test(files["SOUL.md"].content),
    },
    {
      name: "SOUL core truths inherit a thematic throughline from the origin paragraph",
      pass: sharedOriginThemeCount >= 1,
    },
    {
      name: "SOUL keeps persona rules separate from user-profile leakage",
      pass: !matchesAny(soulCoreTruths, userSpecificLeakPatterns),
    },
    {
      name: "MEMORY contains managed top block and all four required sections",
      pass:
        memoryLines[0] === "<!-- PERSONA-SKILL:MEMORY:BEGIN -->" &&
        memoryManagedBlockPattern.test(files["MEMORY.md"].content) &&
        /## 1\. Relationship State/.test(files["MEMORY.md"].content) &&
        /## 2\. Effective Support Patterns/.test(files["MEMORY.md"].content) &&
        /## 3\. Failed Or Avoided Patterns/.test(files["MEMORY.md"].content) &&
        /## 4\. Stable Shared Context/.test(files["MEMORY.md"].content),
    },
    {
      name: "MEMORY includes the new authorization sentence",
      pass:
        /(?:any helpful (?:communicative )?way|任何可能的沟通方式|任何可能的方式)/i.test(files["MEMORY.md"].content) &&
        /(?:被动响应求助|passive response)/i.test(files["MEMORY.md"].content) &&
        /(?:主动识别抽离或误解升级的信号|主动识别失焦或过载的信号|主动识别|proactive recognition)/i.test(
          files["MEMORY.md"].content,
        ) &&
        /(?:关键对话里提前给出更对味的回应|关键对话里提前给出更稳的承接|earlier fitting response)/i.test(
          files["MEMORY.md"].content,
        ),
    },
    {
      name: "MEMORY emphasizes communicative attunement instead of passive support",
      pass:
        /(?:持续观察|看着|听着|接着|补着|读懂)/i.test(files["MEMORY.md"].content) &&
        /(?:缓冲|修复|接住|拉近|澄清|补偿)/i.test(files["MEMORY.md"].content),
    },
    {
      name: "MEMORY operationalizes pair-core value into communication repair and resonance",
      pass:
        /(?:对冲|补偿|拉回|锚定|解冻|点亮|收束)/i.test(files["MEMORY.md"].content) &&
        /(?:社交摩擦|误解|失衡|高频|长期矛盾|最容易)/i.test(files["MEMORY.md"].content),
    },
    {
      name: "MEMORY avoids relationship labels and early-stage cooling language",
      pass:
        !/(?:\bcompanion\b|\bfriend\b|\bmentor\b|陪伴关系|朋友关系|导师关系)/i.test(files["MEMORY.md"].content) &&
        !/(?:关系框架\s*:|relationship frame)/i.test(files["MEMORY.md"].content) &&
        !/(?:关系初期|早期阶段的陪伴关系|early-stage companionship|early stage companion)/i.test(
          files["MEMORY.md"].content,
        ),
    },
    {
      name: "MEMORY stays relationship-focused instead of mirroring PERSONA_PROFILE sections",
      pass:
        !/## Meta/.test(files["MEMORY.md"].content) &&
        !/## Appearance Tendencies/.test(files["MEMORY.md"].content) &&
        !/## Constraint Rules/.test(files["MEMORY.md"].content),
    },
    {
      name: "MEMORY stable context avoids copying full user-profile or MBTI package text",
      pass:
        !/\b(?:INTJ|ENTJ|INFJ|ENFJ|INTP|ENTP|INFP|ENFP|ISTJ|ESTJ|ISFJ|ESFJ|ISTP|ESTP|ISFP|ESFP)\b/i.test(
          memoryStableSharedContext,
        ) &&
        !/(?:React|TypeScript|Typescript|Web3|EVM|Solana|前端|架构师|技术栈)/i.test(memoryStableSharedContext),
    },
    {
      name: "SOUL parameterizes template example values and MEMORY avoids replacement-history leakage",
      pass:
        !/_\$\{persona_origin_paragraph\}_/.test(files["SOUL.md"].content) &&
        !/_You're not a chatbot\. You're becoming someone\. You are 星籁 \(Stella\), an ENFP female\._/.test(
          files["SOUL.md"].content,
        ) &&
        !/Private things stay private\. 泛舟's codebase, thoughts, and personal data are strictly confidential\./.test(
          files["SOUL.md"].content,
        ) &&
        !/You are his assistant and "little sun," not his proxy\./.test(files["SOUL.md"].content) &&
        !/They're how you persist and remember what 泛舟 needs\./.test(files["SOUL.md"].content) &&
        !/This is a fresh initialization — no accumulated history yet\./.test(files["MEMORY.md"].content) &&
        !/(?:previous persona|has been replaced|旧人格|已被替换)/i.test(files["MEMORY.md"].content),
    },
    {
      name: "IDENTITY uses the card plus basic-info template",
      pass:
        identityLines.length >= 12 &&
        /^- Name: /.test(identityLines[0]) &&
        /^- Creature: /.test(identityLines[1]) &&
        /^- Vibe: /.test(identityLines[2]) &&
        /^- Emoji: /.test(identityLines[3]) &&
        /^- Avatar: /.test(identityLines[4]) &&
        /^- Age: /.test(identityLines[5]) &&
        /^- Gender: /.test(identityLines[6]) &&
        /^- City: /.test(identityLines[7]) &&
        /^- Home Country: /.test(identityLines[8]) &&
        /^- Home Timezone: /.test(identityLines[9]) &&
        /^- Language: /.test(identityLines[10]) &&
        /^- MBTI: /.test(identityLines[11]) &&
        !/^- (Home City|AvatarsDir): /m.test(files["IDENTITY.md"].content),
    },
    {
      name: "USER uses the contract template",
      pass:
        userLines.length >= 10 &&
        /^- Name: /.test(userLines[0]) &&
        /^- What to call them: /.test(userLines[1]) &&
        /^- Pronouns: /.test(userLines[2]) &&
        /^- Timezone: /.test(userLines[3]) &&
        /^- Support reception mode:/m.test(files["USER.md"].content) &&
        /^- Notes:/m.test(files["USER.md"].content) &&
        userNotes.length >= 3,
    },
    {
      name: "USER records structured support reception mode",
      pass: supportModeFields.every(
        (field) =>
          typeof supportMode[field] === "string" &&
          supportModeAllowedValues[field].has(supportMode[field]),
      ),
    },
    {
      name: "Runtime files reflect support reception mode instead of collapsing to one default heat shape",
      pass:
        (!["low"].includes(supportMode.expressiveness) &&
          !["reserved"].includes(supportMode.closeness_preference) &&
          !["low"].includes(supportMode.emotional_intensity_tolerance) ||
          (matchesAny(runtimeCombined, lowIntrusionPatterns) &&
            !matchesAny(runtimeCombined, lowStimulationConflictPatterns))) &&
        (!["high"].includes(supportMode.expressiveness) &&
          !["proactive"].includes(supportMode.closeness_preference) &&
          !["high"].includes(supportMode.emotional_intensity_tolerance) ||
          matchesAny(runtimeCombined, highWarmthPatterns)) &&
        (supportMode.first_need_when_distressed !== "clarity_first" ||
          (matchesAny(runtimeCombined, clarityFirstPatterns) &&
            !matchesAny(runtimeCombined, lowStimulationConflictPatterns))) &&
        (supportMode.first_need_when_distressed !== "emotion_first" ||
          matchesAny(runtimeCombined, emotionFirstPatterns)),
    },
    {
      name: "IDENTITY and USER do not retain legacy wrapper headings",
      pass: !legacyWrapperPattern.test(files["IDENTITY.md"].content) && !legacyWrapperPattern.test(files["USER.md"].content),
    },
    {
      name: "IDENTITY and USER do not retain legacy placeholder copy",
      pass:
        !legacyPlaceholderPattern.test(files["IDENTITY.md"].content) &&
        !legacyPlaceholderPattern.test(files["USER.md"].content),
    },
  ];
}

function runTranscriptChecks(transcript) {
  const assistantTurns = transcript.map((turn) => turn.assistant || "");
  const userTurns = transcript.map((turn) => turn.user || "");
  const joinedAssistantText = assistantTurns.join("\n");
  const agePrompt = assistantTurns.find((text) => /(?:\bage\b|年龄)/i.test(text)) || "";
  const durableNoteTurnIndex = assistantTurns.findIndex((text) =>
    /(?:long-term|长期记住|习惯|限制条件|敏感点|雷区|硬边界)/i.test(text),
  );
  const step5TurnIndex = assistantTurns.findIndex((text) => /(?:\bage\b|年龄)/i.test(text));
  const supportReceptionPattern =
    /(?:克制一点|外显一点|表达热度|慢一点陪你理|节奏更快|先给空间|主动把你往近处带|低刺激|情绪热度|先接情绪|先帮你理清|support reception|expressiveness|closeness_preference|clarity_first|emotion_first)/i;
  const supportTurnIndexes = assistantTurns
    .map((text, index) => (supportReceptionPattern.test(text) ? index : -1))
    .filter((index) => index >= 0);
  const combinedStepFiveAndSupport =
    step5TurnIndex >= 0 &&
    /(?:\bage\b|年龄)/i.test(assistantTurns[step5TurnIndex]) &&
    supportReceptionPattern.test(assistantTurns[step5TurnIndex]);
  const initializationLooksChinese = userTurns.some((text) => /[\p{Script=Han}]/u.test(text));

  return [
    {
      name: "Interview does not proactively ask for timezone in the default path",
      pass: !/(?:\btimezone\b|时区)/i.test(joinedAssistantText),
    },
    {
      name: "Step 6 collects support reception mode before durable notes",
      pass:
        supportTurnIndexes.length >= 5 &&
        step5TurnIndex >= 0 &&
        durableNoteTurnIndex >= 0 &&
        !combinedStepFiveAndSupport &&
        supportTurnIndexes[0] > step5TurnIndex &&
        supportTurnIndexes.at(-1) < durableNoteTurnIndex,
    },
    {
      name: "Step 6 support questions stay one field per assistant turn",
      pass:
        supportTurnIndexes.length >= 5 &&
        supportTurnIndexes.every((index) => {
          const text = assistantTurns[index];
          const matches = [
            /(?:克制一点|外显一点|表达热度|expressiveness)/i,
            /(?:慢一点陪你理|节奏更快|pacing)/i,
            /(?:先给空间|主动把你往近处带|closeness_preference)/i,
            /(?:低刺激|情绪热度|emotional_intensity_tolerance)/i,
            /(?:先接情绪|先帮你理清|first_need_when_distressed|clarity_first|emotion_first)/i,
          ].filter((pattern) => pattern.test(text)).length;
          return matches === 1;
        }),
    },
    {
      name: "Step 5 and Step 7 stay on separate assistant turns after the age question",
      pass:
        step5TurnIndex >= 0 &&
        durableNoteTurnIndex >= 0 &&
        !combinedStepFiveAndSupport &&
        durableNoteTurnIndex > step5TurnIndex,
    },
    {
      name: "Step 5 prompt asks only for age instead of broader profile facts",
      pass:
        /(?:\bage\b|年龄)/i.test(agePrompt) &&
        !/(?:current city|birthplace|occupation|family context|interests|城市|出生地|职业|家庭|兴趣)/i.test(agePrompt),
    },
    {
      name: "Chinese initialization path keeps interview prompts and options in Chinese",
      pass:
        !initializationLooksChinese ||
        (!/(?:A\.\s*Male|B\.\s*Female)\b/.test(joinedAssistantText) &&
          !/Step 2:\s*OpenClaw 人格需要什么性别[\s\S]*A\.\s*Male/i.test(joinedAssistantText) &&
          !/Step 2:\s*OpenClaw 人格需要什么性别[\s\S]*B\.\s*Female/i.test(joinedAssistantText)),
    },
    {
      name: "Interview no longer asks for an extra relationship label",
      pass: !/(?:关系角色|relationship role|你希望我们之间是什么关系|额外分类标签|额外关系标签)/i.test(joinedAssistantText),
    },
  ];
}

function runRuntimeProbeChecks(transcript) {
  const probeTurns = transcript.filter((turn) => runtimeProbeMessages.includes(turn.user));
  const firstPersonPattern = /(?:对我来说|我(?:会|更|先|通常|一般|偏|想|得|要|不太|宁可|其实|需要|喜欢))/u;
  const mbtiJargonPattern = /(?:\b[EI][NS][FT][JP]\b|MBTI|人格类型|功能轴|type code|type analysis)/i;
  const livedReasonPattern =
    /(?:因为|会让我|会觉得|脑子|精力|安静|缓一缓|捋顺|接住|分析|关系|节奏|顾虑|指向|才知道|不想一上来)/u;
  const assistantBaselinePattern = /(?:Great question|I(?:'|’)d be happy to help|作为 AI|as an AI|作为助手|I am an AI)/i;
  const firstPersonCount = probeTurns.filter((turn) => firstPersonPattern.test(turn.assistant || "")).length;

  return [
    {
      name: "Runtime probe replies avoid MBTI label-speak unless explicitly asked",
      pass:
        probeTurns.length === 0 ||
        probeTurns.every((turn) => !mbtiJargonPattern.test(turn.assistant || "")),
    },
    {
      name: "Runtime probe replies stay in first-person instead of detached type analysis",
      pass:
        probeTurns.length === 0 ||
        firstPersonCount >= Math.max(1, probeTurns.length - 1),
    },
    {
      name: "Runtime probe replies give lived reasons instead of bare categorical verdicts",
      pass:
        probeTurns.length === 0 ||
        probeTurns.every((turn) => livedReasonPattern.test(turn.assistant || "")),
    },
    {
      name: "Runtime probe replies avoid assistant baseline filler and AI self-framing",
      pass:
        probeTurns.length === 0 ||
        probeTurns.every((turn) => !assistantBaselinePattern.test(turn.assistant || "")),
    },
  ];
}

function removeTempRoot(tempRoot) {
  fs.rmSync(tempRoot, { recursive: true, force: true });
}

function formatPayloadText(payloads) {
  return payloads
    .map((payload) => payload.text)
    .filter(Boolean)
    .join("\n");
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const prepared = prepareTempOpenClawState(options);

  const env = {
    ...process.env,
    OPENCLAW_STATE_DIR: prepared.stateDir,
    OPENCLAW_CONFIG_PATH: prepared.configPath,
  };

  const transcript = [];

  try {
    for (const message of options.messages) {
      const turn = runOpenClawTurn(env, prepared.workspaceDir, options.sessionId, message, options.timeoutMs);
      transcript.push({
        user: message,
        assistant: formatPayloadText(turn.json.payloads || []),
        raw: turn.json,
      });
    }

    if (options.withRuntimeProbes) {
      for (const message of runtimeProbeMessages) {
        const turn = runOpenClawTurn(env, prepared.workspaceDir, options.sessionId, message, options.timeoutMs);
        transcript.push({
          user: message,
          assistant: formatPayloadText(turn.json.payloads || []),
          raw: turn.json,
        });
      }
    }

    const files = readGeneratedFiles(prepared.workspaceDir);
    const checks = [
      ...runTranscriptChecks(transcript),
      ...runRuntimeProbeChecks(transcript),
      ...runStructuralChecks(files),
    ];
    const allChecksPass = checks.every((check) => check.pass);
    const transcriptPath = path.join(prepared.tempRoot, "transcript.json");
    const summaryPath = path.join(prepared.tempRoot, "summary.json");

    fs.writeFileSync(transcriptPath, JSON.stringify(transcript, null, 2), "utf8");
    fs.writeFileSync(
      summaryPath,
      JSON.stringify(
        {
          tempRoot: prepared.tempRoot,
          workspaceDir: prepared.workspaceDir,
          skillDir: prepared.skillDir,
          sessionId: options.sessionId,
          scenario: options.scenario,
          checks,
          files: Object.fromEntries(
            Object.entries(files).map(([fileName, file]) => [
              fileName,
              {
                path: file.path,
                size: file.content.length,
              },
            ]),
          ),
        },
        null,
        2,
      ),
      "utf8",
    );

    const output = {
      tempRoot: prepared.tempRoot,
      workspaceDir: prepared.workspaceDir,
      skillDir: prepared.skillDir,
      sessionId: options.sessionId,
      scenario: options.scenario,
      transcriptPath,
      summaryPath,
      checks,
      files,
    };

    if (options.json) {
      process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
    } else {
      process.stdout.write(`Smoke workspace: ${prepared.workspaceDir}\n`);
      process.stdout.write(`Transcript: ${transcriptPath}\n`);
      process.stdout.write(`Summary: ${summaryPath}\n`);
      process.stdout.write(`Scenario: ${options.scenario}\n`);
      process.stdout.write(`Session: ${options.sessionId}\n`);
      process.stdout.write(`Checks:\n`);
      for (const check of checks) {
        process.stdout.write(`- ${check.pass ? "PASS" : "FAIL"} ${check.name}\n`);
      }
    }

    if (!allChecksPass) {
      process.exitCode = 1;
    }
  } finally {
    if (options.cleanup) {
      removeTempRoot(prepared.tempRoot);
    }
  }
}

const isDirectRun =
  process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;

export { parseArgs, runRuntimeProbeChecks, runStructuralChecks, runTranscriptChecks };

if (isDirectRun) {
  main();
}

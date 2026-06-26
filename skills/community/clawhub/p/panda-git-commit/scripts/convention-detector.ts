import { join } from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileExists, readJson, readText, getRepoRoot } from "./utils.ts";

const exec = promisify(execFile);

export interface ConventionRule {
  types?: string[];
  scopeRequired?: boolean;
  scopeEnum?: string[];
  subjectMaxLength?: number;
  subjectCase?: string;
  bodyMaxLineLength?: number;
  headerPattern?: string;
  footerPattern?: string;
}

export interface HistoryPattern {
  pattern: string;
  regex: string;
  confidence: number;
  examples: string[];
}

export interface ConventionResult {
  source: "commitlint" | "commitizen" | "git-hooks" | "git-history" | "default";
  format: "conventional-commits" | "angular" | "emoji-prefix" | "jira-prefix" | "custom" | "free-form";
  rules: ConventionRule;
  historyPattern: HistoryPattern | null;
  bestPractices: string[];
}

function extractCommitlintRules(config: Record<string, unknown>): ConventionRule {
  const rules: ConventionRule = {};
  const r = config.rules as Record<string, unknown[]> | undefined;
  if (!r) return rules;

  if (r["type-enum"]) {
    const [, , types] = r["type-enum"] as [number, string, string[]];
    if (Array.isArray(types)) rules.types = types;
  }

  if (r["scope-enum"]) {
    const [, , scopes] = r["scope-enum"] as [number, string, string[]];
    if (Array.isArray(scopes)) rules.scopeEnum = scopes;
  }

  if (r["scope-empty"]) {
    const [level, when] = r["scope-empty"] as [number, string];
    if (level >= 2 && when === "never") rules.scopeRequired = true;
  }

  if (r["header-max-length"]) {
    const [, , len] = r["header-max-length"] as [number, string, number];
    if (typeof len === "number") rules.subjectMaxLength = len;
  }

  if (r["subject-case"]) {
    const [, , caseVal] = r["subject-case"] as [number, string, string | string[]];
    if (typeof caseVal === "string") rules.subjectCase = caseVal;
    else if (Array.isArray(caseVal)) rules.subjectCase = caseVal[0];
  }

  if (r["body-max-line-length"]) {
    const [, , len] = r["body-max-line-length"] as [number, string, number];
    if (typeof len === "number") rules.bodyMaxLineLength = len;
  }

  return rules;
}

const COMMITLINT_FILES = [
  "commitlint.config.js",
  "commitlint.config.cjs",
  "commitlint.config.mjs",
  "commitlint.config.ts",
  ".commitlintrc",
  ".commitlintrc.json",
  ".commitlintrc.yml",
  ".commitlintrc.yaml",
  ".commitlintrc.js",
  ".commitlintrc.cjs",
  ".commitlintrc.ts",
];

const COMMITIZEN_FILES = [".czrc", ".cz-config.js", ".cz-config.cjs"];

async function detectCommitlint(root: string): Promise<ConventionRule | null> {
  let foundConfigFile = false;

  for (const file of COMMITLINT_FILES) {
    const p = join(root, file);
    if (!(await fileExists(p))) continue;

    if (file.endsWith(".json") || file === ".commitlintrc") {
      const data = await readJson(p);
      if (data && typeof data === "object") {
        return extractCommitlintRules(data as Record<string, unknown>);
      }
    }

    if (file.endsWith(".yml") || file.endsWith(".yaml")) {
      const text = await readText(p);
      if (text) {
        const rules: ConventionRule = {};
        const typeMatch = text.match(/type-enum[^[]*\[([^\]]+)\]/);
        if (typeMatch) {
          rules.types = typeMatch[1]
            .split(",")
            .map((s) => s.trim().replace(/['"]/g, ""))
            .filter(Boolean);
        }
        const maxLen = text.match(/header-max-length[^,\d]*(\d+)/);
        if (maxLen) rules.subjectMaxLength = parseInt(maxLen[1], 10);
        return rules;
      }
    }

    // JS/TS/MJS/CJS config exists but can't be parsed statically;
    // mark as found and continue to check package.json for supplementary rules
    foundConfigFile = true;
  }

  const pkg = (await readJson(join(root, "package.json"))) as Record<string, unknown> | null;
  if (pkg?.commitlint && typeof pkg.commitlint === "object") {
    return extractCommitlintRules(pkg.commitlint as Record<string, unknown>);
  }

  if (foundConfigFile) return {};

  return null;
}

async function detectCommitizen(root: string): Promise<ConventionRule | null> {
  for (const file of COMMITIZEN_FILES) {
    if (await fileExists(join(root, file))) {
      return {};
    }
  }

  const pkg = (await readJson(join(root, "package.json"))) as Record<string, unknown> | null;
  if (pkg?.config && typeof pkg.config === "object") {
    const config = pkg.config as Record<string, unknown>;
    if (config.commitizen) return {};
  }

  return null;
}

const HOOK_TOOL_PATTERNS = [
  /commitlint/,
  /npx\s+--\s+commitlint/,
  /cz-customizable/,
  /commit-msg-linter/,
  /gitlint/,
];

async function detectGitHooks(root: string): Promise<boolean> {
  const hookPaths = [
    join(root, ".git/hooks/commit-msg"),
    join(root, ".husky/commit-msg"),
    join(root, ".githooks/commit-msg"),
  ];

  for (const p of hookPaths) {
    if (await fileExists(p)) {
      const content = await readText(p);
      if (content && HOOK_TOOL_PATTERNS.some((re) => re.test(content))) {
        return true;
      }
    }
  }

  return false;
}

const CC_BREAKING_RE = /^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+?\))?!:\s/;
const CC_RE = /^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+?\))?:\s/;
const EMOJI_PREFIX_RE = /^(:[a-z_]+:|[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}])\s/u;
const JIRA_RE = /^\[?[A-Z]{2,10}-\d+\]?\s*[:：]?\s/;

interface PatternCount {
  cc: number;
  emoji: number;
  jira: number;
  free: number;
  total: number;
}

async function analyzeHistory(): Promise<{ pattern: HistoryPattern; rules: ConventionRule } | null> {
  try {
    const { stdout } = await exec("git", ["log", "--oneline", "--format=%s", "-50"]);
    const lines = stdout.trim().split("\n").filter(Boolean);
    if (lines.length < 3) return null;

    const counts: PatternCount = { cc: 0, emoji: 0, jira: 0, free: 0, total: lines.length };
    let hasBreaking = false;
    const detectedTypes = new Set<string>();
    const examples: Record<string, string[]> = { cc: [], emoji: [], jira: [], free: [] };

    for (const line of lines) {
      if (CC_BREAKING_RE.test(line)) {
        counts.cc++;
        hasBreaking = true;
        const m = line.match(CC_BREAKING_RE);
        if (m) detectedTypes.add(m[1]);
        if (examples.cc.length < 3) examples.cc.push(line);
      } else if (CC_RE.test(line)) {
        counts.cc++;
        const m = line.match(CC_RE);
        if (m) detectedTypes.add(m[1]);
        if (examples.cc.length < 3) examples.cc.push(line);
      } else if (JIRA_RE.test(line)) {
        counts.jira++;
        if (examples.jira.length < 3) examples.jira.push(line);
      } else if (EMOJI_PREFIX_RE.test(line)) {
        counts.emoji++;
        if (examples.emoji.length < 3) examples.emoji.push(line);
      } else {
        counts.free++;
        if (examples.free.length < 3) examples.free.push(line);
      }
    }

    let dominant: keyof Omit<PatternCount, "total"> = "free";
    let maxCount = 0;
    for (const key of ["cc", "emoji", "jira", "free"] as const) {
      if (counts[key] > maxCount) {
        dominant = key;
        maxCount = counts[key];
      }
    }

    const confidence = maxCount / counts.total;
    if (confidence < 0.3) return null;

    const formatMap: Record<string, ConventionResult["format"]> = {
      cc: "conventional-commits",
      emoji: "emoji-prefix",
      jira: "jira-prefix",
      free: "free-form",
    };

    const regexMap: Record<string, string> = {
      cc: hasBreaking ? "^(type)(\\\\(scope\\\\))?!?:\\\\s" : "^(type)(\\\\(scope\\\\))?:\\\\s",
      emoji: "^(emoji)\\\\s",
      jira: "^\\\\[?[A-Z]+-\\\\d+\\\\]?\\\\s*:?\\\\s",
      free: ".*",
    };

    const rules: ConventionRule = {};
    if (dominant === "cc") {
      rules.types = [...detectedTypes].sort();
    }

    return {
      pattern: {
        pattern: formatMap[dominant],
        regex: regexMap[dominant],
        confidence,
        examples: examples[dominant],
      },
      rules,
    };
  } catch {
    return null;
  }
}

export function computeBestPractices(
  source: ConventionResult["source"],
  rules: ConventionRule
): string[] {
  const tips: string[] = [];

  if (!rules.subjectMaxLength) {
    tips.push("subject 行建议不超过 72 字符");
  }

  if (!rules.bodyMaxLineLength) {
    tips.push("body 每行建议不超过 80 字符");
  }

  if (!rules.subjectCase) {
    tips.push("subject 使用祈使语气（中文：添加/修复/更新；英文：add/fix/update）");
  }
  tips.push("body 解释「为什么」变更，而非「做了什么」");
  tips.push("不相关的变更应拆分为独立 commit");

  if (!rules.types || rules.types.length === 0) {
    tips.push("建议使用 Conventional Commits 的标准 type：feat, fix, docs, style, refactor, perf, test, chore, ci, build");
  }

  if (source === "git-history" || source === "default") {
    tips.push("BREAKING CHANGE 应在 footer 中声明或在 type 后加 !");
    tips.push("关联 issue 使用 Closes #N 或 Fixes #N");
  }

  return tips;
}

export async function detectConvention(root?: string): Promise<ConventionResult> {
  const repoRoot = root ?? (await getRepoRoot());

  const commitlintRules = await detectCommitlint(repoRoot);
  if (commitlintRules) {
    return {
      source: "commitlint",
      format: "conventional-commits",
      rules: commitlintRules,
      historyPattern: null,
      bestPractices: computeBestPractices("commitlint", commitlintRules),
    };
  }

  const commitizenRules = await detectCommitizen(repoRoot);
  if (commitizenRules) {
    return {
      source: "commitizen",
      format: "conventional-commits",
      rules: commitizenRules,
      historyPattern: null,
      bestPractices: computeBestPractices("commitizen", commitizenRules),
    };
  }

  const hasHooks = await detectGitHooks(repoRoot);
  if (hasHooks) {
    return {
      source: "git-hooks",
      format: "conventional-commits",
      rules: {},
      historyPattern: null,
      bestPractices: computeBestPractices("git-hooks", {}),
    };
  }

  const historyResult = await analyzeHistory();
  if (historyResult) {
    return {
      source: "git-history",
      format: historyResult.pattern.pattern as ConventionResult["format"],
      rules: historyResult.rules,
      historyPattern: historyResult.pattern,
      bestPractices: computeBestPractices("git-history", historyResult.rules),
    };
  }

  return {
    source: "default",
    format: "conventional-commits",
    rules: {
      types: ["feat", "fix", "docs", "style", "refactor", "perf", "test", "chore", "ci", "build"],
    },
    historyPattern: null,
    bestPractices: computeBestPractices("default", {}),
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const result = await detectConvention();
  console.log(JSON.stringify(result, null, 2));
}

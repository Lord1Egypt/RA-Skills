import { analyzeDiff, detectLanguage, inferCommitType } from "./analyzer.ts";
import { detectMonorepo, inferScopesFromFiles } from "./scope-detector.ts";
import { splitByFunction, formatSplitSuggestion } from "./splitter.ts";
import { detectConvention } from "./convention-detector.ts";
import {
  loadExtendConfig,
  conventionFromExtend,
  monorepoFromExtend,
  generateExtend,
  mergeExtend,
  writeExtend,
  findExtendPath,
} from "./extend-generator.ts";
import { readText } from "./utils.ts";
import type { ConventionResult } from "./convention-detector.ts";
import type { MonorepoInfo } from "./scope-detector.ts";

interface CliArgs {
  split: boolean;
  scope: string | null;
  type: string | null;
  lang: string | null;
  dryRun: boolean;
  emoji: boolean;
  withDiff: boolean;
  init: boolean;
  refresh: boolean;
}

function isValue(v: string | undefined): v is string {
  return v !== undefined && !v.startsWith("--");
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    split: false,
    scope: null,
    type: null,
    lang: null,
    dryRun: false,
    emoji: false,
    withDiff: false,
    init: false,
    refresh: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--split") args.split = true;
    else if (arg === "--dry-run") args.dryRun = true;
    else if (arg === "--emoji") args.emoji = true;
    else if (arg === "--with-diff") args.withDiff = true;
    else if (arg === "--init") args.init = true;
    else if (arg === "--refresh") args.refresh = true;
    else if (arg === "--scope" && isValue(argv[i + 1])) args.scope = argv[++i];
    else if (arg === "--type" && isValue(argv[i + 1])) args.type = argv[++i];
    else if (arg === "--lang" && isValue(argv[i + 1])) args.lang = argv[++i];
  }

  return args;
}

const EMOJI_MAP: Record<string, string> = {
  feat: "✨",
  fix: "🐛",
  docs: "📝",
  style: "💄",
  refactor: "♻️",
  perf: "⚡",
  test: "✅",
  chore: "🔧",
  ci: "👷",
  build: "📦",
};

async function handleInit(args: CliArgs) {
  const [lang, monorepo, convention] = await Promise.all([
    args.lang ? Promise.resolve(args.lang) : detectLanguage(),
    detectMonorepo(),
    detectConvention(),
  ]);

  const detected = generateExtend(lang, convention, monorepo);

  const extPath = await findExtendPath();
  let finalContent: string;

  if (extPath) {
    const existing = await readText(extPath);
    if (existing) {
      finalContent = mergeExtend(existing, detected, args.refresh);
    } else {
      finalContent = detected;
    }
  } else {
    finalContent = detected;
  }

  const outPath = await writeExtend(finalContent);

  console.log(
    JSON.stringify(
      {
        action: args.refresh ? "refresh" : "init",
        path: outPath,
        language: lang,
        convention: {
          source: convention.source,
          format: convention.format,
        },
        monorepo: {
          isMonorepo: monorepo.isMonorepo,
          tool: monorepo.tool,
        },
        message: args.refresh
          ? "EXTEND.md 已刷新，项目配置已重新检测。"
          : "EXTEND.md 已生成，后续运行将跳过重复检测。",
      },
      null,
      2,
    ),
  );
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.init || args.refresh) {
    await handleInit(args);
    return;
  }

  const extConfig = await loadExtendConfig();

  let lang: string;
  let convention: ConventionResult;
  let monorepo: MonorepoInfo;
  let useEmoji = args.emoji;
  let cachedHint: string | null = null;

  if (extConfig?.convention?.source) {
    const extLang = extConfig.settings.language;
    lang = args.lang ?? (extLang && extLang !== "auto" ? extLang : null) ?? (await detectLanguage());

    const cachedConvention = conventionFromExtend(extConfig);
    convention = cachedConvention ?? (await detectConvention());

    const cachedMonorepo = monorepoFromExtend(extConfig);
    monorepo = cachedMonorepo ?? (await detectMonorepo());

    useEmoji = args.emoji || (extConfig.settings.emoji ?? false);
  } else {
    const [detectedLang, detectedMonorepo, detectedConvention] = await Promise.all([
      args.lang ? Promise.resolve(args.lang) : detectLanguage(),
      detectMonorepo(),
      detectConvention(),
    ]);
    lang = detectedLang;
    monorepo = detectedMonorepo;
    convention = detectedConvention;
    useEmoji = args.emoji;

    cachedHint = "提示：运行 /panda-git-commit --init 可缓存项目配置，后续运行将跳过重复检测。";
  }

  const diff = await analyzeDiff();

  if (!diff.hasStagedChanges) {
    const unstaged = await analyzeDiff(false);
    if (unstaged.files.length === 0) {
      console.log(
        JSON.stringify({
          error: "no_changes",
          message: "没有检测到任何变更。请先修改文件后再运行。",
        }),
      );
      process.exit(1);
    }

    console.log(
      JSON.stringify({
        warning: "no_staged_changes",
        message: "没有 staged 变更。请先运行 git add 将变更加入暂存区。",
        unstaged: {
          fileCount: unstaged.files.length,
          files: unstaged.files.map((f) => ({
            path: f.path,
            status: f.status,
          })),
        },
      }),
    );
    process.exit(1);
  }

  const customMapping = extConfig?.scopeMapping;
  const scopeResult = inferScopesFromFiles(
    diff.files.map((f) => f.path),
    monorepo,
    customMapping,
  );

  const shouldSplit = args.split || scopeResult.shouldSplit;

  if (shouldSplit) {
    const groups = splitByFunction(diff.files, monorepo, customMapping);

    const allowedTypes = convention.rules.types;
    for (const g of groups) {
      if (args.type && groups.length === 1) {
        g.type = args.type;
      } else if (allowedTypes && allowedTypes.length > 0 && !allowedTypes.includes(g.type)) {
        g.type = allowedTypes.includes("fix") ? "fix" : allowedTypes[0];
      }
    }

    const splitOutput: Record<string, unknown> = {
      mode: "split",
      language: lang,
      convention,
      monorepo: {
        isMonorepo: monorepo.isMonorepo,
        tool: monorepo.tool,
      },
      groups: groups.map((g) => {
        const emoji = useEmoji ? EMOJI_MAP[g.type] ?? "" : "";
        return {
          type: g.type,
          scope: args.scope ?? g.scope,
          emoji,
          files: g.files.map((f) => ({
            path: f.path,
            status: f.status,
            additions: f.additions,
            deletions: f.deletions,
          })),
        };
      }),
      suggestion: formatSplitSuggestion(groups, lang),
      dryRun: args.dryRun,
    };
    if (cachedHint) splitOutput.hint = cachedHint;
    if (args.withDiff) splitOutput.rawDiff = diff.rawDiff;
    console.log(JSON.stringify(splitOutput, null, 2));
  } else {
    let type = args.type ?? inferCommitType(diff.files);
    const allowedTypes = convention.rules.types;
    if (allowedTypes && allowedTypes.length > 0 && !allowedTypes.includes(type)) {
      type = allowedTypes.includes("fix") ? "fix" : allowedTypes[0];
    }
    const scope = args.scope ?? scopeResult.scope;
    const emoji = useEmoji ? EMOJI_MAP[type] ?? "" : "";

    const singleOutput: Record<string, unknown> = {
      mode: "single",
      language: lang,
      convention,
      monorepo: {
        isMonorepo: monorepo.isMonorepo,
        tool: monorepo.tool,
      },
      type,
      scope,
      emoji,
      files: diff.files.map((f) => ({
        path: f.path,
        status: f.status,
        additions: f.additions,
        deletions: f.deletions,
      })),
      totalAdditions: diff.totalAdditions,
      totalDeletions: diff.totalDeletions,
      dryRun: args.dryRun,
    };
    if (cachedHint) singleOutput.hint = cachedHint;
    if (args.withDiff) singleOutput.rawDiff = diff.rawDiff;
    console.log(JSON.stringify(singleOutput, null, 2));
  }
}

main().catch((e) => {
  console.error(JSON.stringify({ error: "unexpected", message: String(e) }));
  process.exit(1);
});

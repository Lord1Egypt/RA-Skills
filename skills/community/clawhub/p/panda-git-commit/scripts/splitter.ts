import type { DiffFile } from "./analyzer.ts";
import type { MonorepoInfo } from "./scope-detector.ts";
import { inferScope, inferScopesFromFiles } from "./scope-detector.ts";
import { inferCommitType } from "./analyzer.ts";

export interface CommitGroup {
  type: string;
  scope: string | null;
  files: DiffFile[];
  description: string;
}

const TEST_RE = /\.(test|spec)\.[jt]sx?$|__tests__\//;

function isTestFile(path: string): boolean {
  return TEST_RE.test(path);
}

function getSourcePath(testPath: string): string {
  return testPath
    .replace(/__tests__\//, "")
    .replace(/\.(test|spec)\./, ".");
}

export function groupByScope(
  files: DiffFile[],
  monorepo: MonorepoInfo,
  customMapping?: Record<string, string>
): Map<string, DiffFile[]> {
  const groups = new Map<string, DiffFile[]>();

  for (const f of files) {
    const scope = inferScope(f.path, monorepo, customMapping) ?? "_root";
    const arr = groups.get(scope) ?? [];
    arr.push(f);
    groups.set(scope, arr);
  }

  return groups;
}

export function splitByFunction(
  files: DiffFile[],
  monorepo: MonorepoInfo,
  customMapping?: Record<string, string>
): CommitGroup[] {
  const groups: CommitGroup[] = [];
  const scopeGroups = groupByScope(files, monorepo, customMapping);

  for (const [scope, scopeFiles] of scopeGroups) {
    const testFiles: DiffFile[] = [];
    const sourceFiles: DiffFile[] = [];

    for (const f of scopeFiles) {
      if (isTestFile(f.path)) {
        testFiles.push(f);
      } else {
        sourceFiles.push(f);
      }
    }

    if (sourceFiles.length > 0) {
      const type = inferCommitType(sourceFiles);
      const s = scope === "_root" ? null : scope;
      groups.push({
        type,
        scope: s,
        files: sourceFiles,
        description: "",
      });
    }

    if (testFiles.length > 0) {
      const hasMatchingSource = testFiles.some((t) => {
        const src = getSourcePath(t.path);
        return sourceFiles.some((s) => s.path === src);
      });

      if (hasMatchingSource && sourceFiles.length > 0) {
        const srcGroup = groups.find(
          (g) => g.scope === (scope === "_root" ? null : scope) && g.type !== "test"
        );
        if (srcGroup) {
          srcGroup.files.push(...testFiles);
          continue;
        }
      }

      const s = scope === "_root" ? null : scope;
      groups.push({
        type: "test",
        scope: s,
        files: testFiles,
        description: "",
      });
    }
  }

  return groups;
}

export function formatSplitSuggestion(
  groups: CommitGroup[],
  lang: string
): string {
  const isZh = lang === "zh";
  const header = isZh
    ? `建议拆分为 ${groups.length} 个 commit：`
    : `Suggest splitting into ${groups.length} commits:`;

  const statusLabel = isZh
    ? { added: "新增", modified: "修改", deleted: "删除", renamed: "重命名" }
    : { added: "added", modified: "modified", deleted: "deleted", renamed: "renamed" };
  const lines = [header, ""];

  for (let i = 0; i < groups.length; i++) {
    const g = groups[i];
    const scopePart = g.scope ? `(${g.scope})` : "";
    lines.push(`  ${i + 1}. ${g.type}${scopePart}: ${g.description || "..."}`);

    for (const f of g.files) {
      lines.push(`     - ${f.path} (${statusLabel[f.status]})`);
    }

    if (i < groups.length - 1) lines.push("");
  }

  return lines.join("\n");
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const { analyzeDiff } = await import("./analyzer.ts");
  const { detectMonorepo } = await import("./scope-detector.ts");

  const diff = await analyzeDiff();
  const monorepo = await detectMonorepo();

  if (diff.files.length === 0) {
    console.log(JSON.stringify({ groups: [], message: "没有变更文件" }));
    process.exit(0);
  }

  const groups = splitByFunction(diff.files, monorepo);
  const scopeResult = inferScopesFromFiles(
    diff.files.map((f) => f.path),
    monorepo
  );

  console.log(
    JSON.stringify(
      {
        shouldSplit: groups.length > 1,
        groups: groups.map((g) => ({
          type: g.type,
          scope: g.scope,
          files: g.files.map((f) => ({ path: f.path, status: f.status })),
        })),
        scopes: scopeResult.scopes,
        suggestion: groups.length > 1 ? formatSplitSuggestion(groups, "zh") : null,
      },
      null,
      2
    )
  );
}

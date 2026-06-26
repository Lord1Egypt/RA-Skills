import { execFile } from "node:child_process";
import { promisify } from "node:util";

const exec = promisify(execFile);

export interface DiffFile {
  path: string;
  status: "added" | "modified" | "deleted" | "renamed";
  additions: number;
  deletions: number;
}

export interface DiffAnalysis {
  files: DiffFile[];
  totalAdditions: number;
  totalDeletions: number;
  rawDiff: string;
  hasStagedChanges: boolean;
}

export type DetectedLang = "zh" | "en" | "ja" | "ko";

const CJK_RE = /[\u4e00-\u9fff]/;
const KANA_RE = /[\u3040-\u309f\u30a0-\u30ff]/;
const HANGUL_RE = /[\uac00-\ud7af]/;

export async function detectLanguage(): Promise<DetectedLang> {
  try {
    const { stdout } = await exec("git", [
      "log",
      "--oneline",
      "--format=%s",
      "-20",
    ]);
    const lines = stdout.trim().split("\n").filter(Boolean);
    if (lines.length === 0) return "en";

    const counts: Record<DetectedLang, number> = { zh: 0, en: 0, ja: 0, ko: 0 };

    for (const line of lines) {
      const stripped = line.replace(/^[a-z]+(\([^)]*\))?[!:]?\s*/i, "");
      if (KANA_RE.test(stripped)) counts.ja++;
      else if (HANGUL_RE.test(stripped)) counts.ko++;
      else if (CJK_RE.test(stripped)) counts.zh++;
      else counts.en++;
    }

    let max: DetectedLang = "en";
    let maxCount = 0;
    for (const [lang, count] of Object.entries(counts) as [DetectedLang, number][]) {
      if (count > maxCount) {
        max = lang;
        maxCount = count;
      }
    }
    return max;
  } catch {
    return "en";
  }
}

function parseStatus(s: string): DiffFile["status"] {
  if (s.startsWith("A")) return "added";
  if (s.startsWith("D")) return "deleted";
  if (s.startsWith("R")) return "renamed";
  return "modified";
}

export async function analyzeDiff(staged = true): Promise<DiffAnalysis> {
  const stageFlag = staged ? ["--staged"] : [];

  const [numstatResult, nameStatusResult, rawDiffResult] = await Promise.all([
    exec("git", ["diff", ...stageFlag, "--numstat"]).catch(() => ({ stdout: "" })),
    exec("git", ["diff", ...stageFlag, "--name-status"]).catch(() => ({ stdout: "" })),
    exec("git", ["diff", ...stageFlag]).catch(() => ({ stdout: "" })),
  ]);

  const files: DiffFile[] = [];
  let totalAdditions = 0;
  let totalDeletions = 0;

  // --name-status: build a map from file path → status (handles renames)
  const statusMap = new Map<string, DiffFile["status"]>();
  for (const line of nameStatusResult.stdout.trim().split("\n").filter(Boolean)) {
    const [status, ...pathParts] = line.split("\t");
    // For renames, pathParts = [oldPath, newPath]; use newPath as key
    const filePath = pathParts[pathParts.length - 1];
    if (filePath) statusMap.set(filePath, parseStatus(status));
  }

  // --numstat: build file list with additions/deletions
  for (const line of numstatResult.stdout.trim().split("\n").filter(Boolean)) {
    const [add, del, ...pathParts] = line.split("\t");
    let filePath = pathParts.join("\t");

    // git numstat shows renames as "{old => new}/path" or "dir/{old => new}"
    const renameMatch = filePath.match(/\{(.+?) => (.+?)\}/);
    if (renameMatch) {
      filePath = filePath.replace(/\{.+? => (.+?)\}/, "$1");
    }

    const additions = add === "-" ? 0 : parseInt(add, 10);
    const deletions = del === "-" ? 0 : parseInt(del, 10);
    totalAdditions += additions;
    totalDeletions += deletions;

    const status = statusMap.get(filePath) ?? "modified";
    files.push({ path: filePath, status, additions, deletions });
  }

  return {
    files,
    totalAdditions,
    totalDeletions,
    rawDiff: rawDiffResult.stdout,
    hasStagedChanges: staged && files.length > 0,
  };
}

export function inferCommitType(
  files: DiffFile[]
): string {
  const paths = files.map((f) => f.path);

  const allTests = paths.every(
    (p) => p.includes("test") || p.includes("spec") || p.includes("__tests__")
  );
  if (allTests) return "test";

  const allDocs = paths.every(
    (p) =>
      p.endsWith(".md") ||
      p.endsWith(".txt") ||
      p.endsWith(".rst") ||
      p.includes("docs/")
  );
  if (allDocs) return "docs";

  const allCi = paths.every(
    (p) =>
      p.includes(".github/") ||
      p.includes(".gitlab-ci") ||
      p.includes("Jenkinsfile") ||
      p.includes(".circleci/")
  );
  if (allCi) return "ci";

  const allBuild = paths.every(
    (p) =>
      p === "package.json" ||
      p === "tsconfig.json" ||
      p.includes("webpack") ||
      p.includes("vite.config") ||
      p.includes("rollup") ||
      p === "Dockerfile" ||
      p === "docker-compose.yml"
  );
  if (allBuild) return "build";

  const allStyle = paths.every(
    (p) =>
      p.endsWith(".css") ||
      p.endsWith(".scss") ||
      p.endsWith(".less") ||
      p.endsWith(".styled.ts") ||
      p.endsWith(".styled.tsx")
  );
  if (allStyle) return "style";

  const hasNew = files.some((f) => f.status === "added");
  if (hasNew) return "feat";

  const allDeleted = files.every((f) => f.status === "deleted");
  if (allDeleted) return "chore";

  const totalChanges = files.reduce((s, f) => s + f.additions + f.deletions, 0);
  const totalDeletions = files.reduce((s, f) => s + f.deletions, 0);
  if (totalChanges > 0 && totalDeletions / totalChanges > 0.6) return "refactor";

  return "fix";
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const lang = await detectLanguage();
  const diff = await analyzeDiff();

  if (!diff.hasStagedChanges) {
    const unstaged = await analyzeDiff(false);
    console.log(
      JSON.stringify(
        {
          language: lang,
          staged: diff,
          unstaged,
          suggestedType: unstaged.files.length > 0
            ? inferCommitType(unstaged.files)
            : null,
          warning: "no_staged_changes",
        },
        null,
        2
      )
    );
  } else {
    console.log(
      JSON.stringify(
        {
          language: lang,
          staged: diff,
          suggestedType: inferCommitType(diff.files),
        },
        null,
        2
      )
    );
  }
}

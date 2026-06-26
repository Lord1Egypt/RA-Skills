import { readFile, readdir } from "node:fs/promises";
import { join } from "node:path";
import { fileExists, readJson, getRepoRoot } from "./utils.ts";

export interface MonorepoInfo {
  isMonorepo: boolean;
  tool: string | null;
  workspaceDirs: string[];
  packageMap: Record<string, string>;
}

export interface ScopeResult {
  scope: string | null;
  scopes: string[];
  monorepo: MonorepoInfo;
  shouldSplit: boolean;
}

async function resolveGlobs(root: string, patterns: string[]): Promise<string[]> {
  const dirs: string[] = [];
  for (const pattern of patterns) {
    if (pattern.includes("*")) {
      const base = pattern.replace(/\/\*.*$/, "");
      const basePath = join(root, base);
      try {
        const entries = await readdir(basePath, { withFileTypes: true });
        for (const e of entries) {
          if (e.isDirectory()) dirs.push(join(base, e.name));
        }
      } catch {
        // ignore
      }
    } else {
      dirs.push(pattern);
    }
  }
  return dirs;
}

export async function detectMonorepo(root?: string): Promise<MonorepoInfo> {
  const repoRoot = root ?? (await getRepoRoot());
  const result: MonorepoInfo = {
    isMonorepo: false,
    tool: null,
    workspaceDirs: [],
    packageMap: {},
  };

  const pkgPath = join(repoRoot, "package.json");
  const pkg = (await readJson(pkgPath)) as Record<string, unknown> | null;

  if (pkg?.workspaces) {
    result.isMonorepo = true;
    const ws = Array.isArray(pkg.workspaces)
      ? pkg.workspaces
      : (pkg.workspaces as Record<string, unknown>)?.packages;

    if (Array.isArray(ws)) {
      result.workspaceDirs = await resolveGlobs(repoRoot, ws as string[]);
      result.tool = "npm/yarn workspaces";
    }
  }

  if (!result.isMonorepo && (await fileExists(join(repoRoot, "pnpm-workspace.yaml")))) {
    try {
      const raw = await readFile(join(repoRoot, "pnpm-workspace.yaml"), "utf-8");
      const pkgLines = raw
        .split("\n")
        .filter((l) => l.trim().startsWith("- "))
        .map((l) => l.trim().replace(/^-\s+['"]?/, "").replace(/['"]?\s*(#.*)?$/, ""));
      result.isMonorepo = true;
      result.tool = "pnpm workspaces";
      result.workspaceDirs = await resolveGlobs(repoRoot, pkgLines);
    } catch {
      // ignore
    }
  }

  if (!result.isMonorepo && (await fileExists(join(repoRoot, "lerna.json")))) {
    const lerna = (await readJson(join(repoRoot, "lerna.json"))) as Record<string, unknown> | null;
    if (lerna) {
      result.isMonorepo = true;
      result.tool = "lerna";
      const pkgs = (lerna.packages as string[]) ?? ["packages/*"];
      result.workspaceDirs = await resolveGlobs(repoRoot, pkgs);
    }
  }

  if (!result.isMonorepo && (await fileExists(join(repoRoot, "nx.json")))) {
    result.isMonorepo = true;
    result.tool = "nx";
    const defaultDirs = ["packages/*", "apps/*", "libs/*"];
    result.workspaceDirs = await resolveGlobs(repoRoot, defaultDirs);
  }

  if (!result.isMonorepo && (await fileExists(join(repoRoot, "turbo.json")))) {
    result.isMonorepo = true;
    result.tool = "turborepo";
    if (pkg?.workspaces) {
      const ws = Array.isArray(pkg.workspaces)
        ? pkg.workspaces
        : (pkg.workspaces as Record<string, unknown>)?.packages;
      if (Array.isArray(ws)) {
        result.workspaceDirs = await resolveGlobs(repoRoot, ws as string[]);
      }
    } else {
      const defaultDirs = ["packages/*", "apps/*"];
      result.workspaceDirs = await resolveGlobs(repoRoot, defaultDirs);
    }
  }

  await buildPackageMap(repoRoot, result);

  return result;
}

async function buildPackageMap(root: string, info: MonorepoInfo): Promise<void> {
  const reads = info.workspaceDirs.map(async (dir) => {
    const dirPath = join(root, dir);

    // Nx: project.json name takes priority
    if (info.tool === "nx") {
      const proj = (await readJson(join(dirPath, "project.json"))) as Record<string, unknown> | null;
      if (proj?.name && typeof proj.name === "string") {
        info.packageMap[dir] = proj.name;
        return;
      }
    }

    // All tools: read package.json name
    const pkg = (await readJson(join(dirPath, "package.json"))) as Record<string, unknown> | null;
    if (pkg?.name && typeof pkg.name === "string") {
      info.packageMap[dir] = pkg.name;
      return;
    }

    // Fallback: directory name
    info.packageMap[dir] = dir.split("/").pop() ?? dir;
  });

  await Promise.all(reads);
}

export function inferScope(
  filePath: string,
  monorepo: MonorepoInfo,
  customMapping?: Record<string, string>
): string | null {
  if (customMapping) {
    for (const [pattern, scope] of Object.entries(customMapping)) {
      if (filePath.startsWith(pattern)) return scope;
    }
  }

  if (monorepo.isMonorepo) {
    for (const [dir, name] of Object.entries(monorepo.packageMap)) {
      if (filePath.startsWith(dir + "/") || filePath === dir) return name;
    }
  }

  const parts = filePath.split("/");
  if (parts.length >= 2) {
    const topDir = parts[0];
    if (["src", "lib", "app"].includes(topDir) && parts.length >= 3) {
      return parts[1];
    }
    if (![".", ".."].includes(topDir)) {
      return topDir;
    }
  }

  return null;
}

export function inferScopesFromFiles(
  files: string[],
  monorepo: MonorepoInfo,
  customMapping?: Record<string, string>
): ScopeResult {
  const scopeSet = new Set<string>();

  for (const f of files) {
    const s = inferScope(f, monorepo, customMapping);
    if (s) scopeSet.add(s);
  }

  const scopes = [...scopeSet].sort();
  const shouldSplit = scopes.length > 1;
  const scope = scopes.length === 1 ? scopes[0] : null;

  return { scope, scopes, monorepo, shouldSplit };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const monorepo = await detectMonorepo();
  console.log(JSON.stringify(monorepo, null, 2));
}

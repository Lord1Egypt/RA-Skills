import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
import type { DiscoveredFile, SkillMetadata } from './types.js';

const HARDCODED_IGNORES: readonly string[] = [
  'node_modules',
  '.git',
  'dist',
  'coverage',
  '.saturnday',
];

export function loadIgnorePatterns(skillDir: string): string[] {
  const ignorePath = path.join(skillDir, '.skillignore');
  const patterns = [...HARDCODED_IGNORES];

  try {
    const content = fs.readFileSync(ignorePath, 'utf-8');
    for (const raw of content.split('\n')) {
      const line = raw.trim();
      if (line === '' || line.startsWith('#')) continue;
      if (!patterns.includes(line)) {
        patterns.push(line);
      }
    }
  } catch {
    // .skillignore does not exist — return hardcoded list only
  }

  return patterns;
}

export function shouldIgnoreEntry(
  entryName: string,
  ignorePatterns: string[],
  isSymlink: boolean,
): boolean {
  if (isSymlink) return true;
  return ignorePatterns.includes(entryName);
}

export async function discoverFiles(skillDir: string): Promise<string[]> {
  const ignorePatterns = loadIgnorePatterns(skillDir);
  const results: string[] = [];

  let entries: fs.Dirent[];
  try {
    entries = await fs.promises.readdir(skillDir, { recursive: true, withFileTypes: true });
  } catch {
    return results;
  }

  for (const entry of entries) {
    const parentDir = entry.parentPath;
    const fullPath = path.join(parentDir, entry.name);
    const stat = await fs.promises.lstat(fullPath);

    if (shouldIgnoreEntry(entry.name, ignorePatterns, stat.isSymbolicLink())) continue;
    if (!stat.isFile()) continue;

    const relativePath = path.relative(skillDir, fullPath);
    const segments = relativePath.split(path.sep);

    if (segments.slice(0, -1).some(seg => shouldIgnoreEntry(seg, ignorePatterns, false))) {
      continue;
    }

    results.push(segments.join('/'));
  }

  results.sort();
  return results;
}

const DEFAULT_METADATA: SkillMetadata = {
  name: 'unknown',
  version: 'unknown',
  declaredPermissions: [],
  declaredDependencies: {},
};

export function parseSkillFrontmatter(content: string): Partial<SkillMetadata> {
  const lines = content.split('\n');

  if (lines[0]?.trim() !== '---') {
    return {};
  }

  let closingIndex = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i]?.trim() === '---') {
      closingIndex = i;
      break;
    }
  }

  if (closingIndex === -1) {
    return {};
  }

  const yamlBlock = lines.slice(1, closingIndex).join('\n');
  if (yamlBlock.trim() === '') {
    return {};
  }

  let parsed: unknown;
  try {
    parsed = yaml.load(yamlBlock);
  } catch {
    console.warn('permission-manifest-guard: malformed YAML frontmatter in SKILL.md, using defaults');
    return {};
  }

  if (typeof parsed !== 'object' || parsed === null) {
    return {};
  }

  const doc = parsed as Record<string, unknown>;
  const result: Partial<SkillMetadata> = {};

  if (typeof doc.name === 'string') {
    result.name = doc.name;
  }
  if (typeof doc.version === 'string') {
    result.version = doc.version;
  }
  if (Array.isArray(doc.permissions)) {
    result.declaredPermissions = doc.permissions.filter(
      (p: unknown): p is string => typeof p === 'string',
    );
  }

  return result;
}

export function parsePackageJson(content: string): Partial<SkillMetadata> {
  let pkg: Record<string, unknown>;
  try {
    const parsed = JSON.parse(content);
    if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
      return {};
    }
    pkg = parsed as Record<string, unknown>;
  } catch {
    console.warn('permission-manifest-guard: malformed JSON in package.json, using defaults');
    return {};
  }

  const result: Partial<SkillMetadata> = {};
  const deps: Record<string, string> = {};

  if (typeof pkg.dependencies === 'object' && pkg.dependencies !== null) {
    for (const [key, val] of Object.entries(pkg.dependencies as Record<string, unknown>)) {
      if (typeof val === 'string') {
        deps[key] = val;
      }
    }
  }

  if (typeof pkg.devDependencies === 'object' && pkg.devDependencies !== null) {
    for (const [key, val] of Object.entries(pkg.devDependencies as Record<string, unknown>)) {
      if (typeof val === 'string') {
        deps[key] = val;
      }
    }
  }

  result.declaredDependencies = deps;

  if (typeof pkg.openclaw === 'object' && pkg.openclaw !== null) {
    const oc = pkg.openclaw as Record<string, unknown>;
    if (Array.isArray(oc.permissions)) {
      result.declaredPermissions = oc.permissions.filter(
        (p: unknown): p is string => typeof p === 'string',
      );
    }
  }

  return result;
}

export async function readSkillMetadata(skillDir: string): Promise<SkillMetadata> {
  const metadata: SkillMetadata = { ...DEFAULT_METADATA, declaredPermissions: [], declaredDependencies: {} };

  const skillMdPath = path.join(skillDir, 'SKILL.md');
  try {
    const content = await fs.promises.readFile(skillMdPath, 'utf-8');
    const partial = parseSkillFrontmatter(content);
    if (partial.name !== undefined) metadata.name = partial.name;
    if (partial.version !== undefined) metadata.version = partial.version;
    if (partial.declaredPermissions !== undefined) metadata.declaredPermissions = partial.declaredPermissions;
  } catch {
    // SKILL.md missing — keep defaults
  }

  const pkgPath = path.join(skillDir, 'package.json');
  try {
    const raw = await fs.promises.readFile(pkgPath, 'utf-8');
    const partial = parsePackageJson(raw);
    if (partial.declaredDependencies !== undefined) {
      metadata.declaredDependencies = partial.declaredDependencies;
    }
    if (partial.declaredPermissions !== undefined) {
      for (const perm of partial.declaredPermissions) {
        if (!metadata.declaredPermissions.includes(perm)) {
          metadata.declaredPermissions.push(perm);
        }
      }
    }
  } catch {
    // package.json missing — keep defaults
  }

  return metadata;
}

export async function readDiscoveredFiles(
  filePaths: string[],
  skillDir: string,
): Promise<{ files: DiscoveredFile[]; diagnostics: string[] }> {
  const files: DiscoveredFile[] = [];
  const diagnostics: string[] = [];
  for (const relPath of filePaths) {
    try {
      const content = await fs.promises.readFile(path.join(skillDir, relPath), 'utf-8');
      files.push({ path: relPath, content });
    } catch (err) {
      diagnostics.push(`Failed to read ${relPath}: ${(err as Error).message}`);
    }
  }
  return { files, diagnostics };
}

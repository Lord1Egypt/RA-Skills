import { writeFile, mkdir } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileExists, readText, getRepoRoot } from "./utils.ts";
import { computeBestPractices } from "./convention-detector.ts";
import type { ConventionResult, ConventionRule } from "./convention-detector.ts";
import type { MonorepoInfo } from "./scope-detector.ts";
import type { DetectedLang } from "./analyzer.ts";

export interface ExtendSettings {
  language?: string;
  max_subject_length?: number;
  body_wrap?: number;
  emoji?: boolean;
}

export interface ExtendConvention {
  source?: string;
  format?: string;
  types?: string[];
  scope_required?: boolean;
  scope_enum?: string[];
  subject_max_length?: number;
  subject_case?: string;
  body_max_line_length?: number;
  is_monorepo?: boolean;
}

export interface ExtendConfig {
  settings: ExtendSettings;
  convention?: ExtendConvention;
  customTypes?: Record<string, string>;
  scopeMapping?: Record<string, string>;
  scopeAliases?: Record<string, string[]>;
  raw?: string;
}

const EXTEND_PATHS = [
  ".panda-skills/panda-git-commit/EXTEND.md",
];

function xdgPath(): string {
  const xdg = process.env.XDG_CONFIG_HOME ?? join(process.env.HOME ?? "", ".config");
  return join(xdg, "panda-skills/panda-git-commit/EXTEND.md");
}

function userPath(): string {
  return join(process.env.HOME ?? "", ".panda-skills/panda-git-commit/EXTEND.md");
}

export async function findExtendPath(root?: string): Promise<string | null> {
  const repoRoot = root ?? (await getRepoRoot());

  const projectPath = join(repoRoot, EXTEND_PATHS[0]);
  if (await fileExists(projectPath)) return projectPath;

  const xdg = xdgPath();
  if (await fileExists(xdg)) return xdg;

  const user = userPath();
  if (await fileExists(user)) return user;

  return null;
}

export function parseExtend(content: string): ExtendConfig {
  const config: ExtendConfig = { settings: {}, raw: content };
  const sections = splitSections(content);

  if (sections.Settings) {
    config.settings = parseKvList(sections.Settings) as ExtendSettings;
    if (config.settings.emoji !== undefined) {
      config.settings.emoji = String(config.settings.emoji) === "true";
    }
    for (const numKey of ["max_subject_length", "body_wrap"] as const) {
      if (config.settings[numKey] !== undefined) {
        (config.settings as Record<string, unknown>)[numKey] = Number(config.settings[numKey]);
      }
    }
  }

  if (sections.Convention) {
    const raw = parseKvList(sections.Convention) as Record<string, unknown>;
    const conv: ExtendConvention = {};
    if (raw.source) conv.source = String(raw.source);
    if (raw.format) conv.format = String(raw.format);
    if (raw.types) {
      conv.types = String(raw.types).split(",").map((s) => s.trim()).filter(Boolean);
    }
    if (raw.scope_required !== undefined) {
      conv.scope_required = String(raw.scope_required) === "true";
    }
    if (raw.scope_enum) {
      conv.scope_enum = String(raw.scope_enum).split(",").map((s) => s.trim()).filter(Boolean);
    }
    if (raw.subject_max_length) conv.subject_max_length = Number(raw.subject_max_length);
    if (raw.subject_case) conv.subject_case = String(raw.subject_case);
    if (raw.body_max_line_length) conv.body_max_line_length = Number(raw.body_max_line_length);
    if (raw.is_monorepo !== undefined) conv.is_monorepo = String(raw.is_monorepo) === "true";
    config.convention = conv;
  }

  if (sections["Custom Types"]) {
    config.customTypes = parseKvList(sections["Custom Types"]) as Record<string, string>;
  }

  if (sections["Scope Mapping"]) {
    config.scopeMapping = parseArrowList(sections["Scope Mapping"]);
  }

  if (sections["Scope Aliases"]) {
    const raw = parseKvList(sections["Scope Aliases"]) as Record<string, string>;
    config.scopeAliases = {};
    for (const [k, v] of Object.entries(raw)) {
      config.scopeAliases[k] = String(v).split(",").map((s) => s.trim()).filter(Boolean);
    }
  }

  return config;
}

function splitSections(content: string): Record<string, string> {
  const sections: Record<string, string> = {};
  let currentSection = "";
  const lines = content.split("\n");

  for (const line of lines) {
    const h2Match = line.match(/^## (.+)$/);
    if (h2Match) {
      currentSection = h2Match[1].trim();
      sections[currentSection] = "";
      continue;
    }
    // skip h3+ (templates sub-sections)
    if (line.startsWith("### ")) continue;
    if (currentSection) {
      sections[currentSection] += line + "\n";
    }
  }

  return sections;
}

function parseKvList(text: string): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const line of text.split("\n")) {
    const m = line.match(/^-\s+([^:]+):\s*(.+)$/);
    if (m) {
      result[m[1].trim()] = m[2].trim();
    }
  }
  return result;
}

function parseArrowList(text: string): Record<string, string> {
  const result: Record<string, string> = {};
  for (const line of text.split("\n")) {
    const m = line.match(/^-\s+(.+?)\s*->\s*(.+)$/);
    if (m) {
      result[m[1].trim()] = m[2].trim();
    }
  }
  return result;
}

export function conventionFromExtend(ext: ExtendConfig): ConventionResult | null {
  if (!ext.convention?.source) return null;

  const conv = ext.convention;
  const rules: ConventionRule = {};
  if (conv.types) rules.types = conv.types;
  if (conv.scope_required !== undefined) rules.scopeRequired = conv.scope_required;
  if (conv.scope_enum) rules.scopeEnum = conv.scope_enum;
  if (conv.subject_max_length) rules.subjectMaxLength = conv.subject_max_length;
  if (conv.subject_case) rules.subjectCase = conv.subject_case;
  if (conv.body_max_line_length) rules.bodyMaxLineLength = conv.body_max_line_length;

  const source = conv.source as ConventionResult["source"];

  return {
    source,
    format: (conv.format ?? "conventional-commits") as ConventionResult["format"],
    rules,
    historyPattern: null,
    bestPractices: computeBestPractices(source, rules),
  };
}

export function monorepoFromExtend(ext: ExtendConfig): MonorepoInfo | null {
  if (ext.convention?.is_monorepo === false) {
    return { isMonorepo: false, tool: null, workspaceDirs: [], packageMap: {} };
  }

  if (ext.scopeMapping && Object.keys(ext.scopeMapping).length > 0) {
    return {
      isMonorepo: true,
      tool: "extend-config",
      workspaceDirs: Object.keys(ext.scopeMapping),
      packageMap: ext.scopeMapping,
    };
  }

  return null;
}

export function generateExtend(
  lang: DetectedLang | string,
  convention: ConventionResult,
  monorepo: MonorepoInfo,
): string {
  const lines: string[] = [];

  lines.push("## Settings");
  lines.push("");
  lines.push(`- language: ${lang}`);
  lines.push("- max_subject_length: 72");
  lines.push("- body_wrap: 80");
  lines.push("- emoji: false");
  lines.push("");

  lines.push("## Convention");
  lines.push("");
  lines.push(`- source: ${convention.source}`);
  lines.push(`- format: ${convention.format}`);
  if (convention.rules.types?.length) {
    lines.push(`- types: ${convention.rules.types.join(", ")}`);
  }
  if (convention.rules.scopeRequired !== undefined) {
    lines.push(`- scope_required: ${convention.rules.scopeRequired}`);
  }
  if (convention.rules.scopeEnum?.length) {
    lines.push(`- scope_enum: ${convention.rules.scopeEnum.join(", ")}`);
  }
  if (convention.rules.subjectMaxLength) {
    lines.push(`- subject_max_length: ${convention.rules.subjectMaxLength}`);
  }
  if (convention.rules.subjectCase) {
    lines.push(`- subject_case: ${convention.rules.subjectCase}`);
  }
  if (convention.rules.bodyMaxLineLength) {
    lines.push(`- body_max_line_length: ${convention.rules.bodyMaxLineLength}`);
  }
  lines.push(`- is_monorepo: ${monorepo.isMonorepo}`);
  lines.push("");

  if (monorepo.isMonorepo && Object.keys(monorepo.packageMap).length > 0) {
    lines.push("## Scope Mapping");
    lines.push("");
    for (const [dir, name] of Object.entries(monorepo.packageMap)) {
      lines.push(`- ${dir} -> ${name}`);
    }
    lines.push("");
  }

  return lines.join("\n");
}

const AUTO_DETECTED_SECTIONS = new Set(["Settings", "Convention", "Scope Mapping"]);

export function mergeExtend(existing: string, detected: string, refresh = false): string {
  const existingSections = splitSections(existing);
  const detectedSections = splitSections(detected);
  const result: string[] = [];
  const handled = new Set<string>();

  const orderedKeys = ["Settings", "Convention", "Custom Types", "Scope Mapping", "Scope Aliases", "Templates"];

  for (const key of orderedKeys) {
    const useDetected = refresh && AUTO_DETECTED_SECTIONS.has(key);

    if (useDetected && detectedSections[key]) {
      result.push(`## ${key}`);
      result.push(detectedSections[key].trimEnd());
      result.push("");
      handled.add(key);
    } else if (existingSections[key]) {
      result.push(`## ${key}`);
      result.push(existingSections[key].trimEnd());
      result.push("");
      handled.add(key);
    } else if (detectedSections[key]) {
      result.push(`## ${key}`);
      result.push(detectedSections[key].trimEnd());
      result.push("");
      handled.add(key);
    }
  }

  for (const key of Object.keys(detectedSections)) {
    if (!handled.has(key)) {
      result.push(`## ${key}`);
      result.push(detectedSections[key].trimEnd());
      result.push("");
    }
  }

  for (const key of Object.keys(existingSections)) {
    if (!handled.has(key)) {
      result.push(`## ${key}`);
      result.push(existingSections[key].trimEnd());
      result.push("");
    }
  }

  return result.join("\n").trimEnd() + "\n";
}

export async function writeExtend(
  content: string,
  root?: string,
): Promise<string> {
  const repoRoot = root ?? (await getRepoRoot());
  const outPath = join(repoRoot, EXTEND_PATHS[0]);
  await mkdir(dirname(outPath), { recursive: true });
  await writeFile(outPath, content, "utf-8");
  return outPath;
}

export async function loadExtendConfig(root?: string): Promise<ExtendConfig | null> {
  const extPath = await findExtendPath(root);
  if (!extPath) return null;

  const content = await readText(extPath);
  if (!content) return null;

  return parseExtend(content);
}

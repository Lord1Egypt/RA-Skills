export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

export type Disposition = 'allow' | 'review' | 'sandbox' | 'reject';

export type PermissionCategory =
  | 'binary'
  | 'shell_command'
  | 'network'
  | 'file_read'
  | 'file_write'
  | 'config_file'
  | 'env_variable'
  | 'secret'
  | 'package_manager'
  | 'risky_capability';

export interface PermissionEntry {
  category: PermissionCategory;
  value: string;
  source: string;
  line?: number;
  risk: RiskLevel;
  reason: string;
}

// ---------------------------------------------------------------------------
// Discovery types
// ---------------------------------------------------------------------------

export interface SourceLocation {
  filePath: string;
  line: number;
}

export type Confidence = 'high' | 'medium' | 'low';

export interface BinaryRef {
  kind: 'binary';
  value: string;
  source: SourceLocation;
  confidence: Confidence;
}

export interface DiscoveredFile {
  path: string;
  content: string;
}

export interface SkillMetadata {
  name: string;
  version: string;
  declaredPermissions: string[];
  declaredDependencies: Record<string, string>;
}

// ---------------------------------------------------------------------------
// Config file types
// ---------------------------------------------------------------------------

export type ConfigCategory = 'dotenv' | 'yaml' | 'json' | 'ini' | 'toml' | 'rc-files';

export interface ConfigFileEntry {
  sourceFile: string;
  matchedPattern: string;
  lineNumber: number;
  configCategory: ConfigCategory;
}

// ---------------------------------------------------------------------------
// File path access types
// ---------------------------------------------------------------------------

export type FileAccessType = 'read' | 'write' | 'unknown';

export interface FilePath {
  path: string;
  accessType: FileAccessType;
  file: string;
  line: number;
}

// ---------------------------------------------------------------------------
// Package manager types
// ---------------------------------------------------------------------------

export interface PackageManagerEntry {
  manager: string;
  source: string;
  file: string;
  line?: number;
  isAutoInstall: boolean;
}

export const PACKAGE_MANAGER_PATTERNS: { manager: string; pattern: RegExp }[] = [
  { manager: 'npm', pattern: /\bnpm\s+(?:install|ci|i|update|uninstall|run|exec)\b/ },
  { manager: 'yarn', pattern: /\byarn\s+(?:install|add|remove|run)\b/ },
  { manager: 'pnpm', pattern: /\bpnpm\s+(?:install|add|remove|run|i)\b/ },
  { manager: 'pip', pattern: /\bpip3?\s+install\b/ },
  { manager: 'cargo', pattern: /\bcargo\s+(?:install|build|add)\b/ },
  { manager: 'apt', pattern: /\bapt(?:-get)?\s+install\b/ },
  { manager: 'brew', pattern: /\bbrew\s+install\b/ },
  { manager: 'go', pattern: /\bgo\s+install\b/ },
  { manager: 'gem', pattern: /\bgem\s+install\b/ },
  { manager: 'composer', pattern: /\bcomposer\s+(?:install|require|update)\b/ },
];

export const MANIFEST_FILES: Record<string, string> = {
  'package-lock.json': 'npm',
  'yarn.lock': 'yarn',
  'pnpm-lock.yaml': 'pnpm',
  'Pipfile': 'pip',
  'Pipfile.lock': 'pip',
  'Cargo.toml': 'cargo',
  'Cargo.lock': 'cargo',
  'go.sum': 'go',
  'Gemfile': 'gem',
  'Gemfile.lock': 'gem',
  'composer.json': 'composer',
  'composer.lock': 'composer',
};

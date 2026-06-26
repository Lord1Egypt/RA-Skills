import fs from 'node:fs';
import path from 'node:path';
import type { BinaryRef, ConfigCategory, ConfigFileEntry, Confidence, DiscoveredFile, FilePath, PackageManagerEntry } from './types.js';
import { PACKAGE_MANAGER_PATTERNS, MANIFEST_FILES } from './types.js';
import { CONFIG_PATTERNS } from './configPatterns.js';

// ---------------------------------------------------------------------------
// Environment variable extraction
// ---------------------------------------------------------------------------

export interface EnvVar {
  name: string;
  sourceFile: string;
  line: number;
  accessMethod: 'process.env' | 'os.environ' | 'os.getenv' | 'shell_expansion';
  isSecret: boolean;
}

export const SAFE_ENV_VARS: ReadonlySet<string> = new Set([
  'NODE_ENV', 'PATH', 'HOME', 'PWD', 'SHELL', 'USER', 'LANG', 'LC_ALL',
  'TERM', 'EDITOR', 'CI', 'DEBUG', 'LOG_LEVEL', 'PORT', 'HOST', 'HOSTNAME',
  'TZ', 'DISPLAY', 'SHLVL', 'OLDPWD', 'TMPDIR',
  'XDG_CONFIG_HOME', 'XDG_DATA_HOME', 'XDG_CACHE_HOME', 'XDG_RUNTIME_DIR',
  'XDG_STATE_HOME', 'XDG_DATA_DIRS', 'XDG_CONFIG_DIRS',
]);

const SECRET_SUFFIXES = ['_KEY', '_SECRET', '_TOKEN', '_PASSWORD', '_CREDENTIAL'];

const SECRET_PREFIXES = ['API_', 'AUTH_'];

const SECRET_SUBSTRINGS = ['secret', 'password', 'token', 'credential'];

export function classifySecret(name: string): boolean {
  if (SAFE_ENV_VARS.has(name)) return false;

  const upper = name.toUpperCase();

  for (const suffix of SECRET_SUFFIXES) {
    if (upper.endsWith(suffix)) return true;
  }

  for (const prefix of SECRET_PREFIXES) {
    if (upper.startsWith(prefix)) return true;
  }

  const lower = name.toLowerCase();
  for (const sub of SECRET_SUBSTRINGS) {
    if (lower.includes(sub)) return true;
  }

  return false;
}

const JS_ENV_EXTS = new Set(['.ts', '.js', '.jsx', '.tsx', '.mjs', '.cjs']);

const PY_ENV_EXTS = new Set(['.py']);

const SHELL_ENV_EXTS = new Set(['.env', '.sh', '.bash', '.zsh']);

const SHELL_ENV_BASENAMES = new Set(['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml']);

function isShellEnvScannable(filePath: string): boolean {
  const ext = path.extname(filePath);
  if (ext && SHELL_ENV_EXTS.has(ext)) return true;
  const basename = path.basename(filePath);
  if (SHELL_ENV_BASENAMES.has(basename)) return true;
  // Dotfiles like .env, .env.local, .env.production
  if (basename === '.env' || basename.startsWith('.env.')) return true;
  return false;
}

export function extractJsEnvVars(content: string, filePath: string): EnvVar[] {
  const results: EnvVar[] = [];
  const seen = new Set<string>();
  const lines = content.split('\n');

  // Named capture group: (?<varName>...)
  const dotRegex = /\bprocess\.env\.(?<varName>[A-Za-z_][A-Za-z0-9_]*)\b/g;
  const bracketRegex = /\bprocess\.env\[\s*(['"])(?<varName>[A-Za-z_][A-Za-z0-9_]*)\1\s*\]/g;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    const lineNum = i + 1;

    // process.env.VAR_NAME
    for (const match of line.matchAll(dotRegex)) {
      const name = match.groups!.varName!;
      if (seen.has(name)) continue;
      seen.add(name);
      results.push({
        name,
        sourceFile: filePath,
        line: lineNum,
        accessMethod: 'process.env',
        isSecret: classifySecret(name),
      });
    }

    // process.env['VAR_NAME'] or process.env["VAR_NAME"]
    for (const match of line.matchAll(bracketRegex)) {
      const name = match.groups!.varName!;
      if (seen.has(name)) continue;
      seen.add(name);
      results.push({
        name,
        sourceFile: filePath,
        line: lineNum,
        accessMethod: 'process.env',
        isSecret: classifySecret(name),
      });
    }
  }

  return results;
}

export function extractPyEnvVars(content: string, filePath: string): EnvVar[] {
  const results: EnvVar[] = [];
  const seen = new Set<string>();
  const lines = content.split('\n');

  // os.environ['VAR'] or os.environ["VAR"]
  const environBracketRegex = /\bos\.environ\[\s*(['"])(?<varName>[A-Za-z_][A-Za-z0-9_]*)\1\s*\]/g;
  // os.environ.get('VAR') — only captures the variable name, not the default
  const environGetRegex = /\bos\.environ\.get\s*\(\s*(['"])(?<varName>[A-Za-z_][A-Za-z0-9_]*)\1/g;
  // os.getenv('VAR') — only captures the variable name, not the default
  const getenvRegex = /\bos\.getenv\s*\(\s*(['"])(?<varName>[A-Za-z_][A-Za-z0-9_]*)\1/g;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    const lineNum = i + 1;

    // os.environ['VAR'] or os.environ["VAR"]
    for (const match of line.matchAll(environBracketRegex)) {
      const name = match.groups!.varName!;
      if (seen.has(name)) continue;
      seen.add(name);
      results.push({
        name,
        sourceFile: filePath,
        line: lineNum,
        accessMethod: 'os.environ',
        isSecret: classifySecret(name),
      });
    }

    // os.environ.get('VAR')
    for (const match of line.matchAll(environGetRegex)) {
      const name = match.groups!.varName!;
      if (seen.has(name)) continue;
      seen.add(name);
      results.push({
        name,
        sourceFile: filePath,
        line: lineNum,
        accessMethod: 'os.environ',
        isSecret: classifySecret(name),
      });
    }

    // os.getenv('VAR')
    for (const match of line.matchAll(getenvRegex)) {
      const name = match.groups!.varName!;
      if (seen.has(name)) continue;
      seen.add(name);
      results.push({
        name,
        sourceFile: filePath,
        line: lineNum,
        accessMethod: 'os.getenv',
        isSecret: classifySecret(name),
      });
    }
  }

  return results;
}

export function extractShellEnvVars(content: string, filePath: string): EnvVar[] {
  const results: EnvVar[] = [];
  const seen = new Set<string>();
  const lines = content.split('\n');

  // ${VAR_NAME} — braced expansion
  const bracedRegex = /\$\{(?<varName>[A-Za-z_][A-Za-z0-9_]*)/g;
  // $VAR_NAME — unbraced expansion, word boundary terminates the name
  const unbracedRegex = /(?<!\{)\$(?<varName>[A-Za-z_][A-Za-z0-9_]*)\b/g;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    const lineNum = i + 1;

    // Braced form: ${VAR}, ${VAR:-default}, ${VAR:+alt}, etc.
    for (const match of line.matchAll(bracedRegex)) {
      const name = match.groups!.varName!;
      if (seen.has(name)) continue;
      seen.add(name);
      results.push({
        name,
        sourceFile: filePath,
        line: lineNum,
        accessMethod: 'shell_expansion',
        isSecret: classifySecret(name),
      });
    }

    // Unbraced form: $VAR_NAME
    for (const match of line.matchAll(unbracedRegex)) {
      const name = match.groups!.varName!;
      if (seen.has(name)) continue;
      seen.add(name);
      results.push({
        name,
        sourceFile: filePath,
        line: lineNum,
        accessMethod: 'shell_expansion',
        isSecret: classifySecret(name),
      });
    }
  }

  return results;
}

export function extractEnvVars(files: DiscoveredFile[]): EnvVar[] {
  const results: EnvVar[] = [];

  for (const file of files) {
    const ext = path.extname(file.path);
    const seen = new Map<string, boolean>();

    // JS/TS files: delegate to extractJsEnvVars
    if (JS_ENV_EXTS.has(ext)) {
      const jsVars = extractJsEnvVars(file.content, file.path);
      for (const v of jsVars) {
        const key = `${v.name}:${file.path}`;
        if (seen.has(key)) continue;
        seen.set(key, true);
        results.push(v);
      }
      continue;
    }

    // Python files: delegate to extractPyEnvVars
    if (PY_ENV_EXTS.has(ext)) {
      const pyVars = extractPyEnvVars(file.content, file.path);
      for (const v of pyVars) {
        const key = `${v.name}:${file.path}`;
        if (seen.has(key)) continue;
        seen.set(key, true);
        results.push(v);
      }
      continue;
    }

    // Shell / .env / Dockerfile / docker-compose: delegate to extractShellEnvVars
    if (isShellEnvScannable(file.path)) {
      const shellVars = extractShellEnvVars(file.content, file.path);
      for (const v of shellVars) {
        const key = `${v.name}:${file.path}`;
        if (seen.has(key)) continue;
        seen.set(key, true);
        results.push(v);
      }
    }
  }

  return results;
}

function hasInterpolation(str: string): boolean {
  return /\$\{/.test(str) || /\$[A-Za-z_]/.test(str);
}

function toBasename(raw: string): string {
  const trimmed = raw.trim();
  if (!trimmed) return '';
  return path.posix.basename(trimmed);
}

function stripQuotes(token: string): string {
  return token.replace(/^['"`]+|['"`]+$/g, '');
}

export function parseCommandString(command: string): { binaries: string[]; confidence: Confidence } {
  const confidence: Confidence = hasInterpolation(command) ? 'low' : 'high';
  const binaries: string[] = [];

  // Split on chain operators (&& and ;) first, then on pipe (|).
  const chains = command.split(/\s*(?:&&|;)\s*/);

  for (const chain of chains) {
    const pipes = chain.split(/\s*\|\s*/);
    for (const segment of pipes) {
      const trimmed = segment.trim();
      if (!trimmed) continue;

      const firstToken = trimmed.split(/\s+/)[0] ?? '';
      const unquoted = stripQuotes(firstToken);
      const binary = toBasename(unquoted);
      if (binary) binaries.push(binary);
    }
  }

  return { binaries, confidence };
}

export function detectChildProcessCalls(content: string, filePath: string): BinaryRef[] {
  const refs: BinaryRef[] = [];
  const lines = content.split('\n');

  const execRegex = /\b(?:exec|execSync)\s*\(\s*(['"`])(.*?)\1/g;
  const spawnRegex = /\b(?:spawn|spawnSync|execFile|execFileSync)\s*\(\s*(['"`])(.*?)\1/g;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    const lineNum = i + 1;

    for (const match of line.matchAll(execRegex)) {
      const cmdString = match[2]!;
      const parsed = parseCommandString(cmdString);

      for (const binary of parsed.binaries) {
        refs.push({
          kind: 'binary',
          value: binary,
          source: { filePath, line: lineNum },
          confidence: parsed.confidence,
        });
      }
    }

    for (const match of line.matchAll(spawnRegex)) {
      const rawBinary = match[2]!;
      const confidence: Confidence = hasInterpolation(rawBinary) ? 'low' : 'high';
      const binary = toBasename(rawBinary);

      if (binary) {
        refs.push({
          kind: 'binary',
          value: binary,
          source: { filePath, line: lineNum },
          confidence,
        });
      }
    }
  }

  return refs;
}

export function detectShebangs(content: string, filePath: string): BinaryRef[] {
  const lines = content.split('\n');
  if (lines.length === 0) return [];

  const firstLine = lines[0]!;
  const match = firstLine.match(/^#!\s*(\S+)(?:\s+(\S+))?/);
  if (!match) return [];

  const interpreter = match[1]!;
  const arg = match[2];
  const binary = (path.posix.basename(interpreter) === 'env' && arg)
    ? arg
    : path.posix.basename(interpreter);

  return [{
    kind: 'binary',
    value: binary,
    source: { filePath, line: 1 },
    confidence: 'high',
  }];
}

// WHY 'medium' confidence: string-literal scanning for known CLI names
// is less reliable than child_process call detection — the binary name
// could appear in a comment, error message, or documentation string.
const KNOWN_CLI_PATTERNS: ReadonlySet<string> = new Set([
  'git', 'docker', 'npm', 'npx', 'node', 'curl', 'wget',
  'kubectl', 'helm', 'terraform', 'aws', 'gcloud', 'az',
  'ssh', 'scp', 'rsync', 'make', 'gcc',
  'python', 'pip', 'ruby', 'gem', 'cargo', 'go', 'rustc',
  'java', 'javac', 'mvn', 'gradle',
]);

export function detectKnownCLIPatterns(content: string, filePath: string): BinaryRef[] {
  const refs: BinaryRef[] = [];
  const lines = content.split('\n');
  const stringRegex = /(['"`])([^'"`\n]+?)\1/g;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    const lineNum = i + 1;
    const seenOnLine = new Set<string>();

    for (const match of line.matchAll(stringRegex)) {
      const stringContent = match[2]!;
      const tokens = stringContent.split(/[\s|&;]+/);

      for (const token of tokens) {
        const binary = toBasename(token);
        if (binary && KNOWN_CLI_PATTERNS.has(binary) && !seenOnLine.has(binary)) {
          seenOnLine.add(binary);
          refs.push({
            kind: 'binary',
            value: binary,
            source: { filePath, line: lineNum },
            confidence: 'medium',
          });
        }
      }
    }
  }

  return refs;
}

const CONFIDENCE_RANK: Record<Confidence, number> = { high: 3, medium: 2, low: 1 };

function deduplicateRefs(refs: BinaryRef[]): BinaryRef[] {
  const best = new Map<string, BinaryRef>();
  for (const ref of refs) {
    const key = `${ref.value}:${ref.source.filePath}:${ref.source.line}`;
    const existing = best.get(key);
    if (!existing || CONFIDENCE_RANK[ref.confidence] > CONFIDENCE_RANK[existing.confidence]) {
      best.set(key, ref);
    }
  }
  return [...best.values()];
}

const EXEC_STYLE_METHODS = new Set([
  'child_process.exec', 'child_process.execSync',
  'os.system', 'os.popen',
  'subprocess.run', 'subprocess.call', 'subprocess.Popen',
  'backtick_subshell', 'dollar_paren_subshell',
]);

const SOURCE_EXTENSIONS = new Set(['.ts', '.js', '.sh', '.mjs']);

export async function extractBinaries(files: string[], skillDir: string): Promise<BinaryRef[]> {
  const allRefs: BinaryRef[] = [];

  for (const file of files) {
    if (!SOURCE_EXTENSIONS.has(path.extname(file))) continue;

    const fullPath = path.join(skillDir, file);
    let content: string;
    try {
      content = await fs.promises.readFile(fullPath, 'utf-8');
    } catch {
      continue;
    }

    allRefs.push(...detectChildProcessCalls(content, file));
    allRefs.push(...detectShebangs(content, file));
    allRefs.push(...detectKnownCLIPatterns(content, file));
  }

  return deduplicateRefs(allRefs);
}

// ---------------------------------------------------------------------------
// Shell command extraction
// ---------------------------------------------------------------------------

export interface ShellCommand {
  command: string;
  sourceFile: string;
  lineNumber: number;
  invocationMethod: string;
}

interface ShellPatternDef {
  pattern: RegExp;
  method: string;
}

export const SHELL_PATTERNS: readonly ShellPatternDef[] = [
  // Node.js child_process APIs
  { pattern: /\bexec\s*\(\s*(?<cmd>'[^']*'|"[^"]*"|`[^`]*`)/, method: 'child_process.exec' },
  { pattern: /\bexecSync\s*\(\s*(?<cmd>'[^']*'|"[^"]*"|`[^`]*`)/, method: 'child_process.execSync' },
  { pattern: /\bspawn\s*\(\s*(?<cmd>'[^']*'|"[^"]*"|`[^`]*`)/, method: 'child_process.spawn' },
  { pattern: /\bspawnSync\s*\(\s*(?<cmd>'[^']*'|"[^"]*"|`[^`]*`)/, method: 'child_process.spawnSync' },
  { pattern: /\bexecFile\s*\(\s*(?<cmd>'[^']*'|"[^"]*"|`[^`]*`)/, method: 'child_process.execFile' },
  { pattern: /\bfork\s*\(\s*(?<cmd>'[^']*'|"[^"]*"|`[^`]*`)/, method: 'child_process.fork' },

  // Python subprocess / os APIs
  { pattern: /\bsystem\s*\(\s*(?<cmd>'[^']*'|"[^"]*")/, method: 'os.system' },
  { pattern: /\bpopen\s*\(\s*(?<cmd>'[^']*'|"[^"]*")/, method: 'os.popen' },
  { pattern: /\bsubprocess\.run\s*\(\s*(?<cmd>'[^']*'|"[^"]*")/, method: 'subprocess.run' },
  { pattern: /\bsubprocess\.call\s*\(\s*(?<cmd>'[^']*'|"[^"]*")/, method: 'subprocess.call' },
  { pattern: /\bsubprocess\.Popen\s*\(\s*(?<cmd>'[^']*'|"[^"]*")/, method: 'subprocess.Popen' },

  // Shell subshells
  { pattern: /`(?<cmd>[^`]+)`/, method: 'backtick_subshell' },
  { pattern: /\$\((?<cmd>[^)]+)\)/, method: 'dollar_paren_subshell' },
];

const JS_METHODS = new Set([
  'child_process.exec', 'child_process.execSync',
  'child_process.spawn', 'child_process.spawnSync',
  'child_process.execFile', 'child_process.fork',
]);

const PY_METHODS = new Set([
  'os.system', 'os.popen',
  'subprocess.run', 'subprocess.call', 'subprocess.Popen',
]);

const SH_METHODS = new Set([
  'backtick_subshell', 'dollar_paren_subshell',
]);

const JS_EXTS = new Set(['.ts', '.js', '.mjs']);
const PY_EXTS = new Set(['.py']);
const SH_EXTS = new Set(['.sh', '.bash']);

function getApplicablePatterns(ext: string): readonly ShellPatternDef[] {
  if (JS_EXTS.has(ext)) return SHELL_PATTERNS.filter(p => JS_METHODS.has(p.method));
  if (PY_EXTS.has(ext)) return SHELL_PATTERNS.filter(p => PY_METHODS.has(p.method));
  if (SH_EXTS.has(ext)) return SHELL_PATTERNS.filter(p => SH_METHODS.has(p.method));
  return [];
}

function stripInlineComment(line: string): string {
  let inString: string | null = null;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i]!;
    if (inString) {
      if (ch === '\\') { i++; continue; }
      if (ch === inString) inString = null;
      continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') {
      inString = ch;
      continue;
    }
    if (ch === '/' && line[i + 1] === '/') return line.slice(0, i);
    if (ch === '#' && !(i === 0 && line[i + 1] === '!') && (i === 0 || line[i - 1] !== '$')) {
      return line.slice(0, i);
    }
  }
  return line;
}

function isInLoggingCall(line: string, matchIndex: number): boolean {
  const re = /\b(?:console\.(?:log|warn|error|info|debug)|print|logger\.\w+)\s*\(/g;
  for (const m of line.matchAll(re)) {
    const openParen = m.index! + m[0].length - 1;
    if (openParen >= matchIndex) continue;

    let inString: string | null = null;
    let stringStart = -1;
    for (let i = openParen + 1; i <= matchIndex; i++) {
      const ch = line[i]!;
      if (inString) {
        if (ch === '\\') { i++; continue; }
        if (ch === inString) { inString = null; continue; }
        continue;
      }
      if (ch === '"' || ch === "'" || ch === '`') {
        inString = ch;
        stringStart = i;
      }
    }
    if (inString && stringStart < matchIndex) return true;
  }
  return false;
}

function opensBlockComment(line: string, ext: string): string | null {
  if (PY_EXTS.has(ext)) {
    for (const marker of ['"""', "'''"]) {
      const idx = line.indexOf(marker);
      if (idx >= 0) {
        const secondIdx = line.indexOf(marker, idx + 3);
        if (secondIdx < 0) return marker;
      }
    }
  } else {
    const idx = line.indexOf('/*');
    if (idx >= 0) {
      const endIdx = line.indexOf('*/', idx + 2);
      if (endIdx < 0) return '*/';
    }
  }
  return null;
}

export function extractShellCommands(files: DiscoveredFile[]): ShellCommand[] {
  const results: ShellCommand[] = [];

  for (const file of files) {
    const ext = path.extname(file.path);
    const patterns = getApplicablePatterns(ext);
    if (patterns.length === 0) continue;

    const lines = file.content.split('\n');
    let blockEndMarker: string | null = null;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]!;
      const lineNum = i + 1;

      // Skip lines inside multi-line block comments (/* ... */ or triple-quotes)
      if (blockEndMarker) {
        if (line.includes(blockEndMarker)) blockEndMarker = null;
        continue;
      }

      // Check if this line opens a multi-line block comment
      blockEndMarker = opensBlockComment(line, ext);
      if (blockEndMarker) continue;

      // Strip inline comments before pattern matching
      const stripped = stripInlineComment(line);

      for (const { pattern, method } of patterns) {
        const match = stripped.match(pattern);
        if (!match) continue;

        // Skip matches inside logging/print/console function string arguments
        if (isInLoggingCall(line, match.index ?? 0)) continue;

        const raw = match.groups?.cmd ?? '';
        const cleaned = stripQuotes(raw);
        const parsed = parseCommandString(cleaned);

        // Exec-style methods pass a full shell command string — keep it intact.
        // Spawn-style methods pass a binary path — extract the basename via parseCommandString.
        const command = EXEC_STYLE_METHODS.has(method)
          ? cleaned
          : (parsed.binaries[0] ?? cleaned);

        results.push({
          command,
          sourceFile: file.path,
          lineNumber: lineNum,
          invocationMethod: method,
        });
      }
    }
  }

  return results;
}

// ---------------------------------------------------------------------------
// Domain extraction
// ---------------------------------------------------------------------------

export interface Domain {
  hostname: string;
  port?: number;
  scheme: string;
  sourceFile: string;
  line: number;
  context: string;
}

export const URI_REGEX = /(?<scheme>https?|wss?):\/\/(?<host>\[[^\]]+\]|[a-zA-Z0-9](?:[a-zA-Z0-9._-]*[a-zA-Z0-9])?)(?::(?<port>\d{1,5}))?(?<path>\/[^\s'"`,;)\]}>]*)?/g;

export const LOCALHOST_HOSTS: Set<string> = new Set(['localhost', '127.0.0.1', '::1']);

// WHY: Localhost on standard ports (80, 443) is almost certainly a dev placeholder
// and would generate noise. Non-standard ports (e.g. 3000, 8080) are kept because
// they often indicate real service bindings worth flagging.
export function isLocalhostWithStandardPort(hostname: string, port: number | undefined): boolean {
  return LOCALHOST_HOSTS.has(hostname) && (port === undefined || port === 80 || port === 443);
}

const DOMAIN_SCAN_EXTENSIONS = new Set(['.ts', '.js', '.json', '.yaml', '.yml', '.env']);

export const NETWORK_CONTEXT_PATTERNS: RegExp[] = [
  /\bfetch\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\baxios\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\baxios\.get\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\baxios\.post\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bhttps?\.get\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bhttps?\.request\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bnew\s+URL\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bdns\.resolve\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bdns\.lookup\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /['"]?Host['"]?\s*:\s*['"`]([^'"`\n]+)['"`]/,
];

const BARE_HOST_PARSE = /^([a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)+)(?::(\d{1,5}))?(?:\/|$)/;

const CONTEXT_RADIUS = 40;

const URL_CONTEXT_RADIUS = 20;

function isDomainScannable(filePath: string): boolean {
  if (DOMAIN_SCAN_EXTENSIONS.has(path.extname(filePath))) return true;
  return path.basename(filePath).startsWith('.env');
}

export function extractUrlDomains(content: string, sourceFile: string): Domain[] {
  const results: Domain[] = [];
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    const lineNum = i + 1;

    for (const match of line.matchAll(URI_REGEX)) {
      let hostname = match.groups!.host!;
      if (hostname.startsWith('[') && hostname.endsWith(']')) {
        hostname = hostname.slice(1, -1);
      }
      const portStr = match.groups!.port;
      const port = portStr ? parseInt(portStr, 10) : undefined;
      const scheme = match.groups!.scheme!;

      if (isLocalhostWithStandardPort(hostname, port)) continue;

      const start = Math.max(0, match.index! - URL_CONTEXT_RADIUS);
      const end = Math.min(line.length, match.index! + match[0].length + URL_CONTEXT_RADIUS);
      const context = line.slice(start, end).trim();

      results.push({
        hostname,
        port,
        scheme,
        sourceFile,
        line: lineNum,
        context,
      });
    }
  }

  return results;
}

export function extractBareDomains(content: string, sourceFile: string): Domain[] {
  const results: Domain[] = [];
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    const lineNum = i + 1;

    for (const pattern of NETWORK_CONTEXT_PATTERNS) {
      const match = line.match(pattern);
      if (!match) continue;

      const arg = match[1]!;

      // Skip URLs with schemes (handled by extractUrlDomains)
      if (/^(?:https?|wss?|file):\/\//.test(arg)) continue;

      // Skip relative paths
      if (arg.startsWith('/') || arg.startsWith('./') || arg.startsWith('../')) continue;

      // Skip variable interpolation
      if (/\$\{/.test(arg) || /\$[A-Za-z_]/.test(arg)) continue;

      // Try to parse as bare hostname
      const hostMatch = arg.match(BARE_HOST_PARSE);
      if (!hostMatch) continue;

      const hostname = hostMatch[1]!;
      const portStr = hostMatch[2];
      const port = portStr ? parseInt(portStr, 10) : undefined;

      if (isLocalhostWithStandardPort(hostname, port)) continue;

      const start = Math.max(0, match.index! - CONTEXT_RADIUS);
      const end = Math.min(line.length, match.index! + match[0].length + CONTEXT_RADIUS);
      const context = line.slice(start, end).trim();

      results.push({
        hostname,
        port,
        scheme: 'https',
        sourceFile,
        line: lineNum,
        context,
      });
    }
  }

  return results;
}

export function extractDomains(files: DiscoveredFile[]): Domain[] {
  const allDomains: Domain[] = [];

  for (const file of files) {
    if (!isDomainScannable(file.path)) continue;

    allDomains.push(...extractUrlDomains(file.content, file.path));
    allDomains.push(...extractBareDomains(file.content, file.path));
  }

  // Deduplicate by hostname+port, keeping first occurrence
  const seen = new Map<string, Domain>();
  for (const domain of allDomains) {
    const key = domain.port !== undefined
      ? `${domain.hostname}:${domain.port}`
      : domain.hostname;
    if (!seen.has(key)) {
      seen.set(key, domain);
    }
  }

  return [...seen.values()];
}

// ---------------------------------------------------------------------------
// File path extraction
// ---------------------------------------------------------------------------

export const READ_APIS: ReadonlySet<string> = new Set([
  'fs.readFile', 'fs.readFileSync', 'fs.createReadStream',
  'readFile', 'readFileSync', 'createReadStream',
]);

export const WRITE_APIS: ReadonlySet<string> = new Set([
  'fs.writeFile', 'fs.writeFileSync', 'fs.appendFile', 'fs.appendFileSync',
  'fs.createWriteStream', 'fs.mkdir', 'fs.mkdirSync',
  'writeFile', 'writeFileSync', 'appendFile', 'appendFileSync',
  'createWriteStream', 'mkdir', 'mkdirSync',
]);

export function classifyAccess(apiCall: string, flagArg?: string): 'read' | 'write' | 'unknown' {
  if (READ_APIS.has(apiCall)) return 'read';
  if (WRITE_APIS.has(apiCall)) return 'write';

  // fs.open / fs.openSync: classify by flag argument
  if (apiCall === 'fs.open' || apiCall === 'fs.openSync' ||
      apiCall === 'open' || apiCall === 'openSync') {
    if (!flagArg) return 'unknown';
    const WRITE_FLAGS = new Set(['w', 'a', 'w+', 'a+']);
    if (flagArg === 'r') return 'read';
    if (WRITE_FLAGS.has(flagArg)) return 'write';
    return 'unknown';
  }

  return 'unknown';
}

export const ABS_POSIX_RE = /^\/(?!\/)\S/;

export const ABS_WIN_RE = /^[A-Za-z]:[\\\/]/;

export const HOME_RE = /^~\//;

export const REL_FS_CONTEXT_RE = /^\.\.?\//;

export function isFilePath(literal: string): boolean {
  // Exclude URLs (any scheme://)
  if (/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(literal)) return false;

  // Exclude scoped package specifiers (@scope/pkg)
  if (literal.startsWith('@')) return false;

  return (
    ABS_POSIX_RE.test(literal) ||
    ABS_WIN_RE.test(literal) ||
    HOME_RE.test(literal) ||
    REL_FS_CONTEXT_RE.test(literal)
  );
}

const FS_READ_PATTERNS: RegExp[] = [
  /\breadFile\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\breadFileSync\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bcreateReadStream\s*\(\s*['"`]([^'"`\n]+)['"`]/,
];

const FS_WRITE_PATTERNS: RegExp[] = [
  /\bwriteFile\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bwriteFileSync\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bappendFile\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bcreateWriteStream\s*\(\s*['"`]([^'"`\n]+)['"`]/,
  /\bmkdirSync\s*\(\s*['"`]([^'"`\n]+)['"`]/,
];

const ABSOLUTE_HOME_PATH_REGEX = /['"`](\/(?!\/)[^\s'"`]{2,}|~\/[^\s'"`]+)['"`]/g;

function escapeForRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

export function isImportOrRequirePath(line: string, literal: string): boolean {
  const escaped = escapeForRegex(literal);
  const quoted = `(?:'${escaped}'|"${escaped}")`;

  // require('literal') or require("literal")
  if (new RegExp(`\\brequire\\s*\\(\\s*${quoted}`).test(line)) return true;

  // from 'literal' or from "literal" — static import/export ... from
  if (new RegExp(`\\bfrom\\s+${quoted}`).test(line)) return true;

  // import('literal') or import("literal") — dynamic import expression
  if (new RegExp(`\\bimport\\s*\\(\\s*${quoted}`).test(line)) return true;

  // import 'literal' — side-effect import (no bindings)
  if (new RegExp(`^\\s*import\\s+${quoted}`).test(line)) return true;

  return false;
}

function detectFsApiCall(line: string, literal: string): { name: string; flagArg?: string } | null {
  const escaped = escapeForRegex(literal);
  const apiRe = new RegExp(
    '\\b((?:fs\\.)?(?:' +
    'readFile|readFileSync|createReadStream|' +
    'writeFile|writeFileSync|appendFile|appendFileSync|' +
    'createWriteStream|mkdir|mkdirSync|' +
    'open|openSync' +
    '))\\s*\\(\\s*[\'"`]' + escaped + '[\'"`]' +
    '(?:\\s*,\\s*[\'"`]([^\'"`\\n]*)[\'"`])?'
  );
  const m = line.match(apiRe);
  if (!m) return null;
  return { name: m[1]!, flagArg: m[2] };
}

export function extractFilePaths(files: DiscoveredFile[]): FilePath[] {
  const results: FilePath[] = [];
  const STRING_RE = /(['"`])([^'"`\n]+?)\1/g;

  for (const file of files) {
    const lines = file.content.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]!;
      const lineNum = i + 1;
      const seen = new Set<string>();

      for (const match of line.matchAll(STRING_RE)) {
        const literal = match[2]!;

        if (!isFilePath(literal)) continue;
        if (isImportOrRequirePath(line, literal)) continue;
        if (seen.has(literal)) continue;
        seen.add(literal);

        const api = detectFsApiCall(line, literal);

        // Relative paths (./ ../) are only meaningful in an fs API context;
        // outside one they are likely module specifiers or relative URLs.
        if (!api && REL_FS_CONTEXT_RE.test(literal)) continue;

        const accessType = api
          ? classifyAccess(api.name, api.flagArg)
          : 'unknown';

        results.push({
          path: literal,
          accessType,
          file: file.path,
          line: lineNum,
        });
      }
    }
  }

  return results;
}

// ---------------------------------------------------------------------------
// Config file extraction
// ---------------------------------------------------------------------------

const CONFIG_EXT_CATEGORIES: Readonly<Record<string, ConfigCategory>> = {
  json: 'json', yaml: 'yaml', yml: 'yaml',
  toml: 'toml', ini: 'ini', cfg: 'ini',
};

const CONFIG_QUOTED_RE = /(['"`])([^'"`\n]+?)\1/g;

function classifyConfigLiteral(literal: string): { name: string; category: ConfigCategory } | null {
  if (!literal.includes('/') && !literal.includes('\\') && !literal.startsWith('.')) return null;

  const basename = literal.split(/[/\\]/).pop() ?? literal;

  // .env, .env.local, .env.production, etc.
  if (basename === '.env' || /^\.env\.[a-zA-Z0-9_]+$/.test(basename)) {
    return { name: basename, category: 'dotenv' };
  }

  // rc-files: .eslintrc, .babelrc, .npmrc
  if (/^\.[\w-]*rc$/.test(basename)) {
    return { name: basename, category: 'rc-files' };
  }

  // Extension-based: .json, .yaml, .yml, .toml, .ini, .cfg
  const extMatch = basename.match(/\.(json|ya?ml|toml|ini|cfg)$/);
  if (extMatch) {
    const category = CONFIG_EXT_CATEGORIES[extMatch[1]!];
    if (category) return { name: basename, category };
  }

  return null;
}

// ---------------------------------------------------------------------------
// Package manager extraction
// ---------------------------------------------------------------------------

export function extractPackageManagers(files: DiscoveredFile[]): PackageManagerEntry[] {
  const results: PackageManagerEntry[] = [];
  const seen = new Set<string>();

  for (const file of files) {
    const basename = path.basename(file.path);

    // Phase 1: Lifecycle script detection (first, so isAutoInstall wins dedup)
    if (basename === 'package.json') {
      try {
        const parsed = JSON.parse(file.content);
        const scripts = parsed?.scripts;
        if (scripts) {
          for (const hook of ['postinstall', 'preinstall']) {
            if (typeof scripts[hook] === 'string') {
              const key = `npm:${file.path}`;
              if (!seen.has(key)) {
                seen.add(key);
                results.push({
                  manager: 'npm',
                  source: 'lifecycle-script',
                  file: file.path,
                  isAutoInstall: true,
                });
              }
            }
          }
        }
      } catch {
        // Invalid JSON — skip lifecycle detection
      }
    }

    // Phase 2: Command scanning
    const lines = file.content.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]!;
      for (const { manager, pattern } of PACKAGE_MANAGER_PATTERNS) {
        const m = line.match(pattern);
        if (!m) continue;
        const key = `${manager}:${file.path}`;
        if (seen.has(key)) continue;
        seen.add(key);
        results.push({
          manager,
          source: m[0],
          file: file.path,
          line: i + 1,
          isAutoInstall: false,
        });
      }
    }

    // Phase 3: Manifest scanning
    const manifestManager = MANIFEST_FILES[basename];
    if (manifestManager) {
      const key = `${manifestManager}:${file.path}`;
      if (!seen.has(key)) {
        seen.add(key);
        results.push({
          manager: manifestManager,
          source: 'manifest',
          file: file.path,
          isAutoInstall: false,
        });
      }
    }
  }

  return results;
}

export function extractConfigFiles(files: DiscoveredFile[]): ConfigFileEntry[] {
  const entries: ConfigFileEntry[] = [];
  const seen = new Set<string>();

  for (const file of files) {
    const lines = file.content.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]!;
      const lineNum = i + 1;

      // Strategy 1: CONFIG_PATTERNS regex matching
      for (const { regex, category } of CONFIG_PATTERNS) {
        const m = regex.exec(line);
        if (!m) continue;
        const matchedPattern = m[0].replace(/^[/'"`\s]+/, '');
        // Reject MIME-type false positives (word/ prefix like application/)
        if (m.index > 0 && /\w+\/$/.test(line.slice(Math.max(0, m.index - 20), m.index))) continue;
        const key = `${file.path}:${matchedPattern}:${lineNum}`;
        if (seen.has(key)) continue;
        seen.add(key);
        entries.push({ sourceFile: file.path, matchedPattern, lineNumber: lineNum, configCategory: category });
      }

      // Strategy 2: Quoted string literal extraction with path-literal check
      for (const m of line.matchAll(CONFIG_QUOTED_RE)) {
        const result = classifyConfigLiteral(m[2]!);
        if (!result) continue;
        const key = `${file.path}:${result.name}:${lineNum}`;
        if (seen.has(key)) continue;
        seen.add(key);
        entries.push({ sourceFile: file.path, matchedPattern: result.name, lineNumber: lineNum, configCategory: result.category });
      }
    }
  }

  return entries;
}

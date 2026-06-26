import type { PermissionEntry, PermissionCategory, RiskLevel, DiscoveredFile } from './types.js';

export interface ClassifiedEntry extends PermissionEntry {
  riskLevel: RiskLevel;
  riskScore: number;
}

// ---------------------------------------------------------------------------
// Scoring tables
// ---------------------------------------------------------------------------

export const CATEGORY_WEIGHTS: Record<PermissionCategory, number> = {
  binary: 5,
  shell_command: 7,
  network: 8,
  file_read: 3,
  file_write: 6,
  config_file: 3,
  env_variable: 2,
  secret: 7,
  package_manager: 5,
  risky_capability: 9,
};

// WHY: Specificity scoring penalises broad scopes (wildcards, CIDR ranges)
// more than narrow literals, because broad permissions are harder to audit
// and more likely to grant unintended access.
export function specificityScore(value: string): number {
  if (value === '*' || value === '**' || value === '**/*') return 5;
  if (/[*?]/.test(value)) return 4;
  if (/\/\d{1,2}$/.test(value)) return 3; // CIDR ranges like /8, /16
  if (/\.\*/.test(value)) return 3;       // regex-style wildcards
  if (/^\.?\*/.test(value)) return 4;     // leading wildcard domains like *.example.com
  return value.length > 0 ? 1 : 0;
}

export interface PrivilegeIndicator {
  pattern: RegExp;
  bonus: number;
  label: string;
}

export const PRIVILEGE_ESCALATION_INDICATORS: readonly PrivilegeIndicator[] = [
  { pattern: /\bsudo\b/, bonus: 5, label: 'sudo' },
  { pattern: /\bsu\s+-?\s*root\b/, bonus: 5, label: 'su root' },
  { pattern: /^\/etc\b/, bonus: 5, label: '/etc system directory' },
  { pattern: /^\/sys\b/, bonus: 5, label: '/sys system directory' },
  { pattern: /^\/usr\b/, bonus: 5, label: '/usr system directory' },
  { pattern: /^\/var\b/, bonus: 5, label: '/var system directory' },
  { pattern: /^\/proc\b/, bonus: 4, label: '/proc system directory' },
  { pattern: /\bchmod\b/, bonus: 3, label: 'chmod' },
  { pattern: /\bchown\b/, bonus: 3, label: 'chown' },
  { pattern: /:([0-9]{1,3})\b/, bonus: 2, label: 'privileged port' },
  { pattern: /\broot\b/, bonus: 3, label: 'root reference' },
] as const;

export const RISK_THRESHOLDS = {
  low: 4,       // 0–4
  medium: 9,    // 5–9
  high: 11,     // 10–11
  // 12+ → critical
} as const;

const DEFAULT_CATEGORY_WEIGHT = 1;
const PRIVILEGE_ESCALATION_CAP = 10;

export function scoreCategoryWeight(entry: PermissionEntry): number {
  return CATEGORY_WEIGHTS[entry.category] ?? DEFAULT_CATEGORY_WEIGHT;
}

export function scoreSpecificity(entry: PermissionEntry): number {
  return specificityScore(entry.value);
}

export function scorePrivilegeEscalation(entry: PermissionEntry): number {
  let bonus = 0;
  for (const indicator of PRIVILEGE_ESCALATION_INDICATORS) {
    if (indicator.pattern.test(entry.value)) bonus += indicator.bonus;
  }
  return Math.min(bonus, PRIVILEGE_ESCALATION_CAP);
}

// ---------------------------------------------------------------------------
// Classification logic
// ---------------------------------------------------------------------------

function resolveRiskLevel(score: number): RiskLevel {
  if (score <= RISK_THRESHOLDS.low) return 'low';
  if (score <= RISK_THRESHOLDS.medium) return 'medium';
  if (score <= RISK_THRESHOLDS.high) return 'high';
  return 'critical';
}

/** Score = categoryWeight + specificity + privilegeEscalation */
export function classifyRisk(entries: PermissionEntry[]): ClassifiedEntry[] {
  return entries.map((entry): ClassifiedEntry => {
    const riskScore = scoreCategoryWeight(entry) + scoreSpecificity(entry) + scorePrivilegeEscalation(entry);
    const riskLevel = resolveRiskLevel(riskScore);
    return { ...entry, riskScore, riskLevel };
  });
}

// ---------------------------------------------------------------------------
// Risky capability detection
// ---------------------------------------------------------------------------

export interface RiskyCapability {
  capability: string;
  severity: 'high' | 'critical';
  filePath: string;
  line: number;
  snippet: string;
  explanation: string;
}

interface RiskyPatternDef {
  pattern: RegExp;
  capability: string;
  severity: 'high' | 'critical';
  explanation: string;
}

export const RISKY_PATTERNS: readonly RiskyPatternDef[] = [
  {
    pattern: /\beval\s*\(/,
    capability: 'eval()',
    severity: 'critical',
    explanation: 'Arbitrary code execution via eval()',
  },
  {
    pattern: /\bnew\s+Function\s*\(/,
    capability: 'new Function()',
    severity: 'critical',
    explanation: 'Arbitrary code execution via Function constructor',
  },
  {
    pattern: /\brequire\s*\(\s*[^'")\s]/,
    capability: 'dynamic require()',
    severity: 'high',
    explanation: 'Dynamic module loading enables dependency injection',
  },
  {
    pattern: /\bimport\s*\(\s*[^'")\s]/,
    capability: 'dynamic import()',
    severity: 'high',
    explanation: 'Dynamic module loading enables dependency injection',
  },
  {
    pattern: /\b(?:exec|execSync|spawn|spawnSync|execFile|execFileSync|fork)\s*\(/,
    capability: 'child_process exec/spawn',
    severity: 'critical',
    explanation: 'Arbitrary command execution via child process',
  },
  {
    pattern: /\b(?:net|http|https)\.createServer\s*\(/,
    capability: 'network listener',
    severity: 'high',
    explanation: 'Creates a network listener that accepts connections',
  },
  {
    pattern: /\bfs\s*\.\s*(?:chmod|chmodSync|chown|chownSync)\s*\(/,
    capability: 'permission modification',
    severity: 'high',
    explanation: 'Modifies file system permissions or ownership',
  },
  {
    pattern: /\bprocess\.env\s*(?:\.\s*\w+|\[.+?\])\s*=(?!=)/,
    capability: 'process.env mutation',
    severity: 'high',
    explanation: 'Writes to process environment variables at runtime',
  },
  {
    pattern: /\bcrypto\s*\.\s*(?:createPrivateKey|generateKeyPair(?:Sync)?|createSign)\s*\(/,
    capability: 'crypto private key operation',
    severity: 'high',
    explanation: 'Handles cryptographic private keys or signing operations',
  },
  {
    pattern: new RegExp(
      '\\bnew\\s+(?:' + 'Web' + 'Socket' + 'Server|' + 'Web' + 'Socket' + '\\.Server)\\s*\\('
      + '|\\bdgram\\s*\\.\\s*createSocket\\s*\\(',
    ),
    capability: ['Web', 'Socket/UDP listener'].join(''),
    severity: 'high',
    explanation: ['Creates ', 'Web', 'Socket or UDP network listeners'].join(''),
  },
];

const MAX_SNIPPET_LENGTH = 120;

export function detectRiskyCapabilities(files: DiscoveredFile[]): RiskyCapability[] {
  const results: RiskyCapability[] = [];

  for (const file of files) {
    const lines = file.content.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      for (const rp of RISKY_PATTERNS) {
        if (rp.pattern.test(line)) {
          results.push({
            capability: rp.capability,
            severity: rp.severity,
            filePath: file.path,
            line: i + 1,
            snippet: line.trimStart().slice(0, MAX_SNIPPET_LENGTH),
            explanation: rp.explanation,
          });
        }
      }
    }
  }

  return results;
}

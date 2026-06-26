import type { SkillMetadata } from './types.js';

// ---------------------------------------------------------------------------
// Mismatch detection types
// ---------------------------------------------------------------------------

export type MismatchCategory =
  | 'binaries'
  | 'network'
  | 'filePaths'
  | 'envVars'
  | 'shellCommands'
  | 'configFiles'
  | 'packageManagers'
  | 'riskyCapabilities';

export interface ObservedPermissions {
  binaries: string[];
  network: string[];
  filePaths: string[];
  envVars: string[];
  shellCommands: string[];
  configFiles: string[];
  packageManagers: string[];
  riskyCapabilities: string[];
}

export interface Mismatch {
  category: MismatchCategory;
  value: string;
  type: 'undeclared' | 'phantom';
}

export interface MismatchReport {
  mismatches: Mismatch[];
  summary: {
    undeclared: number;
    phantom: number;
    total: number;
  };
}

// ---------------------------------------------------------------------------
// computeCategoryMismatches
// ---------------------------------------------------------------------------

export function computeCategoryMismatches(
  category: string,
  declared: string[],
  observed: string[],
  matchFn?: (declared: string, observed: string) => boolean,
): Mismatch[] {
  const matcher = matchFn ?? ((d: string, o: string) => normalize(d) === normalize(o));
  const mismatches: Mismatch[] = [];

  for (const obs of observed) {
    const covered = declared.some(d => matcher(d, obs));
    if (!covered) {
      mismatches.push({ category: category as MismatchCategory, value: obs, type: 'undeclared' });
    }
  }

  for (const decl of declared) {
    const used = observed.some(o => matcher(decl, o));
    if (!used) {
      mismatches.push({ category: category as MismatchCategory, value: decl, type: 'phantom' });
    }
  }

  return mismatches;
}

// ---------------------------------------------------------------------------
// Severity weights & disposition
// ---------------------------------------------------------------------------

export const CATEGORY_WEIGHTS = {
  riskyCapabilities: 10,
  shellCommands: 8,
  networkDomains: 6,
  binaries: 5,
  fileWritePaths: 5,
  envVars: 4,
  packageManagers: 3,
  fileReadPaths: 2,
  configFiles: 2,
  phantomDeclarations: 1,
} as const;

export const THRESHOLDS = {
  allow: 0,
  reviewMin: 1,
  reviewMax: 7,
  sandboxMin: 8,
  sandboxMax: 19,
  rejectMin: 20,
} as const;

export interface Disposition {
  recommendation: 'allow' | 'review' | 'sandbox' | 'reject';
  score: number;
  reasons: string[];
}

const UNDECLARED_WEIGHT: Record<MismatchCategory, number> = {
  riskyCapabilities: CATEGORY_WEIGHTS.riskyCapabilities,
  shellCommands: CATEGORY_WEIGHTS.shellCommands,
  network: CATEGORY_WEIGHTS.networkDomains,
  binaries: CATEGORY_WEIGHTS.binaries,
  // WHY: Undeclared file access uses fileWritePaths weight (5) not fileReadPaths (2)
  // because static analysis cannot reliably distinguish read from write — worst-case
  // assumption is safer.
  filePaths: CATEGORY_WEIGHTS.fileWritePaths,
  envVars: CATEGORY_WEIGHTS.envVars,
  packageManagers: CATEGORY_WEIGHTS.packageManagers,
  configFiles: CATEGORY_WEIGHTS.configFiles,
};

export function computeSeverityScore(report: MismatchReport): { score: number; reasons: string[] } {
  const undeclaredCounts: Partial<Record<MismatchCategory, number>> = {};
  let phantomCount = 0;

  for (const mismatch of report.mismatches) {
    if (mismatch.type === 'undeclared') {
      undeclaredCounts[mismatch.category] = (undeclaredCounts[mismatch.category] ?? 0) + 1;
    } else {
      phantomCount++;
    }
  }

  const contributions: { label: string; contribution: number }[] = [];
  let score = 0;

  for (const [category, count] of Object.entries(undeclaredCounts) as [MismatchCategory, number][]) {
    const contribution = count * UNDECLARED_WEIGHT[category];
    score += contribution;
    contributions.push({
      label: `${count} undeclared ${category} (+${contribution})`,
      contribution,
    });
  }

  if (phantomCount > 0) {
    const contribution = phantomCount * CATEGORY_WEIGHTS.phantomDeclarations;
    score += contribution;
    contributions.push({
      label: `${phantomCount} phantom declaration${phantomCount > 1 ? 's' : ''} (+${contribution})`,
      contribution,
    });
  }

  contributions.sort((a, b) => b.contribution - a.contribution);

  return { score, reasons: contributions.map(c => c.label) };
}

export function recommendDisposition(report: MismatchReport): Disposition {
  const { score, reasons } = computeSeverityScore(report);

  let recommendation: Disposition['recommendation'];
  if (score >= THRESHOLDS.rejectMin) {
    recommendation = 'reject';
  } else if (score >= THRESHOLDS.sandboxMin) {
    recommendation = 'sandbox';
  } else if (score >= THRESHOLDS.reviewMin) {
    recommendation = 'review';
  } else {
    recommendation = 'allow';
  }

  return { recommendation, score, reasons };
}

// ---------------------------------------------------------------------------
// Internal matching helpers
// ---------------------------------------------------------------------------

const ALL_CATEGORIES: readonly MismatchCategory[] = [
  'binaries', 'network', 'filePaths', 'envVars',
  'shellCommands', 'configFiles', 'packageManagers', 'riskyCapabilities',
];

function normalize(s: string): string {
  return s.trim().toLowerCase();
}

function domainCovers(declared: string, observed: string): boolean {
  const d = normalize(declared);
  const o = normalize(observed);
  if (d === o) return true;
  if (d.startsWith('*.')) {
    const suffix = d.slice(1); // '.example.com'
    return o.endsWith(suffix) && o.length > suffix.length;
  }
  return false;
}

function pathCovers(declared: string, observed: string): boolean {
  const d = normalize(declared);
  const o = normalize(observed);
  if (d.replace(/\/+$/, '') === o.replace(/\/+$/, '')) return true;
  const prefix = d.endsWith('/') ? d : d + '/';
  return o.startsWith(prefix);
}

function caseInsensitiveMatch(declared: string, observed: string): boolean {
  return normalize(declared) === normalize(observed);
}

function isCoveredBy(category: MismatchCategory, observed: string, declared: string): boolean {
  switch (category) {
    case 'network':
      return domainCovers(declared, observed);
    case 'filePaths':
      return pathCovers(declared, observed);
    default:
      return caseInsensitiveMatch(declared, observed);
  }
}

function inferPhantomCategory(value: string): MismatchCategory {
  const v = value.trim();
  if (v.startsWith('*.') || /^[a-z0-9][-a-z0-9]*\.[a-z]{2,}/i.test(v)) return 'network';
  if (v.startsWith('/') || v.startsWith('~/')) return 'filePaths';
  if (/^[A-Z][A-Z0-9_]*$/.test(v)) return 'envVars';
  return 'binaries';
}

// ---------------------------------------------------------------------------
// Core comparison
// ---------------------------------------------------------------------------

export function compareMetadataToObserved(
  metadata: SkillMetadata,
  observed: ObservedPermissions,
): MismatchReport {
  const declared = metadata.declaredPermissions;

  const declaredByCategory: Record<MismatchCategory, string[]> = {
    binaries: [], network: [], filePaths: [], envVars: [],
    shellCommands: [], configFiles: [], packageManagers: [], riskyCapabilities: [],
  };
  for (const d of declared) {
    declaredByCategory[inferPhantomCategory(d)].push(d);
  }

  const mismatches: Mismatch[] = [];
  for (const category of ALL_CATEGORIES) {
    const matchFn = category === 'network' ? domainCovers
                  : category === 'filePaths' ? pathCovers
                  : undefined;
    mismatches.push(
      ...computeCategoryMismatches(category, declaredByCategory[category], observed[category], matchFn),
    );
  }

  const undeclared = mismatches.filter(m => m.type === 'undeclared').length;
  const phantom = mismatches.filter(m => m.type === 'phantom').length;

  return {
    mismatches,
    summary: { undeclared, phantom, total: undeclared + phantom },
  };
}

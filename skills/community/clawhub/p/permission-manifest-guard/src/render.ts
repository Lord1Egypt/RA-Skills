import type { ObservedPermissions, MismatchReport, MismatchCategory, Disposition } from './policy.js';

// ---------------------------------------------------------------------------
// JSON manifest types
// ---------------------------------------------------------------------------

export interface DispositionJson {
  recommendation: string;
  score: number;
  reasons: string[];
}

export interface MismatchItem {
  category: string;
  value: string;
}

export interface MismatchesJson {
  undeclared: MismatchItem[];
  phantom: MismatchItem[];
}

export interface SummaryJson {
  total_observed: number;
  total_undeclared: number;
  total_phantom: number;
}

export interface ManifestJson {
  skill_name: string;
  generated_at: string;
  disposition: DispositionJson;
  observed: Record<string, string[]>;
  mismatches: MismatchesJson;
  summary: SummaryJson;
}

// ---------------------------------------------------------------------------
// Report types
// ---------------------------------------------------------------------------

export interface ManifestReport {
  skillName: string;
  observed: ObservedPermissions;
  mismatches: MismatchReport;
  disposition?: Disposition;
}

export interface PermissionItem {
  value: string;
  undeclared: boolean;
}

export interface CategoryMismatches {
  undeclared: string[];
  phantom: string[];
}

// ---------------------------------------------------------------------------
// Category display configuration
// ---------------------------------------------------------------------------

interface CategoryConfig {
  key: keyof ObservedPermissions;
  mismatchCategory: MismatchCategory;
  heading: string;
  description: string;
}

const CATEGORY_CONFIGS: readonly CategoryConfig[] = [
  { key: 'binaries', mismatchCategory: 'binaries', heading: 'Binaries', description: 'requests access to the following binaries' },
  { key: 'shellCommands', mismatchCategory: 'shellCommands', heading: 'Shell Commands', description: 'may require the following shell commands' },
  { key: 'network', mismatchCategory: 'network', heading: 'Network Domains', description: 'requests access to the following network domains' },
  { key: 'filePaths', mismatchCategory: 'filePaths', heading: 'File Paths', description: 'requests access to the following file paths' },
  { key: 'envVars', mismatchCategory: 'envVars', heading: 'Environment Variables', description: 'may require the following environment variables' },
  { key: 'configFiles', mismatchCategory: 'configFiles', heading: 'Config Files', description: 'requests access to the following config files' },
  { key: 'packageManagers', mismatchCategory: 'packageManagers', heading: 'Package Managers', description: 'may require the following package managers' },
  { key: 'riskyCapabilities', mismatchCategory: 'riskyCapabilities', heading: 'Risky Capabilities', description: 'may require the following risky capabilities' },
];

// ---------------------------------------------------------------------------
// Markdown rendering
// ---------------------------------------------------------------------------

export function renderPermissionSection(categoryName: string, items: PermissionItem[]): string {
  if (items.length === 0) return '';

  const lines: string[] = [];
  lines.push(`## ${categoryName}`);
  lines.push('');

  for (const item of items) {
    if (item.undeclared) {
      lines.push(`- \`${item.value}\` **[undeclared]**`);
    } else {
      lines.push(`- \`${item.value}\``);
    }
  }

  return lines.join('\n');
}

export function renderDispositionBanner(report: ManifestReport): string {
  if (!report.disposition) return '';

  const { recommendation, score, reasons } = report.disposition;
  const badge = `**[${recommendation.toUpperCase()}]**`;

  const lines: string[] = [];
  lines.push(`> ${badge} Severity score: ${score}`);

  if (reasons.length > 0) {
    lines.push('>');
    for (const reason of reasons) {
      lines.push(`> - ${reason}`);
    }
  }

  return lines.join('\n');
}

export function renderMismatchesSection(mismatches: CategoryMismatches): string {
  if (mismatches.undeclared.length === 0 && mismatches.phantom.length === 0) return '';

  const lines: string[] = [];
  lines.push('## Mismatches');
  lines.push('');

  if (mismatches.undeclared.length > 0) {
    lines.push('The following items may require review (observed but not declared):');
    lines.push('');
    for (const item of mismatches.undeclared) {
      lines.push(`- \`${item}\``);
    }
  }

  if (mismatches.phantom.length > 0) {
    if (mismatches.undeclared.length > 0) {
      lines.push('');
    }
    lines.push('The following items were declared but not observed in code:');
    lines.push('');
    for (const item of mismatches.phantom) {
      lines.push(`- \`${item}\``);
    }
  }

  return lines.join('\n');
}

export function renderSummarySection(report: ManifestReport): string {
  const totalObserved = Object.values(report.observed).reduce(
    (sum, arr) => sum + (arr as string[]).length,
    0,
  );
  const undeclaredCount = report.mismatches.summary.undeclared;
  const phantomCount = report.mismatches.summary.phantom;
  const declaredCount = totalObserved - undeclaredCount;

  const lines: string[] = [];
  lines.push('## Summary');
  lines.push('');
  lines.push(`- Total permissions observed: ${totalObserved}`);
  lines.push(`- Declared: ${declaredCount}`);
  lines.push(`- Undeclared: ${undeclaredCount}`);
  lines.push(`- Phantom: ${phantomCount}`);

  if (report.disposition) {
    lines.push(`- Disposition: **${report.disposition.recommendation}** (score: ${report.disposition.score})`);
  }

  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// renderMarkdownManifest
// ---------------------------------------------------------------------------

export function renderMarkdownManifest(
  observed: ObservedPermissions,
  mismatches: MismatchReport,
  disposition: Disposition,
  skillName: string,
): string {
  const sections: string[] = [];

  sections.push(`# Permission Manifest: ${skillName}`);

  const banner = renderDispositionBanner({ skillName, observed, mismatches, disposition });
  if (banner) {
    sections.push(banner);
  }

  const undeclaredSets = new Map<MismatchCategory, Set<string>>();
  for (const m of mismatches.mismatches) {
    if (m.type === 'undeclared') {
      if (!undeclaredSets.has(m.category)) {
        undeclaredSets.set(m.category, new Set());
      }
      undeclaredSets.get(m.category)!.add(m.value);
    }
  }

  for (const config of CATEGORY_CONFIGS) {
    const items = observed[config.key];
    if (items.length === 0) continue;

    const undeclared = undeclaredSets.get(config.mismatchCategory) ?? new Set<string>();

    const permItems: PermissionItem[] = items.map(item => ({
      value: item,
      undeclared: undeclared.has(item),
    }));

    const section = renderPermissionSection(config.heading, permItems);
    if (!section) continue;

    const splitPos = section.indexOf('\n\n') + 2;
    const withDescription =
      section.slice(0, splitPos) +
      `This skill ${config.description}:\n\n` +
      section.slice(splitPos);

    sections.push(withDescription);
  }

  const categoryMismatches: CategoryMismatches = {
    undeclared: mismatches.mismatches.filter(m => m.type === 'undeclared').map(m => m.value),
    phantom: mismatches.mismatches.filter(m => m.type === 'phantom').map(m => m.value),
  };

  const mismatchSection = renderMismatchesSection(categoryMismatches);
  if (mismatchSection) {
    sections.push(mismatchSection);
  }

  const report: ManifestReport = { skillName, observed, mismatches, disposition };
  sections.push(renderSummarySection(report));

  return sections.join('\n\n').trimEnd();
}

// ---------------------------------------------------------------------------
// renderJsonManifest
// ---------------------------------------------------------------------------

export function renderJsonManifest(
  observed: ObservedPermissions,
  mismatches: MismatchReport,
  disposition: Disposition,
  skillName: string,
): string {
  const totalObserved = Object.values(observed).reduce(
    (sum, arr) => sum + (arr as string[]).length,
    0,
  );

  const undeclared: MismatchItem[] = mismatches.mismatches
    .filter(m => m.type === 'undeclared')
    .map(m => ({ category: m.category, value: m.value }));

  const phantom: MismatchItem[] = mismatches.mismatches
    .filter(m => m.type === 'phantom')
    .map(m => ({ category: m.category, value: m.value }));

  const manifest: ManifestJson = {
    skill_name: skillName,
    generated_at: new Date().toISOString(),
    disposition: {
      recommendation: disposition.recommendation,
      score: disposition.score,
      reasons: disposition.reasons,
    },
    observed: {
      binaries: observed.binaries,
      shellCommands: observed.shellCommands,
      network: observed.network,
      filePaths: observed.filePaths,
      envVars: observed.envVars,
      configFiles: observed.configFiles,
      packageManagers: observed.packageManagers,
      riskyCapabilities: observed.riskyCapabilities,
    },
    mismatches: { undeclared, phantom },
    summary: {
      total_observed: totalObserved,
      total_undeclared: undeclared.length,
      total_phantom: phantom.length,
    },
  };

  return JSON.stringify(manifest, null, 2);
}

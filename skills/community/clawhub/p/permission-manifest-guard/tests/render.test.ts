import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { renderDispositionBanner, renderJsonManifest, renderMarkdownManifest, renderMismatchesSection, renderPermissionSection, renderSummarySection } from '../src/render.js';
import type { CategoryMismatches, ManifestJson, ManifestReport, PermissionItem } from '../src/render.js';
import type { ObservedPermissions, MismatchReport, Mismatch, Disposition } from '../src/policy.js';

function emptyObserved(): ObservedPermissions {
  return {
    binaries: [],
    network: [],
    filePaths: [],
    envVars: [],
    shellCommands: [],
    configFiles: [],
    packageManagers: [],
    riskyCapabilities: [],
  };
}

function emptyMismatchReport(): MismatchReport {
  return { mismatches: [], summary: { undeclared: 0, phantom: 0, total: 0 } };
}

function makeReport(mismatches: Mismatch[]): MismatchReport {
  const undeclared = mismatches.filter(m => m.type === 'undeclared').length;
  const phantom = mismatches.filter(m => m.type === 'phantom').length;
  return { mismatches, summary: { undeclared, phantom, total: undeclared + phantom } };
}

// ---------------------------------------------------------------------------
// renderDispositionBanner
// ---------------------------------------------------------------------------

describe('renderDispositionBanner', () => {
  it('returns empty string when disposition is absent', () => {
    const report: ManifestReport = {
      skillName: 'test-skill',
      observed: emptyObserved(),
      mismatches: emptyMismatchReport(),
    };
    assert.equal(renderDispositionBanner(report), '');
  });

  it('renders reject banner with badge and score', () => {
    const report: ManifestReport = {
      skillName: 'dangerous-skill',
      observed: emptyObserved(),
      mismatches: emptyMismatchReport(),
      disposition: {
        recommendation: 'reject',
        score: 22,
        reasons: [
          '1 undeclared riskyCapabilities (+10)',
          '2 undeclared network (+12)',
        ],
      },
    };
    const result = renderDispositionBanner(report);

    assert.ok(result.startsWith('>'), 'banner is a blockquote');
    assert.ok(result.includes('**[REJECT]**'), 'contains badge-style recommendation');
    assert.ok(result.includes('Severity score: 22'), 'contains numeric score');
    assert.ok(result.includes('1 undeclared riskyCapabilities (+10)'), 'contains first reason');
    assert.ok(result.includes('2 undeclared network (+12)'), 'contains second reason');
    // Every line must be a blockquote
    for (const line of result.split('\n')) {
      assert.ok(line.startsWith('>'), `all lines are blockquotes: "${line}"`);
    }
  });

  it('renders review banner without reasons when reasons array is empty', () => {
    const report: ManifestReport = {
      skillName: 'mild-skill',
      observed: emptyObserved(),
      mismatches: emptyMismatchReport(),
      disposition: {
        recommendation: 'review',
        score: 3,
        reasons: [],
      },
    };
    const result = renderDispositionBanner(report);

    assert.ok(result.includes('**[REVIEW]**'));
    assert.ok(result.includes('Severity score: 3'));
    assert.equal(result.split('\n').length, 1, 'single line when no reasons');
  });
});

// ---------------------------------------------------------------------------
// renderPermissionSection
// ---------------------------------------------------------------------------

describe('renderPermissionSection', () => {
  it('returns empty string for empty items array', () => {
    assert.equal(renderPermissionSection('Binaries', []), '');
  });

  it('returns H2 heading followed by bullet list', () => {
    const items: PermissionItem[] = [
      { value: 'curl', undeclared: false },
      { value: 'wget', undeclared: true },
    ];
    const result = renderPermissionSection('Binaries', items);

    assert.ok(result.startsWith('## Binaries'));
    assert.ok(result.includes('- `curl`'));
    assert.ok(result.includes('- `wget` **[undeclared]**'));
    // No trailing newline
    assert.ok(!result.endsWith('\n'));
  });

  it('marks undeclared items with visual badge', () => {
    const items: PermissionItem[] = [
      { value: 'api.example.com', undeclared: false },
      { value: 'evil.com', undeclared: true },
    ];
    const result = renderPermissionSection('Network Domains', items);

    assert.ok(result.includes('- `api.example.com`'));
    assert.ok(!result.includes('`api.example.com` **[undeclared]**'));
    assert.ok(result.includes('- `evil.com` **[undeclared]**'));
  });

  it('produces no orphaned H2 when items is empty', () => {
    const result = renderPermissionSection('Shell Commands', []);
    assert.equal(result, '');
    assert.ok(!result.includes('##'));
  });
});

// ---------------------------------------------------------------------------
// renderMismatchesSection
// ---------------------------------------------------------------------------

describe('renderMismatchesSection', () => {
  it('returns empty string when both undeclared and phantom arrays are empty', () => {
    const mismatches: CategoryMismatches = { undeclared: [], phantom: [] };
    assert.equal(renderMismatchesSection(mismatches), '');
  });

  it('renders undeclared items with conservative phrasing', () => {
    const mismatches: CategoryMismatches = {
      undeclared: ['curl', 'evil.com'],
      phantom: [],
    };
    const result = renderMismatchesSection(mismatches);

    assert.ok(result.startsWith('## Mismatches'));
    assert.ok(result.includes('may require review'), 'uses conservative phrasing');
    assert.ok(result.includes('- `curl`'));
    assert.ok(result.includes('- `evil.com`'));
    assert.ok(!result.includes('declared but not observed'));
  });

  it('renders phantom items with declared-but-not-observed phrasing', () => {
    const mismatches: CategoryMismatches = {
      undeclared: [],
      phantom: ['phantom-binary', '*.ghost.com'],
    };
    const result = renderMismatchesSection(mismatches);

    assert.ok(result.startsWith('## Mismatches'));
    assert.ok(result.includes('declared but not observed'), 'phantom phrasing');
    assert.ok(result.includes('- `phantom-binary`'));
    assert.ok(result.includes('- `*.ghost.com`'));
    assert.ok(!result.includes('may require review'));
  });

  it('renders both undeclared and phantom as separate sub-lists', () => {
    const mismatches: CategoryMismatches = {
      undeclared: ['wget', 'evil.com'],
      phantom: ['phantom-cli'],
    };
    const result = renderMismatchesSection(mismatches);

    assert.ok(result.includes('## Mismatches'));
    assert.ok(result.includes('may require review'));
    assert.ok(result.includes('declared but not observed'));
    assert.ok(result.includes('- `wget`'));
    assert.ok(result.includes('- `evil.com`'));
    assert.ok(result.includes('- `phantom-cli`'));

    // Undeclared section appears before phantom section
    const undeclaredPos = result.indexOf('may require review');
    const phantomPos = result.indexOf('declared but not observed');
    assert.ok(undeclaredPos < phantomPos, 'undeclared listed before phantoms');
  });
});

// ---------------------------------------------------------------------------
// renderSummarySection
// ---------------------------------------------------------------------------

describe('renderSummarySection', () => {
  it('renders correct counts for a full manifest with all categories populated', () => {
    const observed: ObservedPermissions = {
      binaries: ['curl', 'wget'],
      shellCommands: ['rm -rf /tmp/cache'],
      network: ['api.example.com', 'evil.com'],
      filePaths: ['/tmp/cache.json'],
      envVars: ['API_KEY', 'SECRET_TOKEN'],
      configFiles: ['.npmrc'],
      packageManagers: ['npm install'],
      riskyCapabilities: ['eval()'],
    };
    const report: ManifestReport = {
      skillName: 'test-skill',
      observed,
      mismatches: makeReport([
        { category: 'binaries', value: 'wget', type: 'undeclared' },
        { category: 'network', value: 'evil.com', type: 'undeclared' },
        { category: 'envVars', value: 'SECRET_TOKEN', type: 'undeclared' },
        { category: 'binaries', value: 'phantom-bin', type: 'phantom' },
      ]),
      disposition: { recommendation: 'reject', score: 25, reasons: [] },
    };

    const result = renderSummarySection(report);

    assert.ok(result.startsWith('## Summary'));
    assert.ok(result.includes('- Total permissions observed: 11'));
    assert.ok(result.includes('- Declared: 8'));
    assert.ok(result.includes('- Undeclared: 3'));
    assert.ok(result.includes('- Phantom: 1'));
    assert.ok(result.includes('- Disposition: **reject** (score: 25)'));
  });

  it('renders minimal summary for single category with no mismatches', () => {
    const report: ManifestReport = {
      skillName: 'safe-skill',
      observed: { ...emptyObserved(), binaries: ['git'] },
      mismatches: emptyMismatchReport(),
      disposition: { recommendation: 'allow', score: 0, reasons: [] },
    };

    const result = renderSummarySection(report);

    assert.ok(result.includes('- Total permissions observed: 1'));
    assert.ok(result.includes('- Declared: 1'));
    assert.ok(result.includes('- Undeclared: 0'));
    assert.ok(result.includes('- Phantom: 0'));
    assert.ok(result.includes('- Disposition: **allow** (score: 0)'));
  });

  it('renders zero counts when no permissions are observed', () => {
    const report: ManifestReport = {
      skillName: 'empty-skill',
      observed: emptyObserved(),
      mismatches: emptyMismatchReport(),
      disposition: { recommendation: 'allow', score: 0, reasons: [] },
    };

    const result = renderSummarySection(report);

    assert.ok(result.startsWith('## Summary'));
    assert.ok(result.includes('- Total permissions observed: 0'));
    assert.ok(result.includes('- Declared: 0'));
    assert.ok(result.includes('- Undeclared: 0'));
    assert.ok(result.includes('- Phantom: 0'));
  });

  it('omits disposition line when disposition is absent', () => {
    const report: ManifestReport = {
      skillName: 'no-disp-skill',
      observed: { ...emptyObserved(), envVars: ['NODE_ENV'] },
      mismatches: emptyMismatchReport(),
    };

    const result = renderSummarySection(report);

    assert.ok(result.includes('## Summary'));
    assert.ok(result.includes('- Total permissions observed: 1'));
    assert.ok(!result.includes('Disposition:'), 'no disposition line when absent');
  });
});

// ---------------------------------------------------------------------------
// renderMarkdownManifest (T019.e)
// ---------------------------------------------------------------------------

describe('renderMarkdownManifest', () => {
  it('renders full manifest with all categories populated', () => {
    const observed: ObservedPermissions = {
      binaries: ['curl', 'wget'],
      shellCommands: ['rm -rf /tmp/cache'],
      network: ['api.example.com', 'evil.com'],
      filePaths: ['/tmp/cache.json', '/etc/hosts'],
      envVars: ['API_KEY', 'SECRET_TOKEN'],
      configFiles: ['.npmrc'],
      packageManagers: ['npm install'],
      riskyCapabilities: ['eval()'],
    };

    const mismatches = makeReport([
      { category: 'binaries', value: 'wget', type: 'undeclared' },
      { category: 'network', value: 'evil.com', type: 'undeclared' },
      { category: 'filePaths', value: '/etc/hosts', type: 'undeclared' },
      { category: 'envVars', value: 'SECRET_TOKEN', type: 'undeclared' },
      { category: 'riskyCapabilities', value: 'eval()', type: 'undeclared' },
    ]);

    const disposition: Disposition = {
      recommendation: 'reject',
      score: 30,
      reasons: ['5 undeclared across categories (+30)'],
    };

    const result = renderMarkdownManifest(observed, mismatches, disposition, 'risky-skill');

    // Title
    assert.ok(result.startsWith('# Permission Manifest: risky-skill'));

    // No trailing newlines
    assert.ok(!result.endsWith('\n'), 'no trailing newline');

    // Disposition banner present as blockquote
    assert.ok(result.includes('**[REJECT]**'));
    assert.ok(result.includes('Severity score: 30'));

    // All category headers present
    assert.ok(result.includes('## Binaries'));
    assert.ok(result.includes('## Shell Commands'));
    assert.ok(result.includes('## Network Domains'));
    assert.ok(result.includes('## File Paths'));
    assert.ok(result.includes('## Environment Variables'));
    assert.ok(result.includes('## Config Files'));
    assert.ok(result.includes('## Package Managers'));
    assert.ok(result.includes('## Risky Capabilities'));

    // Declared items appear without badge
    assert.ok(result.includes('- `curl`'));
    assert.ok(result.includes('- `api.example.com`'));

    // Undeclared items carry the visual badge
    assert.ok(result.includes('- `wget` **[undeclared]**'));
    assert.ok(result.includes('- `evil.com` **[undeclared]**'));
    assert.ok(result.includes('- `/etc/hosts` **[undeclared]**'));
    assert.ok(result.includes('- `SECRET_TOKEN` **[undeclared]**'));
    assert.ok(result.includes('- `eval()` **[undeclared]**'));

    // Conservative language present
    assert.ok(result.includes('requests access to'));
    assert.ok(result.includes('may require'));

    // Valid CommonMark — no raw HTML tags, no ANSI escapes
    assert.ok(!/<[a-z][\s\S]*>/i.test(result), 'no raw HTML');
    assert.ok(!/\x1b\[/.test(result), 'no ANSI escapes');

    // Sections joined with double newlines
    assert.ok(result.includes('\n\n## '), 'sections separated by double newlines');

    // Summary section present with correct counts
    assert.ok(result.includes('## Summary'));
    assert.ok(result.includes('- Total permissions observed: 12'));
    assert.ok(result.includes('- Undeclared: 5'));
    assert.ok(result.includes('- Disposition: **reject** (score: 30)'));

    // Mismatches section present
    assert.ok(result.includes('## Mismatches'));
  });

  it('renders minimal manifest with single category and no mismatches', () => {
    const observed: ObservedPermissions = {
      ...emptyObserved(),
      binaries: ['git'],
    };

    const disposition: Disposition = {
      recommendation: 'allow',
      score: 0,
      reasons: [],
    };

    const result = renderMarkdownManifest(observed, emptyMismatchReport(), disposition, 'safe-skill');

    assert.ok(result.startsWith('# Permission Manifest: safe-skill'));
    assert.ok(!result.endsWith('\n'), 'no trailing newline');
    assert.ok(result.includes('## Binaries'));
    assert.ok(result.includes('- `git`'));

    // No undeclared badges
    assert.ok(!result.includes('**[undeclared]**'));

    // No mismatches section when no mismatches exist
    assert.ok(!result.includes('## Mismatches'));

    // One category section plus summary only
    const h2Count = (result.match(/^## /gm) ?? []).length;
    assert.equal(h2Count, 2, 'one category section plus summary');

    // Summary section present
    assert.ok(result.includes('## Summary'));
    assert.ok(result.includes('- Total permissions observed: 1'));
  });

  it('omits empty categories — no orphaned H2 headers', () => {
    const observed: ObservedPermissions = {
      ...emptyObserved(),
      envVars: ['NODE_ENV'],
      network: ['api.example.com'],
    };

    const disposition: Disposition = {
      recommendation: 'review',
      score: 2,
      reasons: ['1 undeclared configFiles (+2)'],
    };

    const result = renderMarkdownManifest(observed, emptyMismatchReport(), disposition, 'partial-skill');

    // Present sections
    assert.ok(result.includes('## Network Domains'));
    assert.ok(result.includes('## Environment Variables'));

    // Absent sections — these categories are empty, no orphaned headers
    assert.ok(!result.includes('## Binaries'));
    assert.ok(!result.includes('## Shell Commands'));
    assert.ok(!result.includes('## File Paths'));
    assert.ok(!result.includes('## Config Files'));
    assert.ok(!result.includes('## Package Managers'));
    assert.ok(!result.includes('## Risky Capabilities'));

    // Two category sections plus summary
    const h2Count = (result.match(/^## /gm) ?? []).length;
    assert.equal(h2Count, 3, 'two category sections plus summary');

    // No trailing newlines or orphaned content
    assert.ok(!result.endsWith('\n'), 'no trailing newline');

    // Every H2 has content following it (no orphaned headers)
    const lines = result.split('\n');
    for (let i = 0; i < lines.length; i++) {
      if (lines[i]!.startsWith('## ')) {
        const nextNonEmpty = lines.slice(i + 1).find(l => l.trim() !== '');
        assert.ok(nextNonEmpty !== undefined, `H2 "${lines[i]}" has content after it`);
        assert.ok(!nextNonEmpty!.startsWith('## ') && !nextNonEmpty!.startsWith('# '),
          `H2 "${lines[i]}" is not immediately followed by another heading`);
      }
    }
  });

  it('renders disposition banner with reject recommendation and reasons', () => {
    const observed: ObservedPermissions = {
      ...emptyObserved(),
      riskyCapabilities: ['eval()', 'child_process exec/spawn'],
    };

    const mismatches = makeReport([
      { category: 'riskyCapabilities', value: 'eval()', type: 'undeclared' },
      { category: 'riskyCapabilities', value: 'child_process exec/spawn', type: 'undeclared' },
    ]);

    const disposition: Disposition = {
      recommendation: 'reject',
      score: 20,
      reasons: [
        '2 undeclared riskyCapabilities (+20)',
      ],
    };

    const result = renderMarkdownManifest(observed, mismatches, disposition, 'evil-skill');

    // Banner is a blockquote with recommendation word and numeric score
    const bannerLines = result.split('\n').filter(l => l.startsWith('>'));
    assert.ok(bannerLines.length >= 1, 'has blockquote lines');
    assert.ok(bannerLines[0]!.includes('**[REJECT]**'), 'badge-style recommendation');
    assert.ok(bannerLines[0]!.includes('Severity score: 20'), 'numeric score');
    assert.ok(bannerLines.some(l => l.includes('2 undeclared riskyCapabilities (+20)')), 'reason in banner');

    // All banner lines are valid blockquotes
    for (const line of bannerLines) {
      assert.ok(line.startsWith('>'), `blockquote line: "${line}"`);
    }

    // Undeclared badges on items
    assert.ok(result.includes('- `eval()` **[undeclared]**'));
    assert.ok(result.includes('- `child_process exec/spawn` **[undeclared]**'));

    // No trailing newlines
    assert.ok(!result.endsWith('\n'), 'no trailing newline');
  });
});

// ---------------------------------------------------------------------------
// renderJsonManifest (T020.b)
// ---------------------------------------------------------------------------

describe('renderJsonManifest', () => {
  it('full manifest round-trip: stringify then parse, verify all keys and counts', () => {
    const observed: ObservedPermissions = {
      binaries: ['curl', 'wget'],
      shellCommands: ['rm -rf /tmp/cache'],
      network: ['api.example.com', 'evil.com'],
      filePaths: ['/tmp/cache.json'],
      envVars: ['API_KEY', 'SECRET_TOKEN'],
      configFiles: ['.npmrc'],
      packageManagers: ['npm install'],
      riskyCapabilities: ['eval()'],
    };

    const mismatches = makeReport([
      { category: 'binaries', value: 'wget', type: 'undeclared' },
      { category: 'network', value: 'evil.com', type: 'undeclared' },
      { category: 'envVars', value: 'SECRET_TOKEN', type: 'undeclared' },
      { category: 'binaries', value: 'phantom-bin', type: 'phantom' },
    ]);

    const disposition: Disposition = {
      recommendation: 'reject',
      score: 25,
      reasons: ['3 undeclared across categories (+25)'],
    };

    const jsonStr = renderJsonManifest(observed, mismatches, disposition, 'test-skill');
    const parsed: ManifestJson = JSON.parse(jsonStr);

    // Top-level keys are exactly the required set
    const expectedKeys = ['skill_name', 'generated_at', 'disposition', 'observed', 'mismatches', 'summary'];
    assert.deepStrictEqual(Object.keys(parsed).sort(), expectedKeys.sort());

    assert.equal(parsed.skill_name, 'test-skill');

    // generated_at is valid ISO 8601
    assert.ok(!isNaN(Date.parse(parsed.generated_at)), 'generated_at is valid ISO 8601');

    // disposition
    assert.equal(parsed.disposition.recommendation, 'reject');
    assert.equal(parsed.disposition.score, 25);
    assert.deepStrictEqual(parsed.disposition.reasons, ['3 undeclared across categories (+25)']);

    // observed categories all present
    assert.deepStrictEqual(parsed.observed.binaries, ['curl', 'wget']);
    assert.deepStrictEqual(parsed.observed.network, ['api.example.com', 'evil.com']);
    assert.deepStrictEqual(parsed.observed.riskyCapabilities, ['eval()']);

    // summary counts match actual data
    assert.equal(parsed.summary.total_observed, 11);
    assert.equal(parsed.summary.total_undeclared, 3);
    assert.equal(parsed.summary.total_phantom, 1);
    assert.equal(parsed.mismatches.undeclared.length, parsed.summary.total_undeclared);
    assert.equal(parsed.mismatches.phantom.length, parsed.summary.total_phantom);
  });

  it('empty-skill manifest: no observed permissions, all arrays empty, disposition is allow', () => {
    const observed = emptyObserved();
    const disposition: Disposition = { recommendation: 'allow', score: 0, reasons: [] };

    const jsonStr = renderJsonManifest(observed, emptyMismatchReport(), disposition, 'empty-skill');
    const parsed: ManifestJson = JSON.parse(jsonStr);

    assert.equal(parsed.skill_name, 'empty-skill');
    assert.equal(parsed.disposition.recommendation, 'allow');
    assert.equal(parsed.disposition.score, 0);
    assert.deepStrictEqual(parsed.disposition.reasons, []);

    // All observed category keys present with empty arrays
    const observedKeys = ['binaries', 'shellCommands', 'network', 'filePaths', 'envVars', 'configFiles', 'packageManagers', 'riskyCapabilities'];
    for (const key of observedKeys) {
      assert.ok(key in parsed.observed, `observed.${key} is present`);
      assert.deepStrictEqual(parsed.observed[key], [], `observed.${key} is empty`);
    }

    assert.deepStrictEqual(parsed.mismatches.undeclared, []);
    assert.deepStrictEqual(parsed.mismatches.phantom, []);
    assert.equal(parsed.summary.total_observed, 0);
    assert.equal(parsed.summary.total_undeclared, 0);
    assert.equal(parsed.summary.total_phantom, 0);
  });

  it('mismatches appear correctly in undeclared/phantom arrays', () => {
    const observed: ObservedPermissions = {
      ...emptyObserved(),
      binaries: ['curl', 'wget'],
      network: ['secret.io'],
    };

    const mismatches = makeReport([
      { category: 'binaries', value: 'wget', type: 'undeclared' },
      { category: 'network', value: 'secret.io', type: 'undeclared' },
      { category: 'binaries', value: 'phantom-tool', type: 'phantom' },
      { category: 'network', value: '*.ghost.com', type: 'phantom' },
    ]);

    const disposition: Disposition = { recommendation: 'sandbox', score: 12, reasons: [] };

    const jsonStr = renderJsonManifest(observed, mismatches, disposition, 'mismatch-skill');
    const parsed: ManifestJson = JSON.parse(jsonStr);

    // Undeclared items
    assert.equal(parsed.mismatches.undeclared.length, 2);
    assert.ok(parsed.mismatches.undeclared.some(
      m => m.category === 'binaries' && m.value === 'wget',
    ));
    assert.ok(parsed.mismatches.undeclared.some(
      m => m.category === 'network' && m.value === 'secret.io',
    ));

    // Phantom items
    assert.equal(parsed.mismatches.phantom.length, 2);
    assert.ok(parsed.mismatches.phantom.some(
      m => m.category === 'binaries' && m.value === 'phantom-tool',
    ));
    assert.ok(parsed.mismatches.phantom.some(
      m => m.category === 'network' && m.value === '*.ghost.com',
    ));

    // Summary counts match array lengths
    assert.equal(parsed.summary.total_undeclared, parsed.mismatches.undeclared.length);
    assert.equal(parsed.summary.total_phantom, parsed.mismatches.phantom.length);
    assert.equal(parsed.summary.total_observed, 3);
  });
});

// ---------------------------------------------------------------------------
// Recommendation rendering — disposition tiers (T027)
// ---------------------------------------------------------------------------

describe('recommendation rendering', () => {
  it('review disposition: output contains review badge and lists the finding summary', () => {
    const observed: ObservedPermissions = {
      ...emptyObserved(),
      envVars: ['API_KEY'],
    };

    const mismatches = makeReport([
      { category: 'envVars', value: 'API_KEY', type: 'undeclared' },
    ]);

    const disposition: Disposition = {
      recommendation: 'review',
      score: 4,
      reasons: ['1 undeclared envVars (+4)'],
    };

    const result = renderMarkdownManifest(observed, mismatches, disposition, 'review-skill');

    assert.ok(result.includes('**[REVIEW]**'), 'contains review badge');
    assert.ok(result.includes('Severity score: 4'), 'contains severity score');
    assert.ok(result.includes('1 undeclared envVars (+4)'), 'lists the finding reason');
    assert.ok(result.includes('`API_KEY`'), 'lists the finding value');
    assert.ok(result.includes('**[undeclared]**'), 'undeclared badge on the finding');
    assert.ok(result.includes('## Summary'), 'has summary section');
    assert.ok(result.includes('Disposition: **review**'), 'summary shows review disposition');
  });

  it('reject with single critical finding: output contains reject indicator and critical finding', () => {
    const observed: ObservedPermissions = {
      ...emptyObserved(),
      riskyCapabilities: ['eval()'],
    };

    const mismatches = makeReport([
      { category: 'riskyCapabilities', value: 'eval()', type: 'undeclared' },
    ]);

    const disposition: Disposition = {
      recommendation: 'reject',
      score: 10,
      reasons: ['1 undeclared riskyCapabilities (+10)'],
    };

    const result = renderMarkdownManifest(observed, mismatches, disposition, 'dangerous-skill');

    assert.ok(result.includes('**[REJECT]**'), 'contains reject badge');
    assert.ok(result.includes('Severity score: 10'), 'contains severity score');
    assert.ok(result.includes('1 undeclared riskyCapabilities (+10)'), 'lists the critical reason');
    assert.ok(result.includes('- `eval()` **[undeclared]**'), 'critical finding marked undeclared');
    assert.ok(result.includes('## Risky Capabilities'), 'risky capabilities section present');
    assert.ok(result.includes('Disposition: **reject**'), 'summary shows reject disposition');
  });

  it('reject with multiple findings across categories: output contains all findings and reject indicator', () => {
    const observed: ObservedPermissions = {
      ...emptyObserved(),
      binaries: ['wget'],
      network: ['evil.com'],
      riskyCapabilities: ['child_process exec/spawn'],
    };

    const mismatches = makeReport([
      { category: 'binaries', value: 'wget', type: 'undeclared' },
      { category: 'network', value: 'evil.com', type: 'undeclared' },
      { category: 'riskyCapabilities', value: 'child_process exec/spawn', type: 'undeclared' },
    ]);

    const disposition: Disposition = {
      recommendation: 'reject',
      score: 26,
      reasons: [
        '1 undeclared binaries (+4)',
        '1 undeclared network (+6)',
        '1 undeclared riskyCapabilities (+10)',
      ],
    };

    const result = renderMarkdownManifest(observed, mismatches, disposition, 'multi-threat-skill');

    assert.ok(result.includes('**[REJECT]**'), 'contains reject badge');

    // All finding values present with undeclared badge
    assert.ok(result.includes('- `wget` **[undeclared]**'), 'binary finding marked undeclared');
    assert.ok(result.includes('- `evil.com` **[undeclared]**'), 'network finding marked undeclared');
    assert.ok(result.includes('- `child_process exec/spawn` **[undeclared]**'), 'risky capability finding marked undeclared');

    // Category sections for all 3 categories present
    assert.ok(result.includes('## Binaries'), 'binaries section present');
    assert.ok(result.includes('## Network Domains'), 'network section present');
    assert.ok(result.includes('## Risky Capabilities'), 'risky capabilities section present');

    // All reasons listed in banner
    assert.ok(result.includes('1 undeclared binaries (+4)'), 'binary reason in banner');
    assert.ok(result.includes('1 undeclared network (+6)'), 'network reason in banner');
    assert.ok(result.includes('1 undeclared riskyCapabilities (+10)'), 'risky reason in banner');

    // Mismatches section aggregates all undeclared items
    assert.ok(result.includes('## Mismatches'), 'mismatches section present');

    assert.ok(result.includes('Disposition: **reject**'), 'summary shows reject disposition');
    assert.ok(result.includes('- Undeclared: 3'), 'summary undeclared count correct');
  });
});

// Pipeline orchestrator for permission-manifest-guard.

import { discoverFiles, readSkillMetadata, readDiscoveredFiles } from './discovery.js';
import {
  extractBinaries, extractDomains, extractEnvVars,
  extractFilePaths, extractShellCommands, extractPackageManagers,
  extractConfigFiles,
} from './extract.js';
import { detectRiskyCapabilities } from './classify.js';
import { compareMetadataToObserved, recommendDisposition } from './policy.js';
import type { ObservedPermissions } from './policy.js';
import type { DiscoveredFile } from './types.js';
import { renderMarkdownManifest, renderJsonManifest } from './render.js';

export { extractDomains, extractShellCommands } from './extract.js';
export type { ShellCommand, Domain, EnvVar } from './extract.js';
export type { DiscoveredFile } from './types.js';

export interface DiagnosticWarning {
  file: string;
  stage: string;
  message: string;
  error: string;
}

export interface AnalysisResult {
  markdownManifest: string;
  jsonManifest: object;
  diagnostics: DiagnosticWarning[];
}

/** Pipeline: discover → extract → classify → policy → render. */
export async function analyzeSkill(skillDir: string): Promise<AnalysisResult> {
  const diagnostics: DiagnosticWarning[] = [];
  const empty: AnalysisResult = { markdownManifest: '', jsonManifest: {}, diagnostics };

  const filePaths = await discoverFiles(skillDir);
  if (filePaths.length === 0) {
    diagnostics.push({ file: skillDir, stage: 'discovery', message: 'No files discovered in skill directory', error: 'empty or missing directory' });
    return empty;
  }
  const { files, diagnostics: readDiags } = await readDiscoveredFiles(filePaths, skillDir);
  for (const msg of readDiags) {
    diagnostics.push({ file: skillDir, stage: 'discovery', message: msg, error: msg });
  }
  if (files.length === 0) {
    diagnostics.push({ file: skillDir, stage: 'discovery', message: 'All discovered files failed to read', error: 'no readable files' });
    return empty;
  }
  const metadata = await readSkillMetadata(skillDir);

  const observed = await extractPerFile(files, filePaths, skillDir, diagnostics);

  let risky: string[] = [];
  try { risky = detectRiskyCapabilities(files).map(r => r.capability); }
  catch (err) { diagnostics.push({ file: '', stage: 'classification', message: 'Classification failed', error: (err as Error).message }); }
  const classified: ObservedPermissions = { ...observed, riskyCapabilities: risky };

  const mismatches = compareMetadataToObserved(metadata, classified);
  const disposition = recommendDisposition(mismatches);

  const name = metadata.name || 'unknown';
  const md = renderMarkdownManifest(classified, mismatches, disposition, name);
  const json = renderJsonManifest(classified, mismatches, disposition, name);

  return { markdownManifest: md, jsonManifest: JSON.parse(json), diagnostics };
}

// ---------------------------------------------------------------------------
// Per-file extraction with error isolation (exported for testing).
// ---------------------------------------------------------------------------

export async function extractPerFile(
  files: DiscoveredFile[], paths: string[], dir: string, diags: DiagnosticWarning[],
): Promise<ObservedPermissions> {
  const binaries: string[] = [];
  const network: string[] = [];
  const envVars: string[] = [];
  const fps: string[] = [];
  const cmds: string[] = [];
  const configs: string[] = [];
  const pkgs: string[] = [];

  for (const p of paths) {
    try { binaries.push(...(await extractBinaries([p], dir)).map(b => b.value)); }
    catch (err) { diags.push({ file: p, stage: 'extraction', message: 'Binary extraction failed', error: (err as Error).message }); }
  }

  for (const file of files) {
    try {
      network.push(...extractDomains([file]).map(d => d.hostname));
      envVars.push(...extractEnvVars([file]).map(e => e.name));
      fps.push(...extractFilePaths([file]).map(fp => fp.path));
      cmds.push(...extractShellCommands([file]).map(c => c.command));
      configs.push(...extractConfigFiles([file]).map(c => c.matchedPattern));
      pkgs.push(...extractPackageManagers([file]).map(pm => pm.manager));
    } catch (err) {
      diags.push({ file: file.path, stage: 'extraction', message: `Extraction failed for ${file.path}`, error: (err as Error).message });
    }
  }

  return {
    binaries: [...new Set(binaries)],
    network: [...new Set(network)],
    envVars: [...new Set(envVars)],
    filePaths: [...new Set(fps)],
    shellCommands: [...new Set(cmds)],
    configFiles: [...new Set(configs)],
    packageManagers: [...new Set(pkgs)],
    riskyCapabilities: [],
  };
}

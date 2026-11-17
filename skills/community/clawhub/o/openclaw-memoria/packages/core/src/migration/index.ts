/**
 * Migration legacy v3.34 → V3 (spec §7.1) :
 * schéma v3.34 reconstitué + importeur backup→quarantaine→vérif/rollback.
 */
export { createSyntheticLegacyDb } from './legacy-schema.js'
export type { SyntheticLegacyOptions, SyntheticLegacySummary } from './legacy-schema.js'
export { importLegacyDb } from './import-legacy.js'
export type { ImportLegacyInput, ImportLegacyReport } from './import-legacy.js'
export { importTranscripts } from './import-transcripts.js'
export type { ImportTranscriptsInput, ImportTranscriptsReport, ImportTranscriptsMemoria, ImportTranscriptsProgress } from './import-transcripts.js'
export {
  parseClaudeCodeTranscript,
  parseCodexRollout,
  parseCodexHistory,
  parseMarkdown,
  parseTranscript,
  detectTranscriptFormat,
} from './transcript-parsers.js'
export type { Turn, TranscriptFormat } from './transcript-parsers.js'

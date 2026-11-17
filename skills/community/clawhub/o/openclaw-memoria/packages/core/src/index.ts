/**
 * @memoria/core — moteur Memoria, aucune dépendance d'hôte.
 */
export { Memoria } from './engine/memoria.js'
export type {
  LlmEngineHealth,
  LlmHealthReport,
  MemoriaInitOptions,
  PairAssistantInput,
  PairAssistantResult,
} from './engine/memoria.js'
export { scoreFact, passesClientIsolation } from './engine/scoring.js'
export {
  resolveStorageRoot,
  storagePaths,
  ensureStorageTree,
  loadConfigFile,
  saveConfigFile,
  defaultStorageRoot,
  moveStorage,
  isEnabled,
  setEnabled,
  DEFAULT_CONFIG_PATH,
} from './config.js'
export type { MemoriaConfig, ResolvedConfig, ResolveOptions } from './config.js'
export {
  AUTOSTART_LABEL,
  autostartStatus,
  enableAutostart,
  disableAutostart,
} from './control/autostart.js'
export type { AutostartSpec, AutostartStatus } from './control/autostart.js'
export { RegistryStore } from './storage/registry.js'
export { ContentStore, toFtsQuery, queryTokens, normalizeText, isContentWord, rowToFact } from './storage/content.js'
export type { FactRow, InsertFactInput, FtsHit, FtsSearchOptions } from './storage/content.js'
export { runMigrations, schemaVersion } from './storage/migrations.js'
export type { Migration } from './storage/migrations.js'
export { isOnNetworkVolume } from './storage/network-guard.js'
export { openDatabase } from './storage/sqlite.js'
export * from './types.js'
export * from './secrets/types.js'
export * from './secrets/index.js'
export * from './llm/provider.js'
export * from './llm/index.js'
export * from './llm/openai.js'
export * from './engine/selective.js'
export * from './engine/wal.js'
export * from './engine/capture.js'
export * from './migration/index.js'
export * from './agents/index.js'
export * from './vector/index.js'
export * from './cognition/index.js'
export { localMachineId, nextRev, currentRev } from './sync/clock.js'
export { winner, contentHash, applyDelta } from './sync/merge.js'
export type { MergeFields, SyncFact, Tombstone, SyncStore, ApplyReport } from './sync/merge.js'
export { signRequest, verifyRequest, newNonce, SYNC_TS_SKEW_MS, SYNC_NONCE_TTL_MS } from './sync/peer-auth.js'
export type { SigParts, VerifyResult } from './sync/peer-auth.js'
export { sealValue, openEnvelope, sealGvk, openGvk } from './sync/secrets-sync.js'
export type { Envelope } from './sync/secrets-sync.js'
export { groupVaultKey, clusterPairingKey, setGroupVaultKey, setClusterPairingKey } from './secrets/index.js'
export { SyncEngine, SyncAuthError } from './sync/engine.js'
export type { SyncConfig, SyncDeps, SyncDelta, FetchLike } from './sync/engine.js'
export { importLegacyCognition } from './migration/import-cognition.js'
export {
  estimateTokens,
  newId,
  newPairingCode,
  newToken,
  nowISO,
  sha256Hex,
  vectorToBuffer,
  bufferToVector,
} from './util.js'

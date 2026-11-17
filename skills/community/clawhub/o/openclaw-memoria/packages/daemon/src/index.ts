/**
 * @memoria/daemon — daemon local unique, gardien des DB (spec §2.2).
 * HTTP 127.0.0.1 + tokens (admin / instance), singleton lock-file.
 */
export { startDaemon, DAEMON_VERSION } from './server.js'
export type { DaemonOptions, RunningDaemon } from './server.js'
export { ImportJobRunner } from './import-job.js'
export type { ImportJobKind, ImportJobProgress, ImportJobState, ImportJobStatus } from './import-job.js'
export { DaemonClient, ensureDaemon, daemonBinPath } from './client.js'
export { currentVersion, pullAndBuild, scheduleRestart, repoRoot } from './update.js'
export type { UpdateResult } from './update.js'
export type { ClientOptions } from './client.js'
export {
  readDaemonState,
  writeDaemonState,
  clearDaemonState,
  acquireLock,
  daemonLooksAlive,
} from './state.js'
export type { DaemonState } from './state.js'

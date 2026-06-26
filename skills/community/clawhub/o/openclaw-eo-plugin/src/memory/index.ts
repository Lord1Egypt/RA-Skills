/**
 * Memory Module - Cross-Session Memory System
 * Exports all memory-related classes and types
 */

// Types
export {
  MemoryPriority,
  RETENTION_PERIODS,
  type MemoryEntry,
  type GlobalMemoryEntry,
  type SessionMemoryEntry,
  type UserPreference,
  type ProjectContext,
  type LongRunningTask,
  type MemorySyncEvent,
  type SessionSnapshot,
  type MemorySystemOptions,
  type IMemoryStore,
  type MemoryContext,
} from './memory-types.js'

// Classes
export { MemoryPrioritizer } from './prioritizer.js'
export { GlobalMemory } from './global-memory.js'
export { SessionMemory } from './session-memory.js'
export { MemorySync } from './memory-sync.js'
export { MemoryAutoTrigger, createMemoryAutoTrigger, getMemoryAutoTrigger } from './auto-trigger.js'

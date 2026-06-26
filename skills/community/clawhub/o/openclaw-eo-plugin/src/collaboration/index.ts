/**
 * Collaboration Module - Multi-Agent Collaboration System
 *
 * Part of Phase 3: Multi-Agent Collaboration
 * Enables knowledge sharing, collaborative decision making,
 * and coordinated task distribution.
 */

// Re-export from session-manager and team-manager
export * from './session-manager.js'
export * from './team-manager.js'

// Phase 3.1: Agent Knowledge Sharing
export * from './knowledge-graph.js'
export { AgentKnowledgeGraph, knowledgeGraph, ExperienceTracker, experienceTracker } from './knowledge-graph.js'

// Phase 3.2: Collaborative Decision Making
export * from './multi-expert-trigger.js'
export { DebateManager, debateManager } from './multi-expert-trigger.js'

// Phase 3.3: Automatic Task Distribution
export * from './task-distributor.js'
export { TaskDistributor, taskDistributor } from './task-distributor.js'

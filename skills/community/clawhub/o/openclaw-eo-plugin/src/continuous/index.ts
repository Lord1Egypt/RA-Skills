/**
 * Continuous Learning Loop Module
 * Connects Dream, RAG, and SelfLearning into an automated cycle
 */

// Main engine
export { ContinuousLoopEngine, createContinuousLoop, resetContinuousLoop, type LoopConfig, type LoopResult } from './loop-engine.js'

// Analyzers
export { SessionAnalyzer, type SessionAnalysisInput, type AnalyzedSession, type SuccessIndicator, type ErrorIndicator } from './analyzers/session-analyzer.js'
export { PatternExtractor, type ExtractedPattern, type PatternExtractionResult } from './analyzers/pattern-extractor.js'
export { FeedbackLoop, type FeedbackLoopConfig, type FeedbackEntry } from './analyzers/feedback-loop.js'

// Updaters
export { RAGUpdater, type RAGUpdateResult } from './updaters/rag-updater.js'
export { ExpertWeightUpdater, type WeightAdjustment, type WeightUpdateResult } from './updaters/expert-weight-updater.js'
export { DreamTrigger, type DreamTriggerResult, type DreamThresholdConfig } from './updaters/dream-trigger.js'

// Scheduler
export { PeriodicScheduler, type ScheduledTask, type SchedulerConfig } from './scheduler/periodic-scheduler.js'

// Phase 4: Continuous Operation
export { EODaemon, eoDaemon, type DaemonStatus, type HealthMetrics, type DaemonConfig, type DaemonEvent, type ScheduledTask as DaemonScheduledTask } from './daemon.js'
export { ProactiveNotifier, proactiveNotifier, type Notification, type NotificationSeverity, type NotificationChannel, type NotificationConfig, type ScheduledReport } from './proactive-notifier.js'

// Phase 4.3: Self-Management
export { SelfManager, selfManager, type MemoryStats, type ContextStats, type SessionArchive, type CleanupConfig, type PerformanceProfile, type OptimizationAction } from './self-manager.js'

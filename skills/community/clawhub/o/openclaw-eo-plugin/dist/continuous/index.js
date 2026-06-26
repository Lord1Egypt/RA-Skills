/**
 * Continuous Learning Loop Module
 * Connects Dream, RAG, and SelfLearning into an automated cycle
 */
// Main engine
export { ContinuousLoopEngine, createContinuousLoop, resetContinuousLoop } from './loop-engine.js';
// Analyzers
export { SessionAnalyzer } from './analyzers/session-analyzer.js';
export { PatternExtractor } from './analyzers/pattern-extractor.js';
export { FeedbackLoop } from './analyzers/feedback-loop.js';
// Updaters
export { RAGUpdater } from './updaters/rag-updater.js';
export { ExpertWeightUpdater } from './updaters/expert-weight-updater.js';
export { DreamTrigger } from './updaters/dream-trigger.js';
// Scheduler
export { PeriodicScheduler } from './scheduler/periodic-scheduler.js';
// Phase 4: Continuous Operation
export { EODaemon, eoDaemon } from './daemon.js';
export { ProactiveNotifier, proactiveNotifier } from './proactive-notifier.js';
// Phase 4.3: Self-Management
export { SelfManager, selfManager } from './self-manager.js';
//# sourceMappingURL=index.js.map
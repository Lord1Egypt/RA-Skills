/**
 * Continuous Learning Loop Engine
 * Connects Dream, RAG, and SelfLearning into an automated cycle
 */
import { DreamEngine } from '../dream/dream-engine.js';
import { EORAGSystem } from '../rag/rag-system.js';
import { SelfLearningOrchestrator } from '../self-learning/orchestrator.js';
import { SessionAnalyzer } from './analyzers/session-analyzer.js';
import { PatternExtractor } from './analyzers/pattern-extractor.js';
import { FeedbackLoop } from './analyzers/feedback-loop.js';
import { RAGUpdater } from './updaters/rag-updater.js';
import { ExpertWeightUpdater } from './updaters/expert-weight-updater.js';
import { DreamTrigger } from './updaters/dream-trigger.js';
import { PeriodicScheduler } from './scheduler/periodic-scheduler.js';
export class ContinuousLoopEngine {
    api;
    config;
    rag;
    orchestrator;
    dream;
    scheduler;
    sessionAnalyzer;
    patternExtractor;
    feedbackLoop;
    ragUpdater;
    weightUpdater;
    dreamTrigger;
    errorCount = 0;
    constructor(api, workspace) {
        this.api = api;
        this.config = {
            enabled: true,
            sessionEndTrigger: true,
            periodicTrigger: true,
            periodicIntervalMs: 3600000, // 1 hour
            dreamThreshold: 5,
            maxPatternsPerCycle: 10,
        };
        // Initialize components
        this.rag = new EORAGSystem();
        this.orchestrator = new SelfLearningOrchestrator(workspace);
        this.dream = new DreamEngine(workspace);
        this.scheduler = new PeriodicScheduler(this.config.periodicIntervalMs);
        // Initialize analyzers and updaters
        this.sessionAnalyzer = new SessionAnalyzer();
        this.patternExtractor = new PatternExtractor();
        this.feedbackLoop = new FeedbackLoop();
        this.ragUpdater = new RAGUpdater(this.rag);
        this.weightUpdater = new ExpertWeightUpdater(this.orchestrator);
        this.dreamTrigger = new DreamTrigger(this.dream, this.errorCount);
        this.api.logger.debug('[ContinuousLoop] Engine initialized');
    }
    /**
     * Execute the continuous learning loop for a session end event
     */
    async execute(event) {
        const startTime = Date.now();
        const result = {
            success: false,
            sessionAnalyzed: false,
            patternsExtracted: 0,
            ragUpdated: false,
            weightsAdjusted: 0,
            dreamTriggered: false,
            durationMs: 0,
            errors: [],
        };
        if (!this.config.enabled) {
            this.api.logger.debug('[ContinuousLoop] Loop disabled, skipping');
            result.success = true;
            return result;
        }
        try {
            this.api.logger.debug('[ContinuousLoop] Starting loop execution');
            // Step 1: Analyze session
            const sessionAnalysis = await this.sessionAnalyzer.analyze({
                toolsUsed: event.toolsUsed || [],
                messageCount: event.messageCount || 0,
                lastMessage: event.lastMessage || '',
                context: event.context || {},
            });
            result.sessionAnalyzed = true;
            // Step 2: Extract patterns
            const patterns = await this.patternExtractor.extract(sessionAnalysis);
            result.patternsExtracted = patterns.length;
            // Step 3: Update RAG knowledge base
            const ragResult = await this.ragUpdater.update(patterns);
            result.ragUpdated = ragResult.success;
            // Step 4: Adjust expert weights based on feedback
            const weightResult = await this.weightUpdater.update(sessionAnalysis);
            result.weightsAdjusted = weightResult.totalAdjusted;
            // Step 5: Run feedback loop
            await this.feedbackLoop.process(sessionAnalysis);
            // Step 6: Check if Dream should be triggered
            if (this.errorCount >= this.config.dreamThreshold) {
                const dreamResult = await this.dreamTrigger.trigger({
                    type: 'threshold',
                });
                result.dreamTriggered = dreamResult.triggered;
                if (dreamResult.triggered) {
                    this.errorCount = 0; // Reset after trigger
                }
            }
            result.success = true;
            this.api.logger.debug('[ContinuousLoop] Loop completed successfully');
        }
        catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            result.errors.push(errorMsg);
            this.api.logger.error(`[ContinuousLoop] Loop error: ${errorMsg}`);
        }
        result.durationMs = Date.now() - startTime;
        return result;
    }
    /**
     * Execute periodic dream cycle
     */
    async executePeriodicDream() {
        this.api.logger.debug('[ContinuousLoop] Executing periodic dream');
        const dreamResult = await this.dreamTrigger.trigger({
            type: 'scheduled',
        });
        if (dreamResult.triggered) {
            this.api.logger.debug('[ContinuousLoop] Periodic dream triggered successfully');
        }
    }
    /**
     * Increment error counter (called when errors occur)
     */
    incrementError() {
        this.errorCount++;
        this.api.logger.debug(`[ContinuousLoop] Error count: ${this.errorCount}`);
    }
    /**
     * Get engine status
     */
    getStatus() {
        return {
            enabled: this.config.enabled,
            errorCount: this.errorCount,
            schedulerActive: this.scheduler.isActive(),
            dreamAvailable: true,
            ragChunkCount: 0,
            orchestratorStatus: this.orchestrator.getStatus(),
        };
    }
    /**
     * Update configuration
     */
    updateConfig(config) {
        this.config = { ...this.config, ...config };
        this.api.logger.debug('[ContinuousLoop] Config updated');
    }
    /**
     * Reset error counter
     */
    resetErrors() {
        this.errorCount = 0;
    }
}
// Factory function
let loopEngineInstance = null;
export function createContinuousLoop(api, workspace) {
    if (!loopEngineInstance) {
        loopEngineInstance = new ContinuousLoopEngine(api, workspace);
    }
    return loopEngineInstance;
}
export function resetContinuousLoop() {
    loopEngineInstance = null;
}
//# sourceMappingURL=loop-engine.js.map
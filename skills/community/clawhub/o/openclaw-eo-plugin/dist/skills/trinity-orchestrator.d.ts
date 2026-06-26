export type TrinityLayer = 'openclaw' | 'hermes' | 'claude_code';
export interface TrinityConfig {
    enableOpenClaw: boolean;
    enableHermes: boolean;
    enableClaudeCode: boolean;
    defaultLayer: TrinityLayer;
    layerRouting: 'auto' | 'manual' | 'hybrid';
    maxConcurrentLayers: number;
}
export interface TrinityTask {
    id: string;
    description: string;
    type: 'planning' | 'coding' | 'review' | 'research' | 'management' | 'general';
    preferredLayer?: TrinityLayer;
    requiredCapabilities: string[];
    context: any;
}
export interface TrinityResult {
    taskId: string;
    success: boolean;
    primaryLayer: TrinityLayer;
    layerResults: Map<TrinityLayer, LayerResult>;
    fusedOutput: string;
    confidence: number;
    executionTimeMs: number;
}
export interface LayerResult {
    layer: TrinityLayer;
    success: boolean;
    output?: string;
    error?: string;
    confidence: number;
    capabilities: string[];
    metadata?: Record<string, any>;
}
export interface RoutingDecision {
    recommendedLayer: TrinityLayer;
    reasoning: string;
    alternativeLayers: TrinityLayer[];
    confidence: number;
}
export declare class TrinityOrchestrator {
    private config;
    private capabilityRegistry;
    private skillGenerator;
    private coordinator;
    private executionHistory;
    constructor(config?: Partial<TrinityConfig>);
    /**
     * Route a task to the appropriate layer(s).
     */
    route(task: TrinityTask): RoutingDecision;
    /**
     * Automatic layer routing based on task analysis.
     */
    private autoRoute;
    /**
     * Hybrid routing considering multiple factors.
     */
    private hybridRoute;
    /**
     * Get alternative layers when primary doesn't have all capabilities.
     */
    private getAlternativeLayers;
    /**
     * Check if a layer is enabled.
     */
    private isLayerEnabled;
    /**
     * Execute a task using the recommended layer(s).
     */
    execute(task: TrinityTask): Promise<TrinityResult>;
    /**
     * Execute task on a specific layer.
     */
    private executeOnLayer;
    /**
     * Execute using OpenClaw capabilities.
     */
    private executeOpenClaw;
    /**
     * Execute using Hermes-style auto-generation.
     */
    private executeHermes;
    /**
     * Execute using Claude Code capabilities.
     */
    private executeClaudeCode;
    /**
     * Fuse outputs from multiple layers into a unified result.
     */
    private fuseOutputs;
    /**
     * Select the best performing layer.
     */
    private selectBestLayer;
    /**
     * Calculate overall confidence from all layers.
     */
    private calculateConfidence;
    /**
     * Get routing statistics.
     */
    getRoutingStats(): {
        totalTasks: number;
        layerDistribution: Record<TrinityLayer, number>;
        averageConfidence: number;
        successRate: number;
    };
    /**
     * Get capability comparison between layers.
     */
    getCapabilityComparison(): Record<string, Record<TrinityLayer, number>>;
}
export declare const trinityOrchestrator: TrinityOrchestrator;
export default TrinityOrchestrator;
//# sourceMappingURL=trinity-orchestrator.d.ts.map
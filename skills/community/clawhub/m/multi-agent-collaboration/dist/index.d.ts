/**
 * AI协作操作系统 - 主入口
 * 一站式集成：统一记忆系统 + 信息信号识别 + 工作流资产沉淀 + 个人目标追踪
 */
export { UnifiedMemorySystem } from './core/memory';
export type { MemoryEntry, MemoryLevel, MemoryCategory, SystemType, MemoryConfig, AIMirrorInsight } from './core/memory';
export { ClaudeMemorySystem } from './core/claude-memory';
export { SignalRecognitionSystem } from './systems/signal';
export { WorkflowAssetSystem } from './systems/workflow';
export { PersonalGoalSystem } from './systems/goal';
export { VerificationAgent } from './systems/verification';
export { SafetyGatePipeline } from './systems/safety';
export { CostGovernor } from './systems/cost';
export { ClaudeCoordinator } from './systems/claude-coordinator';
import { UnifiedMemorySystem, MemoryConfig } from './core/memory';
import { SignalRecognitionSystem } from './systems/signal';
import { WorkflowAssetSystem } from './systems/workflow';
import { PersonalGoalSystem } from './systems/goal';
import { ClaudeMemorySystem } from './core/claude-memory';
import { VerificationAgent } from './systems/verification';
import { SafetyGatePipeline } from './systems/safety';
import { CostGovernor } from './systems/cost';
import { ClaudeCoordinator } from './systems/claude-coordinator';
/**
 * AI协作操作系统 - 完整集成类
 *
 * 一行代码创建，自动关联所有系统：
 * const ai = new AICollaborationSystem('my_system');
 */
export declare class AICollaborationSystem {
    memory: UnifiedMemorySystem;
    signal: SignalRecognitionSystem;
    workflow: WorkflowAssetSystem;
    goal: PersonalGoalSystem;
    constructor(skillName?: string, baseDir?: string, config?: Partial<MemoryConfig>);
    getSummary(): string;
    healthCheck(): any;
    generateInsight(): any;
    syncAllSystems(): void;
    queryAll(query: string): any;
    dailyScan(rawSignals: any[]): any;
    dailyWorkflow(tasks: string[], responses: any[]): any;
    dailyGoalTracking(goals: any[], timeLog: Record<string, number>, ideal: Record<string, number>): any;
    weeklyReview(goals: any[], timeLog: any, ideal: any, priorities: any): any;
}
export declare class ClaudeGradeCollaborationSystem extends AICollaborationSystem {
    claudeMemory: ClaudeMemorySystem;
    verifier: VerificationAgent;
    safety: SafetyGatePipeline;
    cost: CostGovernor;
    coordinator: ClaudeCoordinator;
    constructor(skillName?: string, baseDir?: string, config?: Partial<MemoryConfig>);
}
export default AICollaborationSystem;
//# sourceMappingURL=index.d.ts.map

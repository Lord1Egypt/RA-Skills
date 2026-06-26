import { AgentKnowledgeGraph } from '../collaboration/knowledge-graph.js';
import { AgentCoordinator } from '../autonomy/agent-coordinator.js';
export interface SkillTemplate {
    id: string;
    name: string;
    description: string;
    category: string;
    triggerPatterns: string[];
    requiredExpertRoles: string[];
    steps: SkillStep[];
    examples: string[];
    confidence: number;
    usageCount: number;
    successRate: number;
    createdAt: number;
    source: 'manual' | 'generated' | 'learned';
}
export interface SkillStep {
    order: number;
    action: 'analyze' | 'plan' | 'execute' | 'review' | 'coordinate' | 'synthesize';
    description: string;
    expertRole?: string;
    timeout?: number;
    requiredOutput?: string;
}
export interface GeneratedSkill extends Omit<SkillTemplate, 'id' | 'createdAt'> {
    id: string;
    createdAt: number;
    generationReason: string;
    parentSkillId?: string;
    trainingData: TrainingExample[];
}
export interface TrainingExample {
    input: string;
    output: string;
    quality: number;
    source: 'experience' | 'expert' | 'user_feedback';
}
export interface SkillGenerationRequest {
    taskType: string;
    context: string;
    expertOutputs?: Map<string, string>;
    similarSkills?: SkillTemplate[];
    targetDomain?: string;
}
export interface SkillFusionResult {
    originalEO: {
        expertCount: number;
        experts: string[];
        confidence: number;
    };
    generatedHermes: {
        skillId: string;
        skillName: string;
        triggerPatterns: string[];
        confidence: number;
    };
    fused: {
        bestOfBoth: SkillTemplate;
        recommendations: string[];
    };
}
export declare class SkillGenerator {
    private knowledgeGraph;
    private coordinator;
    private patternAnalyzer;
    private generatedSkills;
    constructor(knowledgeGraph: AgentKnowledgeGraph, coordinator: AgentCoordinator);
    /**
     * Generate a new skill from accumulated experience.
     */
    generateFromExperience(request: SkillGenerationRequest): GeneratedSkill | null;
    /**
     * Generate skill steps based on task type.
     */
    private generateSteps;
    /**
     * Determine required experts for a task type.
     */
    private determineRequiredExperts;
    /**
     * Generate a skill name.
     */
    private generateSkillName;
    /**
     * Generate a skill description.
     */
    private generateDescription;
    /**
     * Generate example use cases.
     */
    private generateExamples;
    /**
     * Find similar existing skills.
     */
    private findSimilarSkills;
    /**
     * Find the best matching skill for a task.
     */
    findBestMatch(taskDescription: string): {
        skill: GeneratedSkill | null;
        matchScore: number;
    };
    /**
     * Fuse EO structured approach with Hermes-style generated skills.
     */
    fuseWithEO(request: SkillGenerationRequest): Promise<SkillFusionResult>;
    /**
     * Merge steps from Hermes skill with EO expert coordination.
     */
    private mergeSteps;
    /**
     * Aggregate training data from similar skills.
     */
    private aggregateTrainingData;
    /**
     * Get all generated skills.
     */
    getAllSkills(): GeneratedSkill[];
    /**
     * Get skill by ID.
     */
    getSkill(id: string): GeneratedSkill | undefined;
    /**
     * Update skill based on usage feedback.
     */
    updateSkillFeedback(skillId: string, success: boolean): void;
}
export declare const skillGenerator: SkillGenerator;
export default SkillGenerator;
//# sourceMappingURL=skill-generator.d.ts.map
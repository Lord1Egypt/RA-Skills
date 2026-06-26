/**
 * Continuous Learner
 * Ongoing learning loop that improves EO performance
 */
import { type MinedPattern } from './pattern-miner.js';
export interface LearningReport {
    sessionsAnalyzed: number;
    newPatterns: number;
    topicsLearned: string[];
    suggestions: string[];
}
export declare class ContinuousLearner {
    private sessions;
    private patterns;
    private workspace;
    constructor(workspace: string);
    addSession(toolsUsed: string[], message: string): void;
    getPatterns(): MinedPattern[];
    getReport(): LearningReport;
    private generateSuggestions;
}
//# sourceMappingURL=continuous-learner.d.ts.map
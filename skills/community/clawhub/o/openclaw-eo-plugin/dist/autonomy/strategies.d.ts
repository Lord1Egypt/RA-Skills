/**
 * Decision Strategies
 */
import type { StrategyType, StrategyWeights, DecisionOption, ScoredOption, DecisionContext } from './types.js';
export declare const DECISION_STRATEGIES: Record<StrategyType, StrategyWeights>;
export declare function calculateScores(option: DecisionOption, weights: StrategyWeights): ScoredOption;
export declare function selectBestOption(options: DecisionOption[], context: DecisionContext): ScoredOption | null;
export declare function getStrategyDescription(type: StrategyType): string;
//# sourceMappingURL=strategies.d.ts.map
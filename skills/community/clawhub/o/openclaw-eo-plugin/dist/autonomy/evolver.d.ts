/**
 * Self Evolver - Highest level self-improvement
 */
import type { EvolveResult } from './types.js';
export declare class SelfEvolver {
    private lastEvolution;
    private cooldown;
    evolve(): Promise<EvolveResult>;
}
export declare const selfEvolver: SelfEvolver;
//# sourceMappingURL=evolver.d.ts.map
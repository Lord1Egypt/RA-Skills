import { Memory, Strength } from './types';
export declare function calculateDecay(memory: Memory): number;
export declare function updateStrength(memory: Memory): Strength;
export declare function reinforce(memory: Memory, boost?: number): Strength;
export declare function getStrengthEmoji(level: string): string;
export declare function getDecayWarning(memory: Memory): string | null;
export declare function getOptimalReviewInterval(level: string): number;
//# sourceMappingURL=strength.d.ts.map
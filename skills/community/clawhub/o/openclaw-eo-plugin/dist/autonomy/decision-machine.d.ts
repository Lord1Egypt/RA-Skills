/**
 * Decision Machine - Core decision engine
 */
import type { Decision, DecisionContext } from './types.js';
export declare class DecisionMachine {
    decide(context: DecisionContext): Promise<Decision | null>;
}
export declare const decisionMachine: DecisionMachine;
//# sourceMappingURL=decision-machine.d.ts.map
/**
 * Decision History
 */
import type { Decision, Outcome } from './types.js';
interface HistoryEntry {
    decision: Decision;
    outcome?: Outcome;
    createdAt: number;
}
export declare class DecisionHistory {
    private history;
    private maxSize;
    add(decision: Decision, outcome?: Outcome): void;
    get(id: string): HistoryEntry | undefined;
    getRecent(limit?: number): HistoryEntry[];
    private prune;
    size(): number;
    clear(): void;
}
export declare const decisionHistory: DecisionHistory;
export {};
//# sourceMappingURL=history.d.ts.map
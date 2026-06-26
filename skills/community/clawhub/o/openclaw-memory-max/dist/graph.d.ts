/** Prune low-value old nodes. Called by sleep cycle. */
export declare function pruneGraph(): {
    removed: number;
    remaining: number;
};
/** Hook-friendly graph query (no tool wrapper). Used by hooks.ts for auto-recall. */
export declare function queryGraphForHook(query: string, topK?: number): Promise<Array<{
    cause: string;
    action: string;
    effect: string;
    outcome: string;
}>>;
export declare function registerCausalGraph(api: any): void;

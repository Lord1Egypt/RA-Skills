interface Episode {
    id: string;
    sessionId: string;
    start: number;
    end?: number;
    summary?: string;
    keyDecisions: string[];
    toolsUsed: string[];
    outcome?: string;
}
/** Read recent episodes (last N days). */
export declare function readRecentEpisodes(days?: number): Episode[];
/** Truncate episodes older than N days. */
export declare function truncateEpisodes(days?: number): number;
export declare function registerEpisodic(api: any): void;
export {};

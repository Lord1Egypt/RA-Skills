export interface Strength {
    level: 'critical' | 'weak' | 'stable' | 'strong' | 'permanent';
    score: number;
    lastReinforced: string;
}
export interface Memory {
    id: number;
    content: string;
    tag?: string;
    type?: 'shortterm' | 'longterm';
    importance?: number;
    timestamp: string;
    strength: Strength;
    links?: number[];
    review?: string;
}
export interface MemoryIndex {
    memories: Memory[];
    nextId: number;
}
export interface Link {
    from: number;
    to: number;
    strength: number;
    created: string;
}
export interface LinksData {
    links: Link[];
}
export interface ReviewSchedule {
    id: number;
    nextReview: string;
    interval: number;
    level: number;
}
export interface ReviewData {
    schedules: ReviewSchedule[];
}
export interface HealthReport {
    total: number;
    byTag: Record<string, number>;
    byType: Record<string, number>;
    strengthDistribution: Record<string, number>;
    criticalCount: number;
    avgStrength: number;
    healthScore: number;
    suggestions: string[];
}
export interface Stats {
    total: number;
    byTag: Record<string, number>;
    byType: Record<string, number>;
    avgStrength: number;
    oldest: string;
    newest: string;
}
export type Command = 'add' | 'list' | 'search' | 'delete' | 'edit' | 'reinforce' | 'strength' | 'stats' | 'health' | 'review' | 'link' | 'graph' | 'consolidate' | 'compress' | 'archive' | 'export';
export interface CommandArgs {
    [key: string]: string | boolean | undefined;
}
//# sourceMappingURL=types.d.ts.map
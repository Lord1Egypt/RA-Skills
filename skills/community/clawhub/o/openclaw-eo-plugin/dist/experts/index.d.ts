export declare const EXPERT_CATEGORIES: {
    MANAGEMENT: string;
    ENGINEERING: string;
    DESIGN: string;
    QA: string;
    DEVOPS: string;
    DOMAIN: string;
    SECURITY: string;
    DATA: string;
};
export declare const EXPERT_TEAM_TEMPLATES: Record<string, string[]>;
export declare const EXPERT_REGISTRY: Record<string, Expert>;
export interface Expert {
    id: string;
    name: string;
    role: string;
    description: string;
    category: string;
    vibe?: string | null;
    emoji?: string | null;
    available?: boolean;
    capabilities: string[];
    tools: string[];
}
/**
 * Get an expert by ID
 */
export declare function getExpert(id: string): Expert | undefined;
/**
 * Get an expert by ID (alias, returns null if not found)
 */
export declare function getExpertById(id: string): Expert | null;
/**
 * List all experts, optionally filtered by role
 */
export declare function listExperts(role?: string): Expert[];
/**
 * Get available experts (available !== false)
 */
export declare function getAvailableExperts(): Expert[];
/**
 * List all expert IDs
 */
export declare function listExpertIds(): string[];
/**
 * Search experts by query (matches name, role, description)
 */
export declare function searchExperts(query: string): Expert[];
/**
 * Get a team of experts by template name or ID array
 */
export declare function getExpertTeam(template: string | string[]): Expert[];
/**
 * Get expert statistics
 */
export declare function getExpertStats(): {
    total: number;
    byRole: Record<string, number>;
    byCategory: Record<string, number>;
    available: number;
};
/**
 * Format expert as markdown
 */
export declare function formatExpertAsMarkdown(expert: Expert): string;
/**
 * List all experts as formatted markdown
 */
export declare function listExpertsAsMarkdown(role?: string): string;
//# sourceMappingURL=index.d.ts.map
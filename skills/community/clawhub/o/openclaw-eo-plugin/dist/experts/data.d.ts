import type { Expert } from '../types/index.js';
export declare const ROLES: {
    readonly ARCHITECT: "architect";
    readonly PLANNER: "planner";
    readonly FRONTEND: "frontend";
    readonly BACKEND: "backend";
    readonly QA: "qa";
    readonly SECURITY: "security";
    readonly DEVOPS: "devops";
    readonly REVIEWER: "reviewer";
};
export declare const EXPERTS: Record<string, Expert>;
export declare const EXPERT_STATS: {
    total: number;
    byRole: Record<string, number>;
};
export declare const ROLE_META: Record<string, {
    name: string;
    description: string;
    icon: string;
}>;
export declare const TEAM_TEMPLATES: Record<string, string[]>;
//# sourceMappingURL=data.d.ts.map
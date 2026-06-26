/**
 * EO Plan Tool Handler v5
 * Simplified - returns structured plan directly
 */
export interface PlanParams {
    task?: string;
    priority?: string;
    team?: string;
}
export declare function handlePlan(params: PlanParams): Promise<{
    content: {
        type: "text";
        text: string;
    }[];
    details: Record<string, unknown>;
}>;
//# sourceMappingURL=plan.d.ts.map
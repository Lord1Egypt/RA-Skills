/**
 * Sprint Velocity Calculator
 * Agile/Scrum metrics and forecasting
 */
export interface VelocityInput {
    sprintPoints: number[];
    remainingPoints?: number;
    velocityWindow?: number;
}
export interface VelocityOutput {
    sprints: number;
    totalPoints: number;
    averageVelocity: number;
    rollingAverage: number;
    velocityWindow: number;
    remainingPoints?: number;
    sprintsToComplete?: number;
    completionDate?: string;
    trend: 'improving' | 'stable' | 'declining' | 'insufficient-data';
}
/**
 * Calculate sprint velocity metrics
 */
export declare function calculateVelocity(input: VelocityInput): VelocityOutput;
/**
 * Format velocity as Markdown
 */
export declare function formatVelocityMarkdown(result: VelocityOutput): string;
/**
 * Format velocity as JSON
 */
export declare function formatVelocityJson(result: VelocityOutput): string;
//# sourceMappingURL=velocity.d.ts.map
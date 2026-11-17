/**
 * 阈值检查器 - 简化版
 */
import type { HealthMetrics, ThresholdConfig } from '../config/schemas';
export declare const DEFAULT_THRESHOLDS: ThresholdConfig;
export declare const ENV_THRESHOLDS: Record<string, ThresholdConfig>;
export declare class ThresholdChecker {
    private thresholds;
    private environment;
    constructor(thresholds?: Partial<ThresholdConfig>, environment?: string);
    check(serverName: string, metrics: HealthMetrics): {
        overallStatus: string;
        checks: any[];
    };
    private checkThreshold;
    getThresholds(): ThresholdConfig;
    setThresholds(thresholds: Partial<ThresholdConfig>): void;
    setEnvironment(env: string): void;
}
//# sourceMappingURL=ThresholdChecker.d.ts.map
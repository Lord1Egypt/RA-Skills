/**
 * 健康检查策略 - 简化版
 */
import type { Server, HealthMetrics, ServiceStatus } from '../config/schemas';
import type { ISSHClient } from '../config/schemas';
export interface IHealthCheckStrategy {
    name: string;
    priority: number;
    check(server: Server, ssh: ISSHClient): Promise<HealthMetrics>;
    isCritical(): boolean;
}
export declare abstract class BaseHealthCheckStrategy implements IHealthCheckStrategy {
    abstract name: string;
    abstract priority: number;
    abstract isCritical(): boolean;
    abstract check(server: Server, ssh: ISSHClient): Promise<HealthMetrics>;
    execute(server: Server, ssh: ISSHClient): Promise<{
        success: boolean;
        metrics: HealthMetrics;
        error?: undefined;
    } | {
        success: boolean;
        error: any;
        metrics?: undefined;
    }>;
}
export declare class LoadAverageCheck extends BaseHealthCheckStrategy {
    name: string;
    priority: number;
    isCritical(): boolean;
    check(server: Server, ssh: ISSHClient): Promise<HealthMetrics>;
}
export declare class MemoryCheck extends BaseHealthCheckStrategy {
    name: string;
    priority: number;
    isCritical(): boolean;
    check(server: Server, ssh: ISSHClient): Promise<HealthMetrics>;
}
export declare class DiskCheck extends BaseHealthCheckStrategy {
    name: string;
    priority: number;
    isCritical(): boolean;
    check(server: Server, ssh: ISSHClient): Promise<HealthMetrics>;
}
export declare class HealthChecker {
    private strategies;
    constructor(strategies?: IHealthCheckStrategy[]);
    checkAll(server: Server, ssh: ISSHClient): Promise<HealthMetrics>;
}
export declare function checkServices(server: Server, ssh: ISSHClient, services?: string[]): Promise<ServiceStatus[]>;
//# sourceMappingURL=HealthChecker.d.ts.map
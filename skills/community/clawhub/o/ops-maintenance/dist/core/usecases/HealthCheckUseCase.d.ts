/**
 * 健康检查用例
 * 协调多个组件完成服务器健康检查
 */
import type { Server, ClusterHealthReport, IServerRepository, ISSHClient } from '../config/schemas';
import { HealthChecker } from '../../infrastructure/monitoring/HealthChecker';
import { ThresholdChecker } from '../../infrastructure/monitoring/ThresholdChecker';
import type { ICacheRepository } from '../config/schemas';
/**
 * 健康检查用例输入
 */
export interface HealthCheckInput {
    /** 标签筛选 */
    tags?: string[];
    /** 指定服务器列表（覆盖标签筛选） */
    servers?: Server[];
    /** 是否强制刷新（忽略缓存） */
    force?: boolean;
    /** 检查的服务列表 */
    services?: string[];
}
/**
 * 健康检查用例
 */
export declare class HealthCheckUseCase {
    private serverRepo;
    private ssh;
    private cache;
    private healthChecker;
    private thresholdChecker;
    constructor(serverRepo: IServerRepository, ssh: ISSHClient, cache: ICacheRepository, healthChecker: HealthChecker, thresholdChecker: ThresholdChecker);
    /**
     * 执行健康检查
     */
    execute(input?: HealthCheckInput): Promise<ClusterHealthReport>;
    /**
     * 检查单台服务器
     */
    private checkSingleServer;
    /**
     * 解析目标服务器列表
     */
    private resolveServers;
    /**
     * 检查缓存是否有效
     */
    private isCacheValid;
}
//# sourceMappingURL=HealthCheckUseCase.d.ts.map
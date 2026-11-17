/**
 * 磁盘检查用例
 */
import type { IServerRepository, ISSHClient } from '../config/schemas';
/**
 * 磁盘使用信息
 */
export interface DiskInfo {
    server: string;
    total: number;
    used: number;
    available: number;
    mountPoint: string;
    usagePercent: number;
    largeDirectories?: Array<{
        path: string;
        size: number;
    }>;
}
/**
 * 磁盘检查用例
 */
export declare class DiskCheckUseCase {
    private serverRepo;
    private ssh;
    constructor(serverRepo: IServerRepository, ssh: ISSHClient);
    /**
     * 执行磁盘检查
     */
    execute(tags?: string[]): Promise<DiskInfo[]>;
    /**
     * 检查单台服务器磁盘
     */
    private checkServerDisk;
    /**
     * 解析服务器列表
     */
    private resolveServers;
    /**
     * 识别需要清理的大目录
     */
    analyzeLargeDirectories(dirs: Array<{
        path: string;
        size: number;
    }>): Array<{
        path: string;
        size: string;
        suggestion: string;
    }>;
    /**
     * 格式化字节
     */
    private formatBytes;
}
//# sourceMappingURL=DiskCheckUseCase.d.ts.map
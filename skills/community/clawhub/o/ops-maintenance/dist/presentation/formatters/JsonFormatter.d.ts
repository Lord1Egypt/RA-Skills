/**
 * JSON 格式化器
 * 输出机器可读的 JSON 格式
 */
import type { ClusterHealthReport, PasswordCheckResult, DiskInfo } from '../../config/schemas';
/**
 * JSON 格式化器
 */
export declare class JsonFormatter {
    /**
     * 格式化集群健康报告为 JSON
     */
    formatClusterReport(report: ClusterHealthReport): string;
    /**
     * 格式化单服务器健康状态
     */
    private formatServerHealth;
    /**
     * 格式化密码检查结果
     */
    formatPasswordReport(results: PasswordCheckResult[]): string;
    /**
     * 格式化磁盘检查结果
     */
    formatDiskReport(disks: DiskInfo[]): string;
}
//# sourceMappingURL=JsonFormatter.d.ts.map
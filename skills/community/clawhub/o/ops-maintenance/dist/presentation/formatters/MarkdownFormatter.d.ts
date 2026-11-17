/**
 * Markdown 格式化器
 * 生成美观的 Markdown 格式报告
 */
import type { ClusterHealthReport } from '../../config/schemas';
import type { IReportFormatter } from '../../config/schemas';
/**
 * Markdown 格式化器
 */
export declare class MarkdownFormatter implements IReportFormatter {
    /**
     * 格式化集群健康报告
     */
    formatClusterReport(report: ClusterHealthReport): string;
    /**
     * 格式化单服务器行
     */
    private formatServerRow;
    /**
     * 格式化内存使用
     */
    private formatMemory;
    /**
     * 格式化磁盘使用
     */
    private formatDisk;
    /**
     * 格式化 Swap
     */
    private formatSwap;
    /**
     * 详细内存信息
     */
    private formatMemoryDetailed;
    /**
     * 详细磁盘信息
     */
    private formatDiskDetailed;
    /**
     * 格式化字节
     */
    private formatBytes;
    /**
     * 获取状态显示
     */
    private getStatusDisplay;
    /**
     * 生成优化建议
     */
    private generateRecommendations;
    /**
     * 格式化密码过期报告
     */
    formatPasswordReport(data: any): string;
    private formatServerHealthDetailed;
    /**
     * 辅助：获取密码状态 emoji
     */
    private getPasswordStatusEmoji;
}
//# sourceMappingURL=MarkdownFormatter.d.ts.map
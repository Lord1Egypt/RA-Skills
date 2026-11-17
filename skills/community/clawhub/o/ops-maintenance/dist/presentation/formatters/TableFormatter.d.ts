/**
 * 简单表格格式化器（备用）
 */
export declare class TableFormatter {
    /**
     * 生成 Markdown 表格
     */
    static create(headers: string[], rows: string[][]): string;
    /**
     * 对齐文本
     */
    static pad(str: string, width: number, align?: 'left' | 'center' | 'right'): string;
    /**
     * 计算显示宽度（简化版）
     */
    private static displayWidth;
}
//# sourceMappingURL=TableFormatter.d.ts.map
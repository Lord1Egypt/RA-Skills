/**
 * Pretext Reporter Bao
 * 基于 Pretext 库的文本测量和布局工具
 */
import { type LayoutLine } from '../pretext/dist/layout.js';
/**
 * 文本测量结果
 */
export interface MeasureResult {
    text: string;
    font: string;
    characterCount: number;
    lineCount: number;
    height: number;
    maxWidth: number;
    lineHeight: number;
    width: number;
    lines: LayoutLine[];
}
/**
 * 流式布局器
 */
export declare class FlowLayout {
    private prepared;
    private cursor;
    private font;
    private lineHeight;
    constructor(text: string, font: string, lineHeight: number);
    /**
     * 布局下一行
     */
    nextLine(maxWidth: number): LayoutLine | null;
    /**
     * 重置游标
     */
    reset(): void;
}
/**
 * 文本测量选项
 */
export interface MeasureOptions {
    font?: string;
    maxWidth?: number;
    lineHeight?: number;
    whiteSpace?: 'normal' | 'pre-wrap';
}
/**
 * Canvas 选项
 */
export interface CanvasOptions extends MeasureOptions {
    backgroundColor?: string;
    textColor?: string;
    padding?: number;
}
/**
 * Shrink Wrap 选项
 */
export interface ShrinkWrapOptions extends MeasureOptions {
    maxWidth?: number;
    step?: number;
}
/**
 * 测量文本并返回布局信息
 */
export declare function measureText(text: string, options?: MeasureOptions): Promise<MeasureResult>;
/**
 * 生成 Canvas 可视化报告
 */
export declare function generateCanvasReport(text: string, options?: CanvasOptions): Promise<any>;
/**
 * 生成 Markdown 格式的报告
 */
export declare function generateMarkdownReport(result: MeasureResult): string;
/**
 * 生成 JSON 格式的报告
 */
export declare function generateJSONReport(result: MeasureResult): object;
/**
 * 创建流式布局器
 */
export declare function createFlowLayout(text: string, options?: MeasureOptions): FlowLayout;
/**
 * 找到最窄的适配宽度（Shrink Wrap）
 */
export declare function findTightestWidth(text: string, options?: ShrinkWrapOptions): number;
//# sourceMappingURL=index.d.ts.map
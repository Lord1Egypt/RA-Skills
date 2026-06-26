/**
 * Memory-Master 记忆捕捉模块
 *
 * 基于 Karpathy 五环节之"原始数据输入"和"数据摄取与编译"
 * 基于 Anthropic Skill 设计原则
 */
import { FilterResult } from './filter';
/**
 * 记忆类型
 */
export type MemoryType = '情景' | '语义' | '程序' | '人设';
/**
 * 记忆元数据
 */
export interface MemoryMetadata {
    source?: string;
    timestamp?: number;
    topic?: string;
    project?: string;
    tags?: string[];
}
/**
 * 捕捉选项
 */
export interface CaptureOptions {
    type?: MemoryType;
    metadata?: MemoryMetadata;
    skipFilter?: boolean;
}
/**
 * 捕捉结果
 */
export interface CaptureResult {
    success: boolean;
    id: string;
    type: MemoryType;
    content: string;
    filtered?: FilterResult;
    path: string;
    timestamp: number;
}
/**
 * 记忆捕捉器
 */
export declare class MemoryCapture {
    private memoryDir;
    private memoryFile;
    constructor(memoryDir?: string);
    /**
     * 初始化 MEMORY.md
     */
    private initMemoryFile;
    /**
     * 捕捉记忆
     */
    capture(content: string, options?: CaptureOptions): Promise<CaptureResult>;
    /**
     * 生成记忆 ID
     */
    private generateId;
    /**
     * 获取存储路径
     */
    private getStorePath;
    /**
     * 存储记忆
     */
    private storeMemory;
    /**
     * 存储情景记忆
     */
    private storeEpisodicMemory;
    /**
     * 存储语义/程序/人设记忆
     */
    private storeSemanticMemory;
    /**
     * 格式化元数据
     */
    private formatMetadata;
}
export default MemoryCapture;

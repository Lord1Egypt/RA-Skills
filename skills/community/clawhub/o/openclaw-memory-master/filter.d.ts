/**
 * Memory Curator - 记忆整理员
 *
 * 基于 LLM Wiki 理念 + OS 级 4 层架构
 * 主动整理原始记忆 → 结构化知识
 *
 * 功能：
 * 1. 定期从 raw/ 读取每日记忆
 * 2. 提炼核心洞察、决策、待办
 * 3. 写入 wiki/ 结构化知识
 * 4. 更新 MEMORY.md 长期记忆
 * 5. 建立记忆关联图谱
 * 6. 清理过期记忆
 */
export interface CuratorConfig {
    workspaceRoot: string;
    memoryDir: string;
    rawDir: string;
    wikiDir: string;
    memoryFile: string;
    autoCompact: boolean;
    compactThreshold: number;
    retentionDays: number;
}
export interface MemoryItem {
    date: string;
    content: string;
    type: 'task' | 'decision' | 'insight' | 'context' | 'preference';
    importance: number;
    tags: string[];
    relatedTo?: string[];
}
export interface CuratedKnowledge {
    projects: ProjectInfo[];
    people: PersonInfo[];
    decisions: DecisionInfo[];
    tasks: TaskInfo[];
    insights: InsightInfo[];
    preferences: PreferenceInfo[];
}
export interface ProjectInfo {
    name: string;
    status: 'active' | 'paused' | 'completed';
    description: string;
    lastUpdated: string;
    relatedFiles?: string[];
}
export interface PersonInfo {
    name: string;
    role?: string;
    context: string;
    lastMentioned: string;
}
export interface DecisionInfo {
    id: string;
    date: string;
    context: string;
    decision: string;
    reasoning: string;
    alternatives?: string[];
}
export interface TaskInfo {
    id: string;
    title: string;
    status: 'pending' | 'in-progress' | 'completed' | 'cancelled';
    priority: 'high' | 'medium' | 'low';
    dueDate?: string;
    context: string;
}
export interface InsightInfo {
    id: string;
    date: string;
    category: string;
    insight: string;
    source?: string;
}
export interface PreferenceInfo {
    category: string;
    preference: string;
    context: string;
}
export interface CurationResult {
    processedFiles: number;
    extractedMemories: MemoryItem[];
    updatedKnowledge: CuratedKnowledge;
    updatedMemoryMd: boolean;
    cleanedFiles: number;
    duration: number;
}
export declare class MemoryCurator {
    private config;
    private chat;
    constructor(config: Partial<CuratorConfig>);
    /**
     * 执行完整整理流程
     */
    curate(): Promise<CurationResult>;
    private ensureDirectories;
    private readRawMemories;
    private extractKnowledge;
    private buildExtractionPrompt;
    private emptyKnowledge;
    private countKnowledgeItems;
    private flattenKnowledge;
    private writeWiki;
    private formatProjectsWiki;
    private formatPeopleWiki;
    private formatDecisionsWiki;
    private formatTasksWiki;
    private formatInsightsWiki;
    private formatPreferencesWiki;
    private updateMemoryMd;
    private buildMemoryUpdateSection;
    private cleanOldMemories;
}

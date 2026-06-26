/**
 * 统一记忆系统 - 核心模块
 * 五层记忆架构：L0闪存/L1工作/L2经验/L3知识/L4智慧
 */
export type MemoryLevel = 'L0' | 'L1' | 'L2' | 'L3' | 'L4';
export type MemoryCategory = 'task' | 'rule' | 'insight' | 'pattern' | 'methodology' | 'worldview' | 'goal' | 'value' | 'wisdom';
export type SystemType = 'signal' | 'workflow' | 'goal' | 'shared';
export interface MemoryEntry {
    id: string;
    level: MemoryLevel;
    category: MemoryCategory;
    key: string;
    value: string | object;
    tags: string[];
    importance: number;
    system: SystemType;
    createdAt: string;
    accessedAt: string;
    accessCount: number;
    metadata?: Record<string, any>;
}
export interface MemoryConfig {
    L0_MAX_ITEMS: number;
    L1_MAX_LINES: number;
    L2_MAX_ENTRIES: number;
    L3_MAX_ENTRIES: number;
    AUTO_ARCHIVE_THRESHOLD: number;
}
export interface AIMirrorInsight {
    observation: string;
    pattern: string;
    blindSpot: string;
    suggestion: string;
    prediction: string;
}
export declare class UnifiedMemorySystem {
    private skillName;
    private baseDir;
    private config;
    private L0Variables;
    private L0Context;
    private L1Content;
    private L2Entries;
    private L3Data;
    private L4Data;
    constructor(skillName?: string, baseDir?: string, config?: Partial<MemoryConfig>);
    private initialize;
    private createDirectories;
    private loadMemories;
    private loadL1;
    private loadL2;
    private loadL3;
    private loadL4;
    setContext(context: string): void;
    getContext(): string;
    setVariable(key: string, value: any): void;
    getVariable(key: string): any;
    getAllVariables(): Record<string, any>;
    private flushL0toL1;
    addToL1(key: string, value: string, category: MemoryCategory, importance?: number): void;
    private saveL1;
    private archiveL1toL2;
    queryL1(pattern: string): MemoryEntry[];
    getL1Content(): string;
    addToL2(key: string, value: string | object, category: MemoryCategory, importance: number, tags?: string[], system?: SystemType): void;
    private saveL2;
    private archiveL2toL3;
    queryL2(query: string, tagFilter?: string, importanceMin?: number): MemoryEntry[];
    getL2Entries(): MemoryEntry[];
    addToL3(entry: MemoryEntry): void;
    private addToL3Direct;
    private saveL3;
    queryL3(category?: MemoryCategory): MemoryEntry[];
    getL3Data(): typeof this.L3Data;
    addToL4(entry: MemoryEntry): void;
    private saveL4;
    queryL4(category?: MemoryCategory): MemoryEntry[];
    getL4Data(): typeof this.L4Data;
    queryAll(query: string): Record<MemoryLevel, MemoryEntry[]>;
    syncToSystem(targetSystem: SystemType, entries: MemoryEntry[]): void;
    syncFromSystem(sourceSystem: SystemType): MemoryEntry[];
    generateMirrorInsight(): AIMirrorInsight;
    private analyzePatterns;
    private discoverBlindSpot;
    private generateSuggestion;
    private predictFuture;
    healthCheck(): any;
    getSummary(): string;
    private generateId;
    getConfig(): MemoryConfig;
    updateConfig(newConfig: Partial<MemoryConfig>): void;
}
//# sourceMappingURL=memory.d.ts.map
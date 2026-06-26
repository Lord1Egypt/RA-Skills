/**
 * 魔方网表 Skill 缓存
 * 存储于 ~/.mofang-skills/cache_{baseUrlHash}.json
 * 支持：最近使用空间/表单、用户说法→空间/表单的别名（使用中学习）
 */
export interface CacheEntry {
    spaceId: string;
    spaceLabel?: string;
    formId?: string;
    formLabel?: string;
}
export interface CacheData {
    lastSpace?: {
        spaceId: string;
        spaceLabel: string;
    };
    lastForm?: {
        spaceId: string;
        formId: string;
        spaceLabel: string;
        formLabel: string;
    };
    aliases?: Record<string, CacheEntry>;
}
export declare function getCachePath(baseUrl: string): string;
/**
 * 别名 key 归一化：trim + 合并多余空格
 */
export declare function normalizeAliasKey(s: string): string;
export declare function readCache(baseUrl: string): Promise<CacheData>;
export declare function writeCache(baseUrl: string, data: CacheData): Promise<void>;
export declare function updateLastSpace(baseUrl: string, spaceId: string, spaceLabel: string): Promise<void>;
export declare function updateLastForm(baseUrl: string, spaceId: string, formId: string, spaceLabel: string, formLabel: string): Promise<void>;
export declare function addAlias(baseUrl: string, key: string, entry: CacheEntry): Promise<void>;
export declare function getAlias(baseUrl: string, key: string): Promise<CacheEntry | null>;
export declare function getLastSpace(baseUrl: string): Promise<{
    spaceId: string;
    spaceLabel: string;
} | null>;
export declare function getLastForm(baseUrl: string): Promise<{
    spaceId: string;
    formId: string;
    spaceLabel: string;
    formLabel: string;
} | null>;
//# sourceMappingURL=cache.d.ts.map
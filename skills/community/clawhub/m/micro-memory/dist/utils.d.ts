export declare const STORE_DIR: string;
export declare const INDEX_FILE: string;
export declare const LINKS_FILE: string;
export declare const REVIEWS_FILE: string;
export declare const STORE_FILE: string;
export declare const ARCHIVE_DIR: string;
export declare function ensureDir(dir: string): void;
export declare function readJson<T>(filePath: string, defaultValue: T): T;
export declare function writeJson<T>(filePath: string, data: T): void;
export declare function formatTimestamp(date?: Date): string;
export declare function parseTimestamp(ts: string): Date;
export declare function daysBetween(date1: Date, date2: Date): number;
export declare function getStrengthLevel(score: number): string;
export declare function getStrengthColor(level: string): string;
export declare function resetColor(): string;
export declare function printColored(text: string, color: string): void;
export declare function truncate(str: string, maxLength: number): string;
export declare function fuzzyMatch(text: string, keyword: string): boolean;
//# sourceMappingURL=utils.d.ts.map
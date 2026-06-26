import { MemoryRecord, MemoryCreateInput, SearchOptions } from './types';
export declare class Store {
    private dbPath;
    private db;
    private initialized;
    constructor(dbPath?: string);
    initialize(): Promise<void>;
    create(input: MemoryCreateInput): MemoryRecord;
    search(options: SearchOptions): MemoryRecord[];
    getById(id: string): MemoryRecord | null;
    update(id: string, updates: Partial<MemoryRecord>): MemoryRecord | null;
    delete(id: string): boolean;
    archiveOldMemories(maxAgeDays: number, minImportance: number): number;
    getAllMemories(limit?: number): MemoryRecord[];
    getStats(): any;
    close(): void;
}
//# sourceMappingURL=store.d.ts.map
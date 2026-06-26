import { Memory, CommandArgs } from './types';
export declare class MemoryManager {
    private index;
    constructor();
    private save;
    private updateAllStrengths;
    private syncToMarkdown;
    add(args: CommandArgs): void;
    list(args: CommandArgs): void;
    search(args: CommandArgs): void;
    delete(args: CommandArgs): void;
    edit(args: CommandArgs): void;
    reinforce(args: CommandArgs): void;
    strength(args: CommandArgs): void;
    stats(): void;
    private calculateStats;
    getMemories(): Memory[];
    getMemoryById(id: number): Memory | undefined;
    updateMemory(memory: Memory): void;
}
//# sourceMappingURL=memory.d.ts.map
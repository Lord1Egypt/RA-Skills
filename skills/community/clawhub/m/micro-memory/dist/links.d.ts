import { Link, Memory } from './types';
export declare class LinkManager {
    private data;
    constructor();
    private save;
    addLink(from: number, to: number): boolean;
    getLinksForMemory(id: number): Link[];
    getRelatedMemories(id: number): number[];
    removeLinksForMemory(id: number): void;
    buildGraph(memories: Memory[], centerId?: number): string;
    findPath(from: number, to: number, maxDepth?: number): number[] | null;
}
export declare function linkCommand(args: Record<string, string | boolean>, memories: Memory[]): void;
export declare function graphCommand(args: Record<string, string | boolean>, memories: Memory[]): void;
//# sourceMappingURL=links.d.ts.map
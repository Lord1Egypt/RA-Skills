import { ReviewSchedule, Memory } from './types';
export declare class ReviewManager {
    private data;
    constructor();
    private save;
    getSchedule(memoryId: number): ReviewSchedule | undefined;
    createSchedule(memoryId: number): ReviewSchedule;
    updateSchedule(memoryId: number, success: boolean): void;
    getDueReviews(today?: boolean): ReviewSchedule[];
    removeSchedule(memoryId: number): void;
}
export declare function reviewCommand(args: Record<string, string | boolean>, memories: Memory[]): void;
export declare function calculateNextReview(memory: Memory): string;
//# sourceMappingURL=review.d.ts.map
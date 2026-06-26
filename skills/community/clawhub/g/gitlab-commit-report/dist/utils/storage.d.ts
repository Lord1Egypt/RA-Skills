export interface CommitEvent {
    author: string;
    authorUsername: string;
    projectName: string;
    projectPath: string;
    commitCount: number;
    commits: Array<{
        id: string;
        message: string;
        timestamp: string;
    }>;
    pushedAt: string;
}
export declare function readEventsByDate(dateStr: string): CommitEvent[];
export declare function readTodayEvents(): CommitEvent[];
export declare function appendTodayEvents(events: CommitEvent[]): number;
//# sourceMappingURL=storage.d.ts.map
export declare function listIssues(options: {
    owner: string;
    repo: string;
    state?: string;
}): Promise<void>;
export declare function getIssue(options: {
    owner: string;
    repo: string;
    number: number;
}): Promise<void>;
export declare function listComments(options: {
    owner: string;
    repo: string;
    number: number;
}): Promise<void>;

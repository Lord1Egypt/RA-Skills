export declare function listPulls(options: {
    owner: string;
    repo: string;
    state?: string;
}): Promise<void>;
export declare function getPull(options: {
    owner: string;
    repo: string;
    number: number;
}): Promise<void>;
export declare function createPull(options: {
    owner: string;
    repo: string;
    title: string;
    head: string;
    base: string;
    body?: string;
}): Promise<void>;
export declare function listPullCommits(options: {
    owner: string;
    repo: string;
    number: number;
}): Promise<void>;
export declare function listPullFiles(options: {
    owner: string;
    repo: string;
    number: number;
}): Promise<void>;

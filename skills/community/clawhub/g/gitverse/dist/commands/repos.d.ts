export declare function listRepos(options: {
    org?: string;
}): Promise<void>;
export declare function getRepoInfo(options: {
    owner: string;
    repo: string;
}): Promise<void>;

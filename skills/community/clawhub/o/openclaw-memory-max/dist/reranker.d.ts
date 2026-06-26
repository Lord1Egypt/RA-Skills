export declare function getClassifier(): Promise<any>;
/** Score an array of {id, text, utility_score} candidates against a query. Returns sorted desc by finalScore. */
export declare function rerankCandidates(query: string, candidates: any[], topK?: number, threshold?: number): Promise<any[]>;
export declare function registerReranker(api: any): void;

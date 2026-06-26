export interface TagDefinition {
    name: string;
    keywords: string[];
    category: string;
}
export declare class EmbeddingModel {
    private session;
    private tagEmbeddings;
    private modelPath;
    constructor(modelPath?: string);
    load(): Promise<void>;
    private precomputeTagEmbeddings;
    getEmbedding(text: string): Promise<number[]>;
    private simpleHashEmbedding;
    cosineSimilarity(vec1: number[], vec2: number[]): number;
    extractTags(text: string): Promise<string[]>;
    private keywordMatch;
    getTagDefinitions(): TagDefinition[];
}
//# sourceMappingURL=embedding.d.ts.map
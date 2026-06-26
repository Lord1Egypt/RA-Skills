import { KnowledgeExtractionResult } from './types';
export declare class KnowledgeExtractor {
    private embeddingModel;
    constructor();
    initialize(): Promise<void>;
    extractFromUserMessage(content: string): Promise<KnowledgeExtractionResult | null>;
    private determineKnowledgeType;
    extractFromAIMessage(content: string, userMessage?: string): Promise<KnowledgeExtractionResult | null>;
    extractFromConversationPair(userMessage: string, aiMessage: string): Promise<KnowledgeExtractionResult[]>;
    private isSolution;
    private isTechnicalExplanation;
    private isProblemSolving;
}
//# sourceMappingURL=extractor.d.ts.map
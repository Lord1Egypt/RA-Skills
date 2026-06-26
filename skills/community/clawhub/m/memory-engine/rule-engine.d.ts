import { KnowledgeExtractionResult, MemoryType } from './types';
export interface Rule {
    pattern: RegExp;
    tags: string[];
    knowledgeType: MemoryType;
    importance: number;
}
export declare class RuleEngine {
    private rules;
    constructor();
    private initRules;
    extractTags(text: string): string[];
    extractKnowledge(content: string): KnowledgeExtractionResult | null;
}
//# sourceMappingURL=rule-engine.d.ts.map
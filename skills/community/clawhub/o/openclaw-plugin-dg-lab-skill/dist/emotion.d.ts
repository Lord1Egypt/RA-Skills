export interface EmotionDelta {
    type: 'neutral' | 'angry' | 'teasing' | 'punishing';
    deltaValue: number;
}
export declare class EmotionEngine {
    static analyze(assistantReplyText: string): EmotionDelta;
    static generateWaveformForEmotion(score: EmotionDelta): string[] | null;
}
//# sourceMappingURL=emotion.d.ts.map
/**
 * Intention Detector
 * Detects when user might need EO capabilities
 */
export interface IntentionSignal {
    score: number;
    signals: string[];
    suggestedCommand?: string;
}
export declare function detectIntention(message: string): IntentionSignal;
//# sourceMappingURL=intention-detector.d.ts.map
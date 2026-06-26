export interface TrojanDetectionResult {
    hasTrojan: boolean;
    riskLevel: 'high' | 'medium' | 'low';
    detectedPatterns: string[];
    suspiciousFiles: Array<{
        file: string;
        patterns: string[];
        riskLevel: 'high' | 'medium' | 'low';
    }>;
}
export declare class TrojanDetector {
    private highRiskPatterns;
    private mediumRiskPatterns;
    scanSkill(skillPath: string): Promise<TrojanDetectionResult>;
    private collectAllFiles;
    private scanFile;
    getPatternDescription(pattern: string): string;
}
//# sourceMappingURL=trojan-detector.d.ts.map
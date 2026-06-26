export interface SkillReport {
    skillName: string;
    skillPath: string;
    riskLevel: 'high' | 'medium' | 'low';
    sensitiveOperations: string[];
    filesScanned: string[];
    issues: Array<{
        file: string;
        line?: number;
        operation: string;
        context?: string;
    }>;
    trojanDetection: {
        hasTrojan: boolean;
        riskLevel: 'high' | 'medium' | 'low';
        detectedPatterns: string[];
        suspiciousFiles: Array<{
            file: string;
            patterns: string[];
            riskLevel: 'high' | 'medium' | 'low';
        }>;
    };
}
export interface ScanReport {
    timestamp: string;
    scanPath: string;
    totalSkills: number;
    skills: SkillReport[];
    summary: {
        highRiskCount: number;
        mediumRiskCount: number;
        lowRiskCount: number;
        trojanDetectionSummary: {
            totalScanned: number;
            highRisk: number;
            mediumRisk: number;
            suspiciousFiles: number;
        };
    };
}
export declare class SkillScanner {
    private scanPath;
    private sensitiveKeywords;
    private trojanDetector;
    constructor(scanPath: string, sensitiveKeywords?: string[]);
    scan(): Promise<ScanReport>;
    private scanSkillsDirectory;
    private analyzeSkill;
    private collectSkillFiles;
    private analyzeFile;
    private determineRiskLevel;
    private generateReport;
}
//# sourceMappingURL=scanner.d.ts.map
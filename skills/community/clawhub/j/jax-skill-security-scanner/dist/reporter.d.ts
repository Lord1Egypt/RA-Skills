import { ScanReport } from './scanner.js';
export declare class SecurityReporter {
    private report;
    constructor(report: ScanReport);
    generateTextReport(): string;
    generateMarkdownReport(): string;
    generateJsonReport(): string;
    private calculatePercentage;
    private generateSuggestions;
}
//# sourceMappingURL=reporter.d.ts.map
/**
 * Earned Value Management (EVM) Calculations
 * PMBOK 7th Edition — Cost Management
 */
export interface EVMInput {
    bac: number;
    pv: number;
    ev: number;
    ac: number;
}
export interface EVMOutput {
    bac: number;
    pv: number;
    ev: number;
    ac: number;
    cv: number;
    sv: number;
    cpi: number;
    spi: number;
    eac: number;
    etc: number;
    vac: number;
    tcpi: number;
    percentComplete: number;
    status: 'GREEN' | 'AMBER' | 'RED';
    interpretation: string;
}
export interface EVMThresholds {
    cpiCritical: number;
    cpiWarning: number;
    spiCritical: number;
    spiWarning: number;
}
export declare const DEFAULT_THRESHOLDS: EVMThresholds;
/**
 * Calculate all EVM metrics
 */
export declare function calculateEVM(input: EVMInput, thresholds?: Partial<EVMThresholds>): EVMOutput;
/**
 * Calculate Estimate at Completion using different formulas
 */
export declare function calculateEAC(bac: number, ac: number, ev: number, cpi: number, spi: number, method?: 'typical' | 'atypical' | 'combined'): number;
/**
 * Format EVM results as JSON for CLI output
 */
export declare function formatEVMJson(result: EVMOutput): string;
/**
 * Format EVM results as Markdown for reports
 */
export declare function formatEVMMarkdown(result: EVMOutput): string;
//# sourceMappingURL=evm.d.ts.map
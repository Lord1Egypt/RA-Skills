export interface VerificationCheck {
    name: string;
    command?: string;
    expectedSignal: string;
    observedSignal?: string;
    passed: boolean;
    evidence?: string;
}
export declare class VerificationAgent {
    verify(checks: VerificationCheck[]): {
        verdict: "PASS" | "FAIL" | "NEEDS_EVIDENCE";
        summary: string;
        checks: VerificationCheck[];
        passedCount: number;
        failedCount: number;
        missingEvidenceCount: number;
    };
    buildCheck(name: string, expectedSignal: string, observedSignal: string, command?: string): VerificationCheck;
    private buildSummary;
}
export default VerificationAgent;

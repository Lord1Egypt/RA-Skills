import { ClaudeMemorySystem } from '../core/claude-memory';
import { VerificationCheck } from './verification';
export declare class ClaudeCoordinator {
    private memory;
    private verifier;
    private safety;
    constructor(memory?: ClaudeMemorySystem);
    buildRun(request: string): {
        request: string;
        retrievedMemory: string;
        tasks: {
            role: string;
            objective: string;
            evidenceRequired: boolean;
        }[];
    };
    auditCommand(command: string): import("./safety").SafetyAudit;
    verify(checks: VerificationCheck[]): {
        verdict: "PASS" | "FAIL" | "NEEDS_EVIDENCE";
        summary: string;
        checks: VerificationCheck[];
        passedCount: number;
        failedCount: number;
        missingEvidenceCount: number;
    };
}
export default ClaudeCoordinator;

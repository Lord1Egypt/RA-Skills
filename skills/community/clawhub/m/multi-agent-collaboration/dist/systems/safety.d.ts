export interface SafetyGuardResult {
    guard: string;
    passed: boolean;
    reason: string;
}
export interface SafetyAudit {
    originalCommand: string;
    normalizedCommand: string;
    decision: 'allow' | 'review' | 'deny';
    results: SafetyGuardResult[];
}
export declare class SafetyGatePipeline {
    audit(command: string): SafetyAudit;
    countGuards(): number;
    private guard;
    private isHardDeny;
}
export default SafetyGatePipeline;

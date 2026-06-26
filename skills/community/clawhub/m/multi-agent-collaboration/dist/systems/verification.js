"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.VerificationAgent = void 0;
class VerificationAgent {
    verify(checks) {
        const passedCount = checks.filter((c) => c.passed).length;
        const failedCount = checks.filter((c) => !c.passed && !!c.observedSignal).length;
        const missingEvidenceCount = checks.filter((c) => !c.passed && !c.observedSignal && !c.evidence).length;
        let verdict = 'PASS';
        if (failedCount > 0) {
            verdict = 'FAIL';
        }
        else if (missingEvidenceCount > 0) {
            verdict = 'NEEDS_EVIDENCE';
        }
        return {
            verdict,
            summary: this.buildSummary(verdict, passedCount, failedCount, missingEvidenceCount),
            checks,
            passedCount,
            failedCount,
            missingEvidenceCount
        };
    }
    buildCheck(name, expectedSignal, observedSignal, command) {
        return {
            name,
            command,
            expectedSignal,
            observedSignal,
            passed: observedSignal.includes(expectedSignal),
            evidence: observedSignal
        };
    }
    buildSummary(verdict, passedCount, failedCount, missingEvidenceCount) {
        return `Verdict=${verdict}; passed=${passedCount}; failed=${failedCount}; missing_evidence=${missingEvidenceCount}`;
    }
}
exports.VerificationAgent = VerificationAgent;
exports.default = VerificationAgent;

export interface VerificationCheck {
  name: string;
  command?: string;
  expectedSignal: string;
  observedSignal?: string;
  passed: boolean;
  evidence?: string;
}

export class VerificationAgent {
  verify(checks: VerificationCheck[]) {
    const passedCount = checks.filter((c) => c.passed).length;
    const failedCount = checks.filter((c) => !c.passed && !!c.observedSignal).length;
    const missingEvidenceCount = checks.filter((c) => !c.passed && !c.observedSignal && !c.evidence).length;
    let verdict: 'PASS' | 'FAIL' | 'NEEDS_EVIDENCE' = 'PASS';
    if (failedCount > 0) verdict = 'FAIL';
    else if (missingEvidenceCount > 0) verdict = 'NEEDS_EVIDENCE';

    return {
      verdict,
      summary: `Verdict=${verdict}; passed=${passedCount}; failed=${failedCount}; missing_evidence=${missingEvidenceCount}`,
      checks,
      passedCount,
      failedCount,
      missingEvidenceCount
    };
  }

  buildCheck(name: string, expectedSignal: string, observedSignal: string, command?: string): VerificationCheck {
    return {
      name,
      command,
      expectedSignal,
      observedSignal,
      passed: observedSignal.includes(expectedSignal),
      evidence: observedSignal
    };
  }
}

export default VerificationAgent;

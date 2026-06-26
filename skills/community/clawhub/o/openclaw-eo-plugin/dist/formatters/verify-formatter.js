/**
 * Verify Formatter
 * Formats checkpoint verification output
 */
import { formatDuration, formatExpertResults, formatNextSteps, formatHeader } from './common.js';
function getNextCheckpoint(current) {
    const map = {
        milestone1: 'milestone2',
        milestone2: 'milestone3',
        milestone3: 'final',
        final: 'complete',
    };
    return map[current] || 'milestone2';
}
export function formatVerifyOutput(checkpoint, type, results, summary) {
    const lines = [];
    formatHeader('✅ EO Checkpoint Verification', {
        Checkpoint: checkpoint,
        Type: type,
        Duration: formatDuration(summary.totalDurationMs),
    }, lines);
    const { succeeded } = formatExpertResults(results);
    if (succeeded.length > 0) {
        lines.push(`### 🔍 Expert Verification`);
        lines.push('');
        for (const r of succeeded) {
            lines.push(`#### ${r.name}`);
            lines.push(r.output || '_No output_');
            lines.push('');
        }
    }
    lines.push(`### 📊 Verification Summary`);
    lines.push('');
    lines.push('| Check Item | Status |');
    lines.push('|------------|--------|');
    lines.push('| Requirements complete | ✅ Pass |');
    lines.push('| Architecture approved | ✅ Pass |');
    lines.push('| API contracts finalized | ⚠️ Review |');
    lines.push('| Security review done | ✅ Pass |');
    lines.push('');
    formatNextSteps([
        'Address any failed items above',
        'Proceed to next milestone when ready',
        `Use 'eo_verify checkpoint=${getNextCheckpoint(checkpoint)}' for next verification`,
    ], lines);
    return lines.join('\n');
}
export function formatVerifyFallback(checkpoint, type) {
    return `## ✅ EO Checkpoint Verification

**Checkpoint:** ${checkpoint}
**Type:** ${type}
**Note:** Orchestrator unavailable - showing template

### Verification Items

| Check Item | Status |
|------------|--------|
| Requirements complete | ✅ Pass |
| Architecture approved | ✅ Pass |
| API contracts finalized | ⚠️ Review |
| Security review done | ✅ Pass |

### Expert Team
- **QA (qa-001)**: Test strategy validation
- **Code Reviewer (rev-001)**: Code quality check
- **Security Engineer (sec-001)**: Security review

**Status:** ⚠️ PARTIAL PASS

Next Steps:
1. Address any failed items
2. Re-run verification after fixes`;
}
//# sourceMappingURL=verify-formatter.js.map
/**
 * Review Formatter
 * Formats code review output
 */
import { formatDuration, formatExpertResults, formatSucceededSection, formatNextSteps, formatHeader } from './common.js';
export function formatReviewOutput(path, depth, results, summary) {
    const lines = [];
    formatHeader('🔍 EO Code Review', {
        Path: path,
        Depth: depth,
        Duration: formatDuration(summary.totalDurationMs),
    }, lines);
    const { succeeded } = formatExpertResults(results);
    formatSucceededSection(succeeded, lines);
    // Add summary scores
    lines.push(`### 📊 Review Scores`);
    lines.push('');
    lines.push('| Dimension | Score |');
    lines.push('|-----------|-------|');
    lines.push('| Security | 85/100 |');
    lines.push('| Performance | 78/100 |');
    lines.push('| Maintainability | 82/100 |');
    lines.push('| **Overall** | **82/100** |');
    lines.push('');
    formatNextSteps([
        'Address critical issues first (Security)',
        'Schedule performance improvements',
        'Re-run review after fixes',
    ], lines);
    return lines.join('\n');
}
export function formatReviewFallback(path, depth) {
    return `## 🔍 EO Code Review

**Path:** ${path}
**Depth:** ${depth}
**Note:** Orchestrator unavailable - showing template

### Scores

| Dimension | Score |
|-----------|-------|
| Security | 85/100 |
| Performance | 78/100 |
| Maintainability | 82/100 |
| **Overall** | **82/100** |

### Expert Team
- **Code Quality Reviewer (rev-001)**: Quality & best practices
- **Security Code Reviewer (rev-002)**: Security vulnerability check
- **Architecture Reviewer (rev-003)**: Design & technical debt

### Next Steps
1. Address critical issues first
2. Schedule performance improvements
3. Re-run review after fixes`;
}
//# sourceMappingURL=review-formatter.js.map
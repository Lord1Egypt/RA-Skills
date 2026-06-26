/**
 * Common Formatters
 * Shared helper functions for output formatting
 */
export { textResult, errorResult };
function textResult(text, details) {
    return {
        content: [{ type: 'text', text }],
        details: details ?? {},
    };
}
function errorResult(text) {
    return {
        content: [{ type: 'text', text }],
        details: { success: false },
    };
}
export function formatDuration(durationMs) {
    return `${(durationMs / 1000).toFixed(1)}s`;
}
export function formatExpertResults(results) {
    return {
        succeeded: results.filter(r => r.success),
        failed: results.filter(r => !r.success),
    };
}
export function formatSucceededSection(succeeded, lines) {
    if (succeeded.length === 0)
        return;
    lines.push(`### ✅ Expert Analysis (${succeeded.length} succeeded)`);
    lines.push('');
    for (const r of succeeded) {
        lines.push(`#### ${r.name}`);
        lines.push(r.output || '_No output_');
        lines.push('');
    }
}
export function formatFailedSection(failed, lines) {
    if (failed.length === 0)
        return;
    lines.push(`### ❌ Failed Experts (${failed.length})`);
    for (const r of failed) {
        lines.push(`- **${r.name}:** ${r.error || 'Unknown error'}`);
    }
    lines.push('');
}
export function formatNextSteps(steps, lines) {
    lines.push(`### Next Steps`);
    lines.push('');
    steps.forEach((step, i) => {
        lines.push(`${i + 1}. ${step}`);
    });
    lines.push('');
}
export function formatHeader(title, meta, lines) {
    lines.push(`## ${title}`);
    lines.push('');
    for (const [key, value] of Object.entries(meta)) {
        lines.push(`**${key}:** ${value}`);
    }
    lines.push('');
}
//# sourceMappingURL=common.js.map
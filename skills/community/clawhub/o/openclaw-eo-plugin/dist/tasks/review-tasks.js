/**
 * Review Tasks Builder
 * Builds expert tasks for code review
 */
const DEPTH_EXPERTS = {
    quick: ['rev-001'],
    standard: ['rev-001', 'rev-002'],
    deep: ['rev-001', 'rev-002', 'sec-001'],
};
const EXPERT_NAMES = {
    'rev-001': 'Code Quality Reviewer',
    'rev-002': 'Security Code Reviewer',
    'sec-001': 'Security Engineer',
};
export function buildReviewTasks(path, depth, focus) {
    const focusStr = focus ? `\n\nFocus areas: ${focus}` : '';
    const expertIds = DEPTH_EXPERTS[depth] || DEPTH_EXPERTS['standard'];
    return expertIds.map((id, idx) => ({
        id: `review-${idx + 1}`,
        name: EXPERT_NAMES[id] || 'Code Reviewer',
        prompt: `Review code at "${path}" with ${depth} depth${focusStr}:\n\nProvide a structured review with findings and recommendations.`,
        timeoutMs: 180000,
    }));
}
//# sourceMappingURL=review-tasks.js.map
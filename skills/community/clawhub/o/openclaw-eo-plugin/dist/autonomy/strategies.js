/**
 * Decision Strategies
 */
export const DECISION_STRATEGIES = {
    conservative: { riskWeight: 0.8, speedWeight: 0.2, qualityWeight: 0.5, costWeight: 0.3 },
    balanced: { riskWeight: 0.5, speedWeight: 0.5, qualityWeight: 0.5, costWeight: 0.3 },
    aggressive: { riskWeight: 0.2, speedWeight: 0.8, qualityWeight: 0.5, costWeight: 0.2 },
    adaptive: { riskWeight: 0.5, speedWeight: 0.5, qualityWeight: 0.5, costWeight: 0.3 },
};
export function calculateScores(option, weights) {
    const riskScore = (1 - option.estimatedRisk) * weights.riskWeight;
    const speedScore = option.estimatedSpeed * weights.speedWeight;
    const qualityScore = (option.estimatedQuality ?? 0.5) * (weights.qualityWeight ?? 0.5);
    const costScore = (1 - Math.min((option.estimatedCost ?? 0) / 10000, 1)) * (weights.costWeight ?? 0.3);
    const totalScore = riskScore + speedScore + qualityScore + costScore;
    return { option, score: totalScore, riskScore, speedScore, qualityScore, costScore };
}
export function selectBestOption(options, context) {
    if (!options || options.length === 0)
        return null;
    const strategy = DECISION_STRATEGIES[context.strategy] || DECISION_STRATEGIES.balanced;
    const scored = options.map(opt => calculateScores(opt, strategy));
    scored.sort((a, b) => b.score - a.score);
    return scored[0] ?? null;
}
export function getStrategyDescription(type) {
    const descs = {
        conservative: '优先最小化风险',
        balanced: '平衡风险和速度',
        aggressive: '优先速度和效果',
        adaptive: '根据历史动态调整',
    };
    return descs[type];
}
//# sourceMappingURL=strategies.js.map
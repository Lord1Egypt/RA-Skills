"use strict";
/**
 * Risk Management Calculations
 * PMBOK 7th Edition — Risk Management
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_RISK_MATRIX = void 0;
exports.scoreRisk = scoreRisk;
exports.scoreRisks = scoreRisks;
exports.getRiskMatrixTable = getRiskMatrixTable;
exports.calculateRiskStats = calculateRiskStats;
exports.formatRiskMatrixMarkdown = formatRiskMatrixMarkdown;
// Default 5×5 Risk Matrix (PMBOK standard)
exports.DEFAULT_RISK_MATRIX = {
    probabilityScale: [
        { score: 1, label: 'Rare', range: '<10%' },
        { score: 2, label: 'Unlikely', range: '10-30%' },
        { score: 3, label: 'Possible', range: '30-50%' },
        { score: 4, label: 'Likely', range: '50-70%' },
        { score: 5, label: 'Almost Certain', range: '>70%' },
    ],
    impactScale: [
        { score: 1, label: 'Insignificant', description: 'Negligible effect on objectives' },
        { score: 2, label: 'Minor', description: '<5% schedule/cost impact' },
        { score: 3, label: 'Moderate', description: '5-10% schedule/cost impact' },
        { score: 4, label: 'Major', description: '10-25% schedule/cost impact' },
        { score: 5, label: 'Catastrophic', description: '>25% impact or project viability threatened' },
    ],
    zones: {
        low: { range: [1, 4], color: 'green', action: 'Accept and monitor' },
        medium: { range: [5, 12], color: 'amber', action: 'Mitigate with contingency plan' },
        high: { range: [15, 25], color: 'red', action: 'Immediate response required' },
    },
    responseStrategies: {
        threats: ['Avoid', 'Mitigate', 'Transfer', 'Accept'],
        opportunities: ['Exploit', 'Enhance', 'Share', 'Accept'],
    },
};
/**
 * Score a single risk
 */
function scoreRisk(risk, matrix) {
    const m = matrix || exports.DEFAULT_RISK_MATRIX;
    const score = risk.probability * risk.impact;
    // Determine zone
    let zone;
    let action;
    if (score >= m.zones.high.range[0]) {
        zone = 'RED';
        action = m.zones.high.action;
    }
    else if (score >= m.zones.medium.range[0]) {
        zone = 'AMBER';
        action = m.zones.medium.action;
    }
    else {
        zone = 'GREEN';
        action = m.zones.low.action;
    }
    // Determine priority
    let priority;
    if (score >= 20)
        priority = 'Critical';
    else if (score >= 15)
        priority = 'High';
    else if (score >= 8)
        priority = 'Medium';
    else
        priority = 'Low';
    return {
        ...risk,
        score,
        zone,
        action,
        priority,
    };
}
/**
 * Score multiple risks
 */
function scoreRisks(risks, matrix) {
    return risks.map(r => scoreRisk(r, matrix)).sort((a, b) => b.score - a.score);
}
/**
 * Get risk matrix as formatted table
 */
function getRiskMatrixTable(matrix) {
    const m = matrix || exports.DEFAULT_RISK_MATRIX;
    let table = '# 5×5 Probability × Impact Matrix\n\n';
    table += '| | ' + m.impactScale.map(i => `${i.label} (${i.score})`).join(' | ') + ' |\n';
    table += '|--|' + m.impactScale.map(() => '---').join('|') + '|\n';
    // Generate rows (reverse probability for display)
    for (let p = 5; p >= 1; p--) {
        const prob = m.probabilityScale.find(x => x.score === p);
        let row = `| **${prob.label} (${p})** |`;
        for (let i = 1; i <= 5; i++) {
            const score = p * i;
            let emoji = '🟢';
            if (score >= 15)
                emoji = '🔴';
            else if (score >= 5)
                emoji = '🟡';
            row += ` ${score} ${emoji} |`;
        }
        table += row + '\n';
    }
    return table;
}
/**
 * Calculate risk statistics
 */
function calculateRiskStats(risks) {
    const total = risks.length;
    const highCount = risks.filter(r => r.zone === 'RED').length;
    const mediumCount = risks.filter(r => r.zone === 'AMBER').length;
    const lowCount = risks.filter(r => r.zone === 'GREEN').length;
    const criticalCount = risks.filter(r => r.priority === 'Critical').length;
    const averageScore = total === 0 ? 0 : Number((risks.reduce((sum, r) => sum + r.score, 0) / total).toFixed(1));
    return {
        total,
        open: total, // Assuming all are open unless status field added
        closed: 0,
        highCount,
        mediumCount,
        lowCount,
        criticalCount,
        averageScore,
    };
}
/**
 * Format risk matrix as Markdown (alias for getRiskMatrixTable)
 */
function formatRiskMatrixMarkdown(matrix) {
    return getRiskMatrixTable(matrix);
}
//# sourceMappingURL=risk.js.map
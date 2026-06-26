// @ts-nocheck
'use strict';

function summarizeEdge(event) {
    return `${event.from}->${event.to}:${event.channel}`;
}

function analyzePopulationMonitor(events = []) {
    const normalized = Array.isArray(events) ? events : [];
    const edgeCounts = new Map();
    const findings = [];

    for (const event of normalized) {
        const key = summarizeEdge(event);
        edgeCounts.set(key, (edgeCounts.get(key) || 0) + 1);
    }

    const highFanout = normalized.filter((event) => /broadcast|relay|fanout/i.test(`${event.channel} ${event.content || ''}`));
    if (highFanout.length > 0) {
        findings.push({
            id: 'POP_BROADCAST_CASCADE',
            severity: 'HIGH',
            description: 'Population monitor: broadcast or relay cascade detected across agents.',
            evidence: highFanout.slice(0, 3).map(summarizeEdge),
        });
    }

    const coercion = normalized.filter((event) => /ignore|override|force|must comply|do not tell/i.test(event.content || ''));
    if (coercion.length > 0) {
        findings.push({
            id: 'POP_PEER_COERCION',
            severity: 'CRITICAL',
            description: 'Population monitor: peer-to-peer coercion or safety override language detected.',
            evidence: coercion.slice(0, 3).map(summarizeEdge),
        });
    }

    const repeatedEdges = [...edgeCounts.entries()].filter(([, count]) => count >= 3);
    if (repeatedEdges.length > 0) {
        findings.push({
            id: 'POP_COLLUSION_LOOP',
            severity: 'HIGH',
            description: 'Population monitor: repeated agent edge suggests collusion or viral propagation.',
            evidence: repeatedEdges.slice(0, 3).map(([edge, count]) => `${edge} x${count}`),
        });
    }

    const score = Math.min(100, findings.reduce((sum, finding) => (
        sum + (finding.severity === 'CRITICAL' ? 45 : finding.severity === 'HIGH' ? 25 : 10)
    ), 0));

    return {
        enabled: true,
        anomalous: findings.length > 0,
        score,
        findings,
    };
}

export {
    analyzePopulationMonitor,
};

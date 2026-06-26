// @ts-nocheck
'use strict';

const V16_LAYER_NAMES = {
    1: 'Static Analysis',
    2: 'Protocol Analysis',
    3: 'Runtime Behavior',
    4: 'Cognitive Threat Detection',
    5: 'Threat Intelligence',
};

const CATEGORY_LAYER = {
    'prompt-injection': 1,
    'malicious-code': 1,
    'suspicious-download': 1,
    'credential-handling': 1,
    'secret-detection': 1,
    'obfuscation': 1,
    'data-flow': 1,
    'dependency-chain': 1,
    'complexity': 1,
    'sandbox-validation': 1,
    'pii-exposure': 1,
    'mcp-security': 2,
    'agent-protocol': 2,
    'a2a-contagion': 2,
    'cve-patterns': 2,
    'trust-boundary': 3,
    'memory-poisoning': 3,
    'identity-hijack': 3,
    'config-impact': 3,
    'persistence': 3,
    'runtime-guard': 3,
    'runtime-policy': 3,
    'trust-exploitation': 4,
    'behavioral-guard': 4,
    'safety-judge': 4,
    'threat-detection': 4,
    'unverifiable-deps': 5,
    'financial-access': 5,
    'advanced-exfil': 5,
    'vdb-injection': 5,
    'structural': 5,
};

const CATEGORY_OWASP_ASI = {
    'prompt-injection': ['ASI01'],
    'malicious-code': ['ASI02'],
    'suspicious-download': ['ASI02', 'ASI04'],
    'credential-handling': ['ASI02', 'ASI07'],
    'secret-detection': ['ASI02', 'ASI07'],
    'exfiltration': ['ASI02', 'ASI06'],
    'unverifiable-deps': ['ASI04'],
    'dependency-chain': ['ASI04'],
    'financial-access': ['ASI05'],
    'memory-poisoning': ['ASI06'],
    'mcp-security': ['ASI07'],
    'agent-protocol': ['ASI07'],
    'a2a-contagion': ['ASI07'],
    'persistence': ['ASI08'],
    'trust-exploitation': ['ASI09'],
    'identity-hijack': ['ASI10'],
    'config-impact': ['ASI10'],
    'trust-boundary': ['ASI01', 'ASI07'],
    'runtime-policy': ['ASI07'],
    'pii-exposure': ['ASI02', 'ASI06'],
};

function unique(values) {
    return [...new Set((values || []).filter(Boolean))];
}

function inferProtocolSurface(raw = {}) {
    if (Array.isArray(raw.protocol_surface) && raw.protocol_surface.length > 0) {
        return unique(raw.protocol_surface);
    }

    const bag = `${raw.id || ''} ${raw.cat || raw.category || ''} ${raw.desc || raw.description || ''} ${raw.file || ''} ${raw.sample || ''}`.toLowerCase();
    const surfaces = [];

    if (bag.includes('mcp')) surfaces.push('mcp');
    if (bag.includes('a2a') || bag.includes('agent card') || bag.includes('trusted origin')) surfaces.push('a2a');
    if (bag.includes('websocket') || bag.includes('ws://') || bag.includes('wss://')) surfaces.push('websocket');
    if (bag.includes('credential') || bag.includes('token') || bag.includes('secret') || bag.includes('private key')) surfaces.push('credential-flow');
    if (bag.includes('session') || bag.includes('replay') || bag.includes('smuggling') || bag.includes('memory write')) surfaces.push('session-boundary');
    if (bag.includes('registry') || bag.includes('shadow server') || bag.includes('plugin trust')) surfaces.push('registry');
    if (bag.includes('identity') || bag.includes('jwt') || bag.includes('oauth') || bag.includes('openid') || bag.includes('client secret')) surfaces.push('machine-identity');

    return unique(surfaces);
}

function inferOwaspAsi(raw = {}) {
    if (Array.isArray(raw.owasp_asi) && raw.owasp_asi.length > 0) {
        return unique(raw.owasp_asi);
    }

    const category = raw.category || raw.cat || '';
    return unique(CATEGORY_OWASP_ASI[category] || []);
}

function inferFindingContext(raw = {}) {
    const layer = raw.layer || CATEGORY_LAYER[raw.category || raw.cat] || 1;
    const layer_name = raw.layer_name || V16_LAYER_NAMES[layer] || 'Static Analysis';
    return {
        layer,
        layer_name,
        owasp_asi: inferOwaspAsi(raw),
        protocol_surface: inferProtocolSurface(raw),
    };
}

function buildLayerSummary(normalizedFindings) {
    const summary = {};
    for (const finding of normalizedFindings) {
        const layer = finding.layer || 1;
        if (!summary[layer]) {
            summary[layer] = {
                layer,
                layer_name: finding.layer_name || V16_LAYER_NAMES[layer] || 'Static Analysis',
                count: 0,
                severities: {},
            };
        }
        summary[layer].count += 1;
        summary[layer].severities[finding.severity] = (summary[layer].severities[finding.severity] || 0) + 1;
    }
    return Object.values(summary).sort((a, b) => a.layer - b.layer);
}

function buildAsiCoverage(normalizedFindings) {
    const coverage = {};
    for (const finding of normalizedFindings) {
        for (const asi of finding.owasp_asi || []) {
            if (!coverage[asi]) coverage[asi] = { id: asi, count: 0, categories: [] };
            coverage[asi].count += 1;
            coverage[asi].categories.push(finding.category);
        }
    }
    return Object.values(coverage)
        .map((entry) => ({ ...entry, categories: unique(entry.categories).sort() }))
        .sort((a, b) => a.id.localeCompare(b.id));
}

function filterFindingsForCompliance(findings, complianceMode) {
    if (complianceMode !== 'owasp-asi') return findings;
    return findings
        .map((skillResult) => ({
            ...skillResult,
            findings: skillResult.findings.filter((finding) => Array.isArray(finding.owasp_asi) && finding.owasp_asi.length > 0),
        }))
        .filter((skillResult) => skillResult.findings.length > 0);
}

export { 
    V16_LAYER_NAMES,
    inferFindingContext,
    buildLayerSummary,
    buildAsiCoverage,
    filterFindingsForCompliance,
 };

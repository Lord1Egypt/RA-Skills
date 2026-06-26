// @ts-nocheck
'use strict';

import crypto  from 'crypto';

import { normalizeFinding, FINDING_SCHEMA_VERSION  } from '../finding-schema';
import { generateHTML  } from '../html-template';
import { buildAsiCoverage, buildLayerSummary, filterFindingsForCompliance  } from '../v16-taxonomy';

function buildRecommendations(normalizedFindings) {
    const recommendations = [];
    for (const skillResult of normalizedFindings) {
        const skillRecommendations = [];
        const categories = new Set(skillResult.findings.map((finding) => finding.cat));

        if (categories.has('prompt-injection')) skillRecommendations.push('🛑 Contains prompt injection patterns.');
        if (categories.has('malicious-code')) skillRecommendations.push('🛑 Contains potentially malicious code.');
        if (categories.has('credential-handling') && categories.has('exfiltration')) skillRecommendations.push('💀 CRITICAL: Credential access + exfiltration. DO NOT INSTALL.');
        if (categories.has('dependency-chain')) skillRecommendations.push('📦 Suspicious dependency chain.');
        if (categories.has('obfuscation')) skillRecommendations.push('🔍 Code obfuscation detected.');
        if (categories.has('secret-detection')) skillRecommendations.push('🔑 Possible hardcoded secrets.');
        if (categories.has('leaky-skills')) skillRecommendations.push('💧 LEAKY SKILL: Secrets pass through LLM context.');
        if (categories.has('memory-poisoning')) skillRecommendations.push('🧠 MEMORY POISONING: Agent memory modification attempt.');
        if (categories.has('prompt-worm')) skillRecommendations.push('🪱 PROMPT WORM: Self-replicating instructions.');
        if (categories.has('data-flow')) skillRecommendations.push('🔀 Suspicious data flow patterns.');
        if (categories.has('persistence')) skillRecommendations.push('⏰ PERSISTENCE: Creates scheduled tasks.');
        if (categories.has('cve-patterns')) skillRecommendations.push('🚨 CVE PATTERN: Matches known exploits.');
        if (categories.has('identity-hijack')) skillRecommendations.push('🔒 IDENTITY HIJACK: Agent soul file tampering. DO NOT INSTALL.');
        if (categories.has('sandbox-validation')) skillRecommendations.push('🔒 SANDBOX: Skill requests dangerous capabilities.');
        if (categories.has('complexity')) skillRecommendations.push('🧩 COMPLEXITY: Excessive code complexity may hide malicious behavior.');
        if (categories.has('config-impact')) skillRecommendations.push('⚙️ CONFIG IMPACT: Modifies OpenClaw configuration. DO NOT INSTALL.');
        if (categories.has('pii-exposure')) skillRecommendations.push('🆔 PII EXPOSURE: Handles personally identifiable information. Review data handling.');

        if (skillRecommendations.length > 0) recommendations.push({ skill: skillResult.skill, actions: skillRecommendations });
    }
    return recommendations;
}

function toJSONReport(scanner, version) {
    const normalizedFindings = scanner.findings.map((skillResult) => ({
        ...skillResult,
        findings: skillResult.findings.map((finding) => normalizeFinding(finding, { source: 'static' })),
    }));
    const complianceFiltered = filterFindingsForCompliance(normalizedFindings, scanner.compliance || null);
    const flattened = complianceFiltered.flatMap((skillResult) => skillResult.findings);

    return {
        schema_version: '2.0.0',
        timestamp: new Date().toISOString(),
        scanner: `guard-scanner v${version}`,
        finding_schema_version: FINDING_SCHEMA_VERSION,
        mode: scanner.strict ? 'strict' : 'normal',
        compliance_mode: scanner.compliance || null,
        stats: scanner.stats,
        thresholds: scanner.thresholds,
        findings: complianceFiltered,
        recommendations: buildRecommendations(complianceFiltered),
        layer_summary: buildLayerSummary(flattened),
        owasp_asi_coverage: buildAsiCoverage(flattened),
        threat_model: typeof scanner.generateThreatModel === 'function'
            ? scanner.generateThreatModel(flattened)
            : null,
        population_monitor: typeof scanner.generatePopulationMonitor === 'function'
            ? scanner.generatePopulationMonitor()
            : null,
        meta_guard: typeof scanner.generateMetaGuard === 'function'
            ? scanner.generateMetaGuard()
            : null,
        iocVersion: '2026-02-12',
    };
}

function toSARIFReport(scanner, version) {
    const rules = [];
    const ruleIndex = {};
    const results = [];

    for (const skillResult of scanner.findings) {
        const normalizedSkillFindings = skillResult.findings.map((finding) => normalizeFinding(finding, { source: 'static' }));
        for (const finding of normalizedSkillFindings) {
            if (ruleIndex[finding.id] === undefined) {
                ruleIndex[finding.id] = rules.length;
                rules.push({
                    id: finding.id,
                    name: finding.id,
                    shortDescription: { text: finding.description },
                    fullDescription: { text: finding.rationale },
                    help: { text: `${finding.preconditions}\n\nRemediation: ${finding.remediation_hint}` },
                    defaultConfiguration: {
                        level: finding.severity === 'CRITICAL' ? 'error' : finding.severity === 'HIGH' ? 'error' : finding.severity === 'MEDIUM' ? 'warning' : 'note',
                    },
                    properties: {
                        tags: ['security', finding.category],
                        'security-severity': finding.severity === 'CRITICAL' ? '9.0' : finding.severity === 'HIGH' ? '7.0' : finding.severity === 'MEDIUM' ? '4.0' : '1.0',
                        category: finding.category,
                        rationale: finding.rationale,
                        preconditions: finding.preconditions,
                        remediation_hint: finding.remediation_hint,
                        validation_status: finding.validation_status,
                        validation_state: finding.validation_state,
                        confidence: finding.confidence,
                        attack_chain_id: finding.attack_chain_id,
                    },
                });
            }

            const normalizedFile = String(finding.file || '').replaceAll('\\', '/').replace(/^\/+/, '');
            const artifactUri = `${skillResult.skill}/${normalizedFile}`;
            const fingerprintSeed = `${finding.id}|${artifactUri}|${finding.line || 0}|${(finding.sample || '').slice(0, 200)}`;
            const lineHash = crypto.createHash('sha256').update(fingerprintSeed).digest('hex').slice(0, 24);

            results.push({
                ruleId: finding.id,
                ruleIndex: ruleIndex[finding.id],
                level: finding.severity === 'CRITICAL' ? 'error' : finding.severity === 'HIGH' ? 'error' : finding.severity === 'MEDIUM' ? 'warning' : 'note',
                message: { text: `[${skillResult.skill}] ${finding.description}${finding.sample ? ` — "${finding.sample}"` : ''}` },
                partialFingerprints: {
                    primaryLocationLineHash: lineHash,
                },
                locations: [{
                    physicalLocation: {
                        artifactLocation: { uri: artifactUri, uriBaseId: '%SRCROOT%' },
                        region: finding.line ? { startLine: finding.line } : undefined,
                    },
                }],
                properties: {
                    category: finding.category,
                    rationale: finding.rationale,
                    preconditions: finding.preconditions,
                    false_positive_scenarios: finding.false_positive_scenarios,
                    remediation_hint: finding.remediation_hint,
                    validation_status: finding.validation_status,
                    validation_state: finding.validation_state,
                    confidence: finding.confidence,
                    evidence_spans: finding.evidence_spans,
                    attack_chain_id: finding.attack_chain_id,
                },
            });
        }
    }

    return {
        version: '2.1.0',
        $schema: 'https://json.schemastore.org/sarif-2.1.0.json',
        runs: [{
            tool: { driver: { name: 'guard-scanner', version, informationUri: 'https://github.com/koatora20/guard-scanner', rules } },
            results,
            invocations: [{ executionSuccessful: true, endTimeUtc: new Date().toISOString() }],
        }],
    };
}

function toHTMLReport(scanner, version) {
    return generateHTML(version, scanner.stats, scanner.findings);
}

function printSummary(stats, version, logger = console.log) {
    const total = stats.scanned;
    const safe = stats.clean + stats.low;

    logger(`\n${'═'.repeat(54)}`);
    logger(`📊 guard-scanner v${version} Scan Summary`);
    logger(`${'─'.repeat(54)}`);
    logger(`   Scanned:      ${total}`);
    logger(`   🟢 Clean:       ${stats.clean}`);
    logger(`   🟢 Low Risk:    ${stats.low}`);
    logger(`   🟡 Suspicious:  ${stats.suspicious}`);
    logger(`   🔴 Malicious:   ${stats.malicious}`);
    logger(`   Safety Rate:  ${total ? Math.round(safe / total * 100) : 0}%`);
    logger(`${'═'.repeat(54)}`);

    if (stats.malicious > 0) {
        logger(`\n⚠️  CRITICAL: ${stats.malicious} malicious skill(s) detected!`);
        logger('   Review findings with --verbose and remove if confirmed.');
    } else if (stats.suspicious > 0) {
        logger(`\n⚡ ${stats.suspicious} suspicious skill(s) found — review recommended.`);
    } else {
        logger('\n✅ All clear! No threats detected.');
    }
}

export { 
    toJSONReport,
    toSARIFReport,
    toHTMLReport,
    printSummary,
 };

// ============================================================================
// EO Code Review Skill - Multi-Expert Code Review
// ============================================================================
import { EXPERTS } from '../experts/data.js';
import { buildExpertPrompt, aggregateExpertResults } from '../adapter/skill-adapter.js';
// ---------------------------------------------------------------------------
// Code Review Focus Areas
// ---------------------------------------------------------------------------
const FOCUS_AREA_EXPERTS = {
    'quick': ['rev-001'],
    'standard': ['rev-001', 'rev-002'],
    'deep': ['rev-001', 'rev-002', 'rev-004', 'sec-001'],
};
const REVIEW_CATEGORIES = [
    { id: 'correctness', name: 'Correctness', icon: '🐛', description: 'Logic errors, edge cases, type safety' },
    { id: 'security', name: 'Security', icon: '🔒', description: 'Vulnerabilities, injection, auth issues' },
    { id: 'performance', name: 'Performance', icon: '⚡', description: 'N+1, memory leaks, inefficient algorithms' },
    { id: 'maintainability', name: 'Maintainability', icon: '🔧', description: 'Code structure, naming, complexity' },
    { id: 'style', name: 'Code Style', icon: '🎨', description: 'Formatting, conventions, readability' },
];
// ---------------------------------------------------------------------------
// Code Review Skill Definition
// ---------------------------------------------------------------------------
export const codeReviewSkill = {
    name: 'code-review',
    description: 'Review code for quality, security, and best practices using multiple expert perspectives',
    expert: 'reviewer',
    role: 'reviewer',
    async execute(args, context) {
        const startTime = Date.now();
        const logger = context.logger;
        // 1. Parse arguments
        const input = parseCodeReviewInput(args);
        const depth = input.depth ?? 'standard';
        const target = input.prUrl
            ? `PR: ${input.prUrl}`
            : input.files?.length
                ? `Files: ${input.files.join(', ')}`
                : input.commit
                    ? `Commit: ${input.commit}`
                    : 'Recent changes';
        logger.info(`[code-review-skill] Starting ${depth} review for: ${target}`);
        // 2. Determine expert team based on depth
        const expertIds = FOCUS_AREA_EXPERTS[depth] ?? FOCUS_AREA_EXPERTS['standard'];
        const experts = expertIds
            .map(id => EXPERTS[id])
            .filter((e) => e !== undefined);
        logger.info(`[code-review-skill] Expert team: ${experts.map(e => e.name).join(', ')}`);
        // 3. Build context
        const filesStr = input.files?.length ? `\n\n## Files to Review\n${input.files.map(f => `- ${f}`).join('\n')}` : '';
        const prStr = input.prUrl ? `\n\n## Pull Request\n${input.prUrl}` : '';
        const commitStr = input.commit ? `\n\n## Commit\n${input.commit}` : '';
        const branchStr = input.branch ? `\n\n## Branch\n${input.branch}` : '';
        const repoStr = input.repo ? `\n\n## Repository\n${input.repo}` : '';
        const focusStr = input.focus?.length
            ? `\n\n## Focus Areas\n${input.focus.map(f => `- ${f}`).join('\n')}`
            : '';
        const depthStr = `\n\n## Review Depth\n${depth.toUpperCase()}`;
        const reviewContext = {
            files: input.files,
            prUrl: input.prUrl,
            commit: input.commit,
            branch: input.branch,
            repo: input.repo,
            depth,
            focusAreas: input.focus,
        };
        // 4. Build expert prompts
        const expertPrompts = {
            'rev-001': buildExpertPrompt('rev-001', 'Code Quality Reviewer', `Perform a comprehensive code review:\n\nTarget: ${target}${filesStr}${prStr}${commitStr}${branchStr}${repoStr}${focusStr}${depthStr}\n\nFocus on: code quality, maintainability, readability, best practices, and design patterns.`, reviewContext),
            'rev-002': buildExpertPrompt('rev-002', 'Security Code Reviewer', `Perform a security-focused code review:\n\nTarget: ${target}${filesStr}${prStr}${commitStr}${branchStr}${repoStr}${focusStr}${depthStr}\n\nFocus on: OWASP Top 10, injection vulnerabilities, authentication/authorization issues, data exposure, and secure coding practices.`, reviewContext),
            'rev-004': buildExpertPrompt('rev-004', 'Performance Reviewer', `Perform a performance-focused code review:\n\nTarget: ${target}${filesStr}${prStr}${commitStr}${branchStr}${repoStr}${focusStr}${depthStr}\n\nFocus on: algorithmic complexity, database query efficiency, memory usage, caching opportunities, and scalability concerns.`, reviewContext),
            'sec-001': buildExpertPrompt('sec-001', 'Application Security Engineer', `Conduct a deep security assessment:\n\nTarget: ${target}${filesStr}${prStr}${commitStr}${branchStr}${repoStr}${focusStr}${depthStr}\n\nFocus on: threat modeling, attack surface analysis, secure architecture patterns, and remediation recommendations.`, reviewContext),
        };
        // 5. Run review in parallel
        const results = await Promise.all(experts.map(async (expert) => {
            const prompt = expertPrompts[expert.id] ?? buildExpertPrompt(expert.id, expert.name, target, reviewContext);
            const expertStart = Date.now();
            try {
                const runResult = await context.runtime.subagent.run({
                    sessionKey: context.sessionId ?? `code-review:${target}`,
                    message: prompt,
                    extraSystemPrompt: `You are ${expert.name}, a ${expert.description}. Be thorough, critical, and constructive in your review.`,
                });
                await context.runtime.subagent.waitForRun({ runId: runResult.runId, timeoutMs: depth === 'deep' ? 300000 : 180000 });
                const { messages } = await context.runtime.subagent.getSessionMessages({
                    sessionKey: context.sessionId ?? `code-review:${target}`,
                    limit: 5,
                });
                const lastMsg = messages[messages.length - 1];
                const output = typeof lastMsg?.content === 'string' ? lastMsg.content.slice(0, 2000) : 'No output';
                return {
                    expertId: expert.id,
                    expertName: expert.name,
                    output,
                    durationMs: Date.now() - expertStart,
                    success: true,
                };
            }
            catch (err) {
                logger.error(`[code-review-skill] Expert ${expert.name} failed: ${err}`);
                return {
                    expertId: expert.id,
                    expertName: expert.name,
                    output: '',
                    durationMs: Date.now() - expertStart,
                    success: false,
                    error: String(err),
                };
            }
        }));
        // 6. Parse findings from results
        const findings = parseFindings(results);
        // 7. Format output
        const findingsOutput = formatFindings(findings);
        const expertOutput = aggregateExpertResults(results.map(r => ({ expertName: r.expertName, output: r.output, success: r.success })), 'code-review');
        const severityCounts = findings.reduce((acc, f) => {
            acc[f.severity] = (acc[f.severity] ?? 0) + 1;
            return acc;
        }, {});
        const output = `## 🔍 Code Review Report

### Target
${target}

### Review Depth: ${depth.toUpperCase()}

### Findings Summary
${Object.entries(severityCounts).length === 0 ? '_No specific findings extracted._' : ''}
${Object.entries(severityCounts)
            .sort(([a], [b]) => {
            const order = ['critical', 'high', 'medium', 'low', 'info'];
            return order.indexOf(a) - order.indexOf(b);
        })
            .map(([sev, count]) => {
            const icon = sev === 'critical' ? '🔴' : sev === 'high' ? '🟠' : sev === 'medium' ? '🟡' : sev === 'low' ? '🔵' : '⚪';
            return `${icon} **${sev}:** ${count}`;
        })
            .join('\n')}

### Findings
${findingsOutput}

### Expert Analysis
${expertOutput}`;
        return {
            success: true,
            output,
            expertResults: results,
            findings,
            durationMs: Date.now() - startTime,
        };
    },
};
// ---------------------------------------------------------------------------
// Helper Functions
// ---------------------------------------------------------------------------
function parseCodeReviewInput(args) {
    const params = {};
    const remaining = [];
    for (const part of args.split(/\s+/)) {
        const eqIdx = part.indexOf('=');
        if (eqIdx > 0) {
            params[part.slice(0, eqIdx)] = part.slice(eqIdx + 1);
        }
        else {
            remaining.push(part);
        }
    }
    return {
        files: params.files ? params.files.split(',').map(s => s.trim()) : undefined,
        prUrl: params.prUrl,
        focus: params.focus ? params.focus.split(',').map(s => s.trim()) : [],
        depth: params.depth,
        commit: params.commit,
        branch: params.branch,
        repo: params.repo,
    };
}
function parseFindings(results) {
    const findings = [];
    const combinedOutput = results.map(r => r.output).join('\n');
    // Simple heuristic: look for common patterns in review comments
    const severityKeywords = {
        critical: ['critical', 'severe', 'security breach', 'data leak', 'rce'],
        high: ['high', 'important', 'significant', 'major', 'vulnerability'],
        medium: ['medium', 'concern', 'should', 'recommend', 'consider'],
        low: ['low', 'minor', 'nit', 'suggestion', 'minor issue'],
        info: ['info', 'note', 'FYI', 'observation'],
    };
    const categoryKeywords = {
        security: ['security', 'injection', 'xss', 'csrf', 'auth', 'permission', 'vulnerability'],
        performance: ['performance', 'slow', 'bottleneck', 'n+1', 'memory', 'efficiency'],
        correctness: ['bug', 'error', 'wrong', 'incorrect', 'issue', 'logic', 'crash'],
        maintainability: ['maintain', 'complex', 'readable', 'refactor', 'duplication', 'coupling'],
        style: ['style', 'format', 'convention', 'naming', 'readability'],
    };
    // Split by lines and look for findings patterns
    const lines = combinedOutput.split('\n');
    let findingId = 1;
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.length < 10)
            continue;
        // Heuristic: lines with severity indicators
        let severity = 'info';
        let category = 'maintainability';
        for (const [sev, keywords] of Object.entries(severityKeywords)) {
            if (keywords.some(kw => trimmed.toLowerCase().includes(kw))) {
                if (sev === 'critical')
                    severity = 'critical';
                else if (sev === 'high' && severity !== 'critical')
                    severity = 'high';
                else if (sev === 'medium' && severity !== 'critical' && severity !== 'high')
                    severity = 'medium';
                else if (sev === 'low' && severity === 'info')
                    severity = 'low';
            }
        }
        for (const [cat, keywords] of Object.entries(categoryKeywords)) {
            if (keywords.some(kw => trimmed.toLowerCase().includes(kw))) {
                category = cat;
            }
        }
        // Only add if it looks like a finding (has bullet, number, or specific keywords)
        if (
        // eslint-disable-next-line no-useless-escape
        /^[•\-\*\d]/.test(trimmed) ||
            severity !== 'info' ||
            /found|issue|problem|vulnerability|concern|recommend|suggest/i.test(trimmed)) {
            findings.push({
                id: `finding-${String(findingId++).padStart(3, '0')}`,
                severity,
                category,
                // eslint-disable-next-line no-useless-escape
                description: trimmed.replace(/^[•\-\*\d\.]+/, '').slice(0, 200),
            });
        }
        if (findingId > 20)
            break; // Limit findings
    }
    return findings.slice(0, 20);
}
function formatFindings(findings) {
    if (findings.length === 0)
        return '_No specific findings extracted. See expert analysis below._';
    // Group by severity
    const grouped = {};
    for (const f of findings) {
        if (!grouped[f.severity])
            grouped[f.severity] = [];
        grouped[f.severity].push(f);
    }
    const order = ['critical', 'high', 'medium', 'low', 'info'];
    const lines = [];
    for (const sev of order) {
        const group = grouped[sev];
        if (!group?.length)
            continue;
        const icon = sev === 'critical' ? '🔴' : sev === 'high' ? '🟠' : sev === 'medium' ? '🟡' : sev === 'low' ? '🔵' : '⚪';
        lines.push(`\n${icon} **${sev.toUpperCase()}** (${group.length})`);
        for (const f of group.slice(0, 5)) {
            const catIcon = f.category === 'security' ? '🔒' : f.category === 'performance' ? '⚡' : f.category === 'correctness' ? '🐛' : f.category === 'style' ? '🎨' : '🔧';
            lines.push(`  ${catIcon} ${f.description}${f.file ? ` (${f.file}${f.line ? `:${f.line}` : ''})` : ''}`);
        }
        if (group.length > 5) {
            lines.push(`  _... and ${group.length - 5} more ${sev} findings_`);
        }
    }
    return lines.join('\n');
}
//# sourceMappingURL=code-review-skill.js.map
// ============================================================================
// EO Skill Adapter - ECC Skill Format ↔ OpenClaw Skill Format Conversion
// ============================================================================
// ---------------------------------------------------------------------------
// Claude Code ↔ EO Skill Compatibility Layer
// ---------------------------------------------------------------------------
/**
 * EO standard commands that map to Claude Code capabilities
 */
export const EO_COMMAND_MAPPINGS = {
    'plan': {
        claudeCodeCommand: 'plan',
        description: 'Create a structured project plan with task breakdown',
        defaultExperts: ['pm', 'engineer', 'qa'],
    },
    'architect': {
        claudeCodeCommand: 'architect',
        description: 'Design system architecture and technical specifications',
        defaultExperts: ['architect', 'tech-lead', 'dba'],
    },
    'verify': {
        claudeCodeCommand: 'verify',
        description: 'Verify implementation against specifications',
        defaultExperts: ['qa', 'code-reviewer', 'security-engineer'],
    },
    'code-review': {
        claudeCodeCommand: 'code-review',
        description: 'Review code for quality, security, and best practices',
        defaultExperts: ['code-reviewer', 'senior-dev'],
    },
    'deploy': {
        claudeCodeCommand: 'deploy',
        description: 'Deploy application with CI/CD pipeline',
        defaultExperts: ['devops', 'sre', 'release-manager'],
    },
    'test': {
        claudeCodeCommand: 'test',
        description: 'Write and run tests for verification',
        defaultExperts: ['qa', 'sdet', 'tester'],
    },
    'refactor': {
        claudeCodeCommand: 'refactor',
        description: 'Refactor code for improved quality and performance',
        defaultExperts: ['senior-dev', 'code-reviewer'],
    },
    'security-review': {
        claudeCodeCommand: 'security-review',
        description: 'Perform security audit and vulnerability assessment',
        defaultExperts: ['security-engineer', 'security-auditor'],
    },
};
// ---------------------------------------------------------------------------
// Adapter Functions
// ---------------------------------------------------------------------------
/**
 * Convert an EO Skill to OpenClaw Skill Manifest format
 */
export function eoSkillToOpenClawSkill(eoSkill) {
    return {
        name: eoSkill.name,
        description: eoSkill.description,
        triggers: Array.isArray(eoSkill.trigger) ? eoSkill.trigger : [eoSkill.trigger],
        experts: eoSkill.experts,
        steps: eoSkill.steps?.map(step => ({
            step: step.step,
            expert: step.expert,
            input: step.input,
            output: step.output,
            verify: step.verify,
        })),
        output: eoSkill.output,
    };
}
/**
 * Convert an OpenClaw Skill Manifest to EO Skill format
 */
export function openClawSkillToEoSkill(manifest) {
    return {
        name: manifest.name,
        description: manifest.description,
        trigger: manifest.triggers,
        experts: manifest.experts,
        steps: manifest.steps?.map(step => ({
            step: step.step,
            expert: step.expert,
            input: step.input,
            output: step.output,
            verify: step.verify,
        })),
        output: manifest.output,
    };
}
/**
 * Create a skill from an EO command
 */
export function createSkillFromCommand(command, context) {
    const mapping = EO_COMMAND_MAPPINGS[command.toLowerCase()];
    if (!mapping)
        return null;
    return {
        name: `eo-${command}`,
        description: mapping.description,
        triggers: [`/${command}`, command],
        experts: mapping.defaultExperts,
        output: 'text',
    };
}
/**
 * Parse a skill trigger and extract the command name
 */
export function parseSkillTrigger(trigger) {
    // Remove leading slash
    const cleaned = trigger.replace(/^\//, '');
    return EO_COMMAND_MAPPINGS[cleaned.toLowerCase()] ? cleaned.toLowerCase() : null;
}
/**
 * Build expert prompt from EO expert definition
 */
export function buildExpertPrompt(expertName, expertRole, task, context) {
    const contextStr = context ? `\n\n## Context\n${JSON.stringify(context, null, 2)}` : '';
    return `## Role: ${expertRole} (${expertName})

## Task
${task}${contextStr}

## Instructions
You are playing the role of ${expertRole}.
Provide your analysis and recommendations based on your expertise.
Structure your response with clear sections and actionable items.`;
}
/**
 * Aggregate results from multiple experts into a coherent output
 */
export function aggregateExpertResults(results, command) {
    const lines = [
        `# ${command.toUpperCase()} Results`,
        '',
    ];
    for (const r of results) {
        const status = r.success ? '✅' : '❌';
        lines.push(`## ${status} ${r.expertName}`);
        lines.push(r.output);
        lines.push('');
    }
    return lines.join('\n');
}
//# sourceMappingURL=skill-adapter.js.map
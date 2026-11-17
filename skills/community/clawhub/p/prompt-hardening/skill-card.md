## Description:

Prompt Hardening helps agents audit and strengthen LLM system prompts, agent prompts, AGENTS.md/SOUL.md files, and scheduled prompts for better instruction compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit prompts that agents repeatedly bypass, classify instruction-following failure patterns, and draft hardened prompt language before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local audit script is reported by security evidence as flawed and may produce unreliable checks, especially on untrusted prompt files.

Mitigation: Treat audit results as advisory, avoid running scripts/audit.sh on untrusted prompt files until its shell-check logic is fixed, and manually review prompt changes before use.

Risk: Prompt-hardening recommendations can introduce incorrect, overly rigid, or misleading instructions if applied without context.

Mitigation: Review drafted changes against the target agent's actual tool boundaries, runtime enforcement, and intended user workflow before deployment.

## Reference(s):

- [Detailed Pattern Descriptions](references/patterns.md)
- [Prompt Hardening Research Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with checklist results, rewritten prompt text, violation analysis, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output; prompt changes are applied manually by the operator.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md frontmatter states 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

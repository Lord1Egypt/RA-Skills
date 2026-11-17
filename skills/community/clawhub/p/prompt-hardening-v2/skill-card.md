## Description:

Provides systematic prompt-hardening patterns and an audit checklist to help agents follow rules, respect tool constraints, and reduce instruction drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit and harden system prompts, agent prompts, SOUL.md, AGENTS.md, and scheduled prompts when agents ignore rules, bypass tool constraints, or drift in long conversations. It provides human-applied patterns, checklists, and guidance rather than automatically modifying target prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled local audit script is identified by the security evidence as flawed and may be unsafe for prompt files from untrusted sources.

Mitigation: Avoid running scripts/audit.sh on untrusted prompt files until shell quoting and command-string issues are fixed; use the markdown guidance directly for low-risk review.

Risk: Prompt-only hardening may not fully enforce critical constraints.

Mitigation: Pair critical prompt rules with code-level validation, hooks, or other enforcement mechanisms when reliability matters.

Risk: Hardening recommendations can introduce overbroad or misleading instructions if copied without review.

Mitigation: Review proposed prompt changes against the target agent's actual tools, authority boundaries, and failure history before deployment.

## Reference(s):

- [Detailed Pattern Descriptions](artifact/references/patterns.md)
- [Prompt Hardening Research Sources](artifact/references/sources.md)
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/prompt-hardening-v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with checklist tables and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory/planning output; target prompt changes are applied manually by the operator or a separate executor.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

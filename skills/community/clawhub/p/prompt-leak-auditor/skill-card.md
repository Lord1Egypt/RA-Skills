## Description:

Audits prompts, skill copy, and instructions for leaked secrets, local paths, internal rules, or high-risk instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and prompt authors use this skill before release or internal review to scan prompts, SKILL.md files, README files, or directories for sensitive disclosures and risky instruction patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may contain local paths or partially redacted sensitive snippets.

Mitigation: Review reports before sharing and run the audit only on intended files or directories.

Risk: Very large or untrusted directories may produce noisy or excessive scan output.

Mitigation: Scope each run to specific files or small directories and inspect the report before acting on it.

Risk: The skill output is primarily Chinese-language.

Mitigation: Use it only where Chinese-language reporting is acceptable or add a separate translation and review step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/prompt-leak-auditor)
- [ClawHub publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown report, with optional JSON output from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports mask high-sensitivity content by default and focus on reviewable findings, remediation suggestions, human review points, and follow-up governance.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

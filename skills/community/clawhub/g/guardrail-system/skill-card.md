## Description:

Guardrail System provides input prompt-injection checks, tool permission classification, and output sensitive-information redaction for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add pre-input, pre-tool-use, and post-output checks around AI agent workflows. It helps detect common prompt-injection patterns, require review for higher-risk tool calls, and redact selected sensitive strings before output is shared.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may give users false confidence when enforcing dangerous tool permissions.

Mitigation: Review the tool-authorization behavior before installing it as a security control, and do not rely on it to enforce dangerous tool permissions until the mutable permission policy is fixed and verified.

Risk: Private keys or multiline secrets may not be safely redacted.

Mitigation: Validate multiline secret redaction before using the output guard on sensitive content, and supplement it with independent scanning or human review until the redaction issue is fixed.

## Reference(s):

- [Injection Patterns](artifact/references/injection_patterns.md)
- [Permission Levels](artifact/references/permission_levels.md)
- [ClawHub Skill Page](https://clawhub.ai/paudyyin/skills/guardrail-system)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Python result objects, sanitized text, and Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns allow/block decisions, confirmation or authorization flags, explanatory messages, and optional sanitized output.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

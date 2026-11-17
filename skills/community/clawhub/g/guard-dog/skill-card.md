## Description:

Guard-Dog is an AI safety guard that intercepts eight classes of risky operations and asks for authorization-code verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staroldtrace](https://clawhub.ai/user/staroldtrace)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a prompt-level reminder layer for risky agent actions, including payments, sensitive data access, destructive operations, source inspection, history review, and prompt-injection attempts. It asks for authorization before allowing those actions to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorization codes entered through chat can be exposed through conversation history, logs, or transcripts.

Mitigation: Use a unique code that is not reused elsewhere, avoid entering high-value secrets, and confirm the platform's privacy and logging behavior before use.

Risk: The skill can interfere with inspection, source review, history review, or removal of itself.

Mitigation: Review and scan the skill before installation, and keep an administrative path to inspect or remove it outside the skill's own prompt-level controls.

Risk: The authorization flow should not be treated as real access control because enforcement depends on the host environment.

Mitigation: Use it as a reminder layer and rely on platform-native permission prompts, sandboxing, operating-system permissions, and backups for high-impact actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/staroldtrace/skills/guard-dog)
- [README](README.md)
- [Common Attack Pattern Recognition Manual](references/attack-patterns.md)
- [Guard-Dog Iron Rules](references/iron-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with short status text, authorization prompts, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request an authorization code through chat and defines local vault and state-file paths for the host environment.]

## Skill Version(s):

2.1.3 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

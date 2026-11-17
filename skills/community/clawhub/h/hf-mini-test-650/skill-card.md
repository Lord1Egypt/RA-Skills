## Description:

HF Mini is a local HeartFlow cognitive preprocessor that generates structured cognition data for downstream agents, including state sensing, self-cognition, judgment, self-correction, memory search, emotion analysis, psychology analysis, and reasoning verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced agent users can use this skill to run local cognitive preprocessing and MCP tools that structure user input, inspect reasoning state, retrieve memory, analyze emotions, and verify reasoning before a downstream model produces a final response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill includes under-scoped self-modification and persistent behavior.

Mitigation: Review the skill before installation and run it only in a dedicated test checkout.

Risk: Optional code execution, daemon mode, and self-upgrade behavior can receive local file, process, and repository access.

Mitigation: Do not enable these capabilities unless the operator understands and accepts the access they grant.

Risk: Running the skill near sensitive staged changes or credentials may expose local development state to privileged behavior.

Mitigation: Use an isolated workspace without sensitive staged changes, secrets, or unrelated credentials nearby.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/hf-mini-test-650)
- [npm package @yun520-1/heartflow](https://www.npmjs.com/package/@yun520-1/heartflow)
- [GitHub issues page referenced by artifact](https://github.com/yun520-1/mark-heartflow-skill/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text with optional code snippets, shell commands, configuration notes, and local MCP tool results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some behavior may depend on optional local privileges such as code execution, daemon mode, file writes, or environment access.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 6.0.36)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

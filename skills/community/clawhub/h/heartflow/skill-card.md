## Description:

HeartFlow is a rule-based text discrimination engine for AI output validation with a multi-module pipeline, multiple discrimination dimensions, and no LLM dependency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to check user input, AI drafts, and AI outputs before they are acted on or shown to users. It returns gate decisions, findings, scores, and rewrite or verification guidance for rule-based output quality and safety checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Correction logging and auto-rules can persist snippets of prior local context in JSON files.

Mitigation: Avoid sensitive content unless local persistence is acceptable, and clear the local data files between sessions when needed.

Risk: A local regex and rule-based gate is not a complete safety system and may miss issues or produce false positives.

Mitigation: Use the skill as a pre-send signal and keep human, policy, or application-specific review for high-impact outputs.

Risk: Security evidence notes mixed-language output, inconsistent capability claims, and missing referenced MCP/bin files.

Mitigation: Validate the intended integration path before relying on CLI, MCP, or package capability claims in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/heartflow)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Project link listed in artifact README](https://github.com/yun520-1/mark-heartflow-skill)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown with JavaScript and shell command snippets; runtime checks return structured JavaScript objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gate actions include pass, verify, rewrite, and block; findings may include scores, dimensions, and guidance.]

## Skill Version(s):

6.4.1 (source: SKILL.md frontmatter, package.json, VERSION, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

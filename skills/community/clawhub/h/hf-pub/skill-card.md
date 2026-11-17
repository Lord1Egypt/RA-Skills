## Description:

HeartFlow is a rule-based, LLM-free pipeline that screens AI inputs, drafts, and outputs with text discrimination gates and returns pass, verify, rewrite, or block decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add a local text-screening gate that checks user input, draft responses, and outbound responses before an agent acts or replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation directs users toward Git clone, MCP server, and background daemon workflows for code that security evidence marks as requiring review.

Mitigation: Review the package source and explicitly approve any server or long-running background process before enabling those workflows.

Risk: Local memory and auto-rule behavior may be inappropriate where conversation snippets or adaptive blocking rules are sensitive.

Mitigation: Review or disable local memory and auto-rule persistence before use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/hf-pub)
- [Skill-declared npm package](https://www.npmjs.com/package/@yun520-1/heartflow)
- [Skill-declared GitHub repository](https://github.com/yun520-1/mark-heartflow-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples; runtime API returns structured JavaScript objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pass, verify, rewrite, or block gate decisions with checked_by trace data.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact version 6.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

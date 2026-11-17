## Description:

Use the local Gemini CLI for one-shot prompts, structured JSON output, shell-assisted research, and delegated AI-to-AI workflows on a Linux host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiromps](https://clawhub.ai/user/hiromps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to call a local Gemini CLI for bounded prompts, structured JSON generation, code or content drafting, and secondary model review while retaining control of file edits and command execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or selected file contents may be sent to Gemini.

Mitigation: Use bounded prompts and avoid secret, credential, private, or proprietary files unless sharing that content with Gemini is acceptable.

Risk: Gemini output may include shell commands, code, or guidance that is incorrect or unsafe to apply directly.

Mitigation: Review generated output before executing commands or applying edits, and keep the local agent responsible for validation and final action.

## Reference(s):

- [OpenGemini CLI ClawHub listing](https://clawhub.ai/hiromps/skills/openclaw-gemini-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are proposals from Gemini CLI that should be reviewed before execution or application.]

## Skill Version(s):

1.0.1 (source: server release metadata, released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

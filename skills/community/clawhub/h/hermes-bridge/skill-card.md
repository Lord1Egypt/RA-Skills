## Description:

Delegate tasks or questions to a local Hermes Agent via its CLI for fast, persona-specific responses and terminal tool access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibigbigip](https://clawhub.ai/user/ibigbigip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they want OpenClaw to delegate a task or question to a locally installed Hermes Agent and relay the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated prompt text may be exposed to the local Hermes Agent and its configured tools.

Mitigation: Use the skill only when intentionally sending prompts to Hermes, and avoid sending secrets unless Hermes and its configuration are trusted.

Risk: The documented command pattern can turn delegated prompt text into local shell execution.

Mitigation: Review command construction before use with arbitrary prompt text and prefer separated arguments or another non-shell interface for untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ibigbigip/skills/hermes-bridge)
- [Publisher profile](https://clawhub.ai/user/ibigbigip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local hermes CLI available on the system PATH.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

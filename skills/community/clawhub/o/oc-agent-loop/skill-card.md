## Description:

Keep OpenClaw maintenance tight: diagnose one issue, change one thing, validate it, then keep or revert with evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiepu110](https://clawhub.ai/user/jiepu110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to keep local OpenClaw maintenance tasks bounded: diagnose one issue, make a small candidate change, validate it, and decide whether to keep, revise, or revert.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to edit local files and run validation commands.

Mitigation: Keep changes scoped to one narrow issue, disclose touched files and commands, and require maintainer review before keeping changes.

Risk: A candidate change could be kept without reliable validation.

Mitigation: Run syntax checks, targeted tests, and project-specific validation; revise or revert if validation is missing or failing.

Risk: Maintenance work could affect secrets, deployment targets, or production state.

Mitigation: Do not change credentials, deployment targets, production state, or environment-specific configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiepu110/skills/oc-agent-loop)
- [OpenClaw Gateway Guardian GitHub repository](https://github.com/Star-Ring-Protocol/openclaw-gateway-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text summaries with optional code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include a candidate change summary, validation output summary, keep/revise/revert decision, and deliberately scoped follow-up items.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

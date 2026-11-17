## Description:

Nola is an AI engineering squad lead that dispatches 14 specialist agents to build, test, review, document, and ship software work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flikq](https://clawhub.ai/user/flikq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill in OpenClaw to coordinate multi-agent software work such as feature implementation, bug investigation, code review, testing, documentation, deployment planning, and release tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate agents that modify code, run project commands, start servers, push branches, or create pull requests.

Mitigation: Use it only in trusted or isolated repositories and require explicit approval before command execution, server startup, branch pushes, or pull request creation.

Risk: Broad repository access during delegated coding work could expose unrelated secrets or sensitive files.

Mitigation: Run it in a scoped workspace, avoid mounting unrelated secrets, and review generated changes before release.

Risk: Installer or test dependencies may change over time.

Mitigation: Pin installer and test dependency versions where possible before using the skill in repeatable or production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flikq/skills/nola)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with task briefs, code or configuration changes, shell command snippets, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate multiple specialist agents and produce repository changes depending on the user's request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

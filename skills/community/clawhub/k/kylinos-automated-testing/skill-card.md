## Description:

Guides an agent through GUI compatibility automated adaptation testing for Kylin V11 desktop software without relying on a specific toolchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyanogenic](https://clawhub.ai/user/cyanogenic)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, desktop compatibility testers, and agent operators use this skill to guide agents through install, launch, functional exploration, uninstall, and reporting workflows for Kylin V11 desktop applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to install and remove software and close target processes on a real desktop.

Mitigation: Run it in a disposable VM or dedicated test account and provide the exact package, application, and process scope before testing.

Risk: Desktop screenshots may capture sensitive information from unrelated windows.

Mitigation: Use a clean test desktop and keep sensitive windows closed before allowing screenshot-based testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyanogenic/skills/kylinos-automated-testing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Text]

**Output Format:** [Markdown guidance with structured report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compatibility test plans, action guidance, evidence summaries, and structured test results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

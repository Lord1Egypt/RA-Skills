## Description:

Audit your OpenClaw cron job history and estimate how much you've spent on AI agents this week.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avale-slai](https://clawhub.ai/user/avale-slai)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use Jobaudit to audit recent cron job history, estimate AI agent spend, identify expensive jobs, and produce cost-optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer changes the user's shell startup configuration.

Mitigation: Review the installer before use and make PATH changes manually or with explicit user consent.

Risk: The installer sends an install event to an external Signal Loom endpoint.

Mitigation: Make telemetry opt-in or disclose the install event before running the installer.

Risk: The skill may process job-history and API-key related data flows that are not documented in the artifact.

Mitigation: Document what job history is read, what is transmitted, and how Signal Loom API keys are handled before deployment.

Risk: The package references a jobaudit executable that is not present in the artifact.

Mitigation: Publish the referenced executable or correct the package metadata before users install the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avale-slai/skills/jobaudit)
- [Signal Loom signup](https://signalloomai.com/signup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown cost audit and optimization report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include total job count, cost estimates, cheapest model configuration, savings estimate, and top expensive jobs.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact package.json is 1.0.1 and install.sh is 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

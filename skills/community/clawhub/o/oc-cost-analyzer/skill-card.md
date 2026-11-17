## Description:

Analyzes OpenClaw token usage and costs, identifies high-consumption patterns such as long conversations, frequent cron jobs, and large contexts, and produces cost reports with optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers using OpenClaw use this skill to review local session costs, find expensive usage patterns, and generate recommendations for model choice, context management, cron frequency, and local-model usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw conversation logs from a sensitive memory path.

Mitigation: Run it only in a trusted local environment, review the generated report before sharing it, and confirm the log directory scope before execution.

Risk: The documented data-access path does not match the script behavior.

Mitigation: Confirm the actual log path used by the installed version and update local documentation or configuration before relying on results.

Risk: The documentation includes a broad cleanup command that can delete persistent memory Markdown files.

Mitigation: List matching files and create backups before any deletion; avoid the cleanup command unless deletion is intentional.

Risk: Cron examples can schedule recurring cost checks.

Mitigation: Add cron jobs only when recurring analysis is desired and review their frequency and output location.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report and console text with command recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local cost summaries and a Markdown cost-analysis report; no network output is described.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Schedule automatic OpenClaw and skill updates with reliable cron templates, timezone-safe scheduling, and clear summary outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure scheduled OpenClaw and ClawHub skill update checks, choose safer modes such as dry run or core-only updates, and produce concise update summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring unattended update jobs can update OpenClaw and installed skills without human review.

Mitigation: Use dry-run or core-only examples first, set an explicit timezone, avoid broad all-skill updates where possible, and review how to list, edit, or remove the scheduled cron job before enabling it.

## Reference(s):

- [Agent Implementation Guide](artifact/references/agent-guide.md)
- [Update Summary Examples](artifact/references/summary-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cron setup commands, update-mode guidance, and concise status-summary templates.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

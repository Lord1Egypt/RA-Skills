## Description:

Builds a reusable, scored memory mesh with safety gating and 12-hour auto-refresh for cross-session memory consolidation and quality control in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw agent operators use this skill to consolidate local memory, score and filter reusable lessons, synchronize trusted shared memory feeds, and optionally prepare or post contribution payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled jobs can continue processing local memory after initial setup.

Mitigation: Review the OpenClaw cron configuration before enabling it, use the shortest necessary scope, and disable the schedule when continuous sync is not required.

Risk: Automatic skill updates can replace installed skill copies.

Mitigation: Set auto_update_skills to false unless automatic replacement is intentional, and review update reports before trusting newly pulled memory feeds.

Risk: Local memory-derived contribution payloads can be posted externally to GitHub or through browser automation.

Mitigation: Run posting commands only after reviewing the generated payload and destination issue, keep scheduled posting disabled by default, and use workspaces whose memory files are safe to publish.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/memory-mesh-core)
- [GitHub Issue contribution intake](https://github.com/wanng-ide/memory-mesh-core/issues/1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus generated JSON and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local memory mesh artifacts, reports, contribution payloads, and optional scheduling configuration.]

## Skill Version(s):

1.0.6 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

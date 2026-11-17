## Description:

归档 helps agents work with Granola archives by supporting search, synchronization freshness checks, notes, transcripts, panels, and SQL-oriented data workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external automation users use this skill to request archive search, data synchronization, notes, transcripts, and SQL panel workflows through an agent. It is intended for clearly authorized workflows where the user can review outputs and approve any file, API, or command activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags the release as suspicious because its stated purpose is inconsistent and it advertises scraping evasion plus broad file, API, and command abilities without clear user controls.

Mitigation: Review carefully before installing, use only for clearly authorized targets, and require explicit approval for scraping-evasion, cookie rotation, IP rotation, broad file writes, or command execution.

Risk: The artifact describes API key configuration and data-processing workflows, which can expose sensitive credentials or data if used too broadly.

Mitigation: Keep API keys out of version control, limit credential scope, and confirm the intended data flow before running archive, sync, transcript, SQL, or export workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/grain-crawler)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON snippets with occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key according to artifact usage constraints; review scope before enabling file, API, or command activity.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

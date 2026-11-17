## Description:

Monid helps agents discover, inspect, and run data and API endpoints through the Monid CLI before building custom scrapers or falling back to generic web fetches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monid](https://clawhub.ai/user/monid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find existing Monid endpoints for web scraping, data retrieval, enrichment, search, monitoring, media generation, and API access tasks before implementing a custom integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task data and endpoint requests may be sent to Monid or paid third-party endpoints.

Mitigation: Use Monid only when the user accepts that processing and cost model, prefer existing dedicated tools when available, start with small limits, and check balance when cost awareness matters.

Risk: API keys or file contents could be exposed during setup, command execution, or hosted-file workflows.

Mitigation: Do not paste API keys into chat or visible command lines, approve each upload explicitly, use the shortest practical signed URL lifetime, and delete hosted files after use.

Risk: Mutable global installs and remote skill updates can change behavior after review.

Mitigation: Review CLI and skill updates before installation, avoid unattended updates from mutable latest sources, and keep the skill version aligned with reviewed release evidence.

Risk: Server-supplied hints can influence agent actions.

Mitigation: Treat hints as suggestions, verify them against the inspected endpoint schema and the user's instructions, and do not override user-provided tools or preferences.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monid/skills/monid)
- [Current Monid skill](https://monid.ai/SKILL.md)
- [Monid application](https://app.monid.ai)
- [Monid API keys](https://app.monid.ai/access/api-keys)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands for discovery, inspection, endpoint runs, polling, setup, key management, file upload, and cost checks.]

## Skill Version(s):

0.1.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

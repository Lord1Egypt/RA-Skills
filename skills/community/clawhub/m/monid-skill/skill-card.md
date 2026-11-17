## Description:

Social Media Search guides agents to discover, inspect, and run Monid data endpoints for social media search, scraping, enrichment, and related structured data tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monid](https://clawhub.ai/user/monid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover, inspect, and run Monid endpoints for social media search and other structured data retrieval, especially before building custom scrapers or declaring data inaccessible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monid endpoint runs may spend the user's paid-service balance.

Mitigation: Use Monid only when intentionally selected, prefer the user's existing dedicated tools when available, start with small limits, and confirm cost-sensitive runs before execution.

Risk: The skill can handle API keys during setup.

Mitigation: Do not paste production API keys into chat, save only keys the user explicitly provides for Monid, and verify key state with Monid key-management commands.

Risk: Some workflows upload local files to Monid-managed remote storage for third-party endpoint access.

Mitigation: Approve each local file upload explicitly, use only necessary files, and delete remote files when the workflow is complete.

Risk: The setup guidance asks agents to replace the local skill with the latest remote version.

Mitigation: Avoid automatic self-updates or remote skill replacement unless the new version has been separately reviewed and trusted.

Risk: Broad endpoint access can route user tasks through external services unexpectedly.

Mitigation: Inspect endpoint schemas before running, explain when Monid is being used, and do not route around the user's own service-specific tools or API keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monid/skills/monid-skill)
- [Monid skill source](https://monid.ai/SKILL.md)
- [Monid app](https://app.monid.ai)
- [Monid API keys](https://app.monid.ai/access/api-keys)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke external Monid endpoints and save endpoint results to local files when instructed.]

## Skill Version(s):

0.1.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

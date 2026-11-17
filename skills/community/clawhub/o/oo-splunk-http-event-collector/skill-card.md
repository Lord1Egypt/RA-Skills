## Description:

Splunk HTTP Event Collector (splunk.com). Use this skill for ANY Splunk HTTP Event Collector request — reading, creating, and updating data. Whenever a task involves Splunk HTTP Event Collector, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with a connected Splunk HTTP Event Collector by checking an action's live schema and sending structured or raw event payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs downloaded installer code whose remote behavior has not been verified.

Mitigation: Review the setup path, prefer a verified CLI release, and require approval before downloaded installation code runs.

Risk: Event payloads are sent through the connected OOMOL account to Splunk.

Mitigation: Confirm the exact payload and consider whether its contents are appropriate to send through OOMOL.

## Reference(s):

- [Splunk HTTP Event Collector API documentation](https://help.splunk.com/en/splunk-enterprise/leverage-rest-apis/rest-api-reference/10.4/input-endpoints/input-endpoint-descriptions)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON payloads, Configuration guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads are built to match the live connector schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

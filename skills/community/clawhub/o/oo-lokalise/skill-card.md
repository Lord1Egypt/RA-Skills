## Description:

Lokalise (lokalise.com). Use this skill for ANY Lokalise request — reading, creating, updating, and deleting data. Whenever a task involves Lokalise, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and localization teams use the skill to inspect Lokalise projects, translation keys, languages, and translations, and to create or update keys and translations. Deleting a key requires confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lokalise changes require approval, but setup instructs the agent to execute unverified remote installers without a separate approval step.

Mitigation: Review and approve CLI installation separately, including changes to other agent skills. Use narrowly scoped Lokalise credentials and retain the required confirmations for updates and deletions.

## Reference(s):

- [Lokalise homepage](https://lokalise.com)
- [Lokalise REST API documentation](https://developers.lokalise.com/reference/lokalise-rest-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON payloads and command-line instructions in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses are returned as JSON; input schemas are inspected before actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

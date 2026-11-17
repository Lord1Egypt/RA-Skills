## Description:

Metaso (metaso.cn). Use this skill for ANY Metaso request — reading, creating, and updating data. Whenever a task involves Metaso, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Metaso and read webpages, or to create Metaso chat completions through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs remote installers whose contents were not verified, and setup may make broader local changes.

Mitigation: Review setup before installation, prefer a pinned and independently verified oo CLI install, and explicitly approve its local changes. Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if startup skill synchronization is unwanted.

Risk: Metaso requests pass through OOMOL using the connected account and its permissions.

Mitigation: Connect only the Metaso account and permissions needed for the intended tasks.

## Reference(s):

- [Metaso Search API documentation](https://metaso.cn/search-api/playground)
- [Metaso](https://metaso.cn)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, JSON]

**Output Format:** [Metaso results as text or structured JSON, with JSON action payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the selected Metaso action.]

## Skill Version(s):

1.0.6 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

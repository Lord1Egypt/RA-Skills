## Description:

Search and read data through Serply for web, news, scholar, and video queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users with an OOMOL-connected Serply account can search the web, news, scholarly literature, and video, then use the returned search data in their task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and CLI use can make persistent agent changes through startup skill synchronization, which the skill does not explain.

Mitigation: Review CLI setup and use a reviewed, pinned release. Decide whether additional agent skills should be installed; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

## Reference(s):

- [Serply](https://serply.io)
- [Serply API documentation](https://serply.io/docs)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [JSON search results, including article and academic result entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results vary by action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

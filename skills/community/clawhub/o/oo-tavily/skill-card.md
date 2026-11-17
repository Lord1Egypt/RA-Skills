## Description:

Use Tavily through an OOMOL-connected account to search, crawl, extract, map, and manage research tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily search, crawl, extraction, mapping, usage, and research actions through an OOMOL-connected account, following each action's input schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may persistently change other agents’ installed skills through startup synchronization.

Mitigation: Use a verified, pinned installation and set OO_SKILLS_SYNC_DISABLED=1 before the first invocation if you want to avoid those changes.

Risk: The remote installers and downloaded executable were not verified.

Mitigation: Review the installation source and verify the downloaded executable before installing or running it.

## Reference(s):

- [Tavily API Documentation](https://docs.tavily.com/)
- [Tavily](https://tavily.com)
- [oo CLI Command Reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action requests and responses with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Tavily action and its input schema.]

## Skill Version(s):

1.0.6 (source: skill frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

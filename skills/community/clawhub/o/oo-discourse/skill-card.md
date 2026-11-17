## Description:

Discourse (discourse.org). Use this skill for ANY Discourse request — reading, creating, and updating data. Whenever a task involves Discourse, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected Discourse account can search and read topics, browse categories, and create topics or replies. The skill is intended for users who want an agent to handle Discourse requests through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs automatic execution of remote code, and the documented changes the CLI can make to other agents’ skills are omitted from the setup instructions.

Mitigation: Review CLI installation separately, verify a fixed release before execution, and consider setting OO_SKILLS_SYNC_DISABLED=1 before running the CLI. The remote installers’ complete effects remain unverified.

Risk: Creating a topic or reply changes Discourse content and may publish it to others.

Mitigation: Use only the intended Discourse account and confirm public post contents before running write actions.

## Reference(s):

- [Discourse](https://www.discourse.org/)
- [Discourse API Documentation](https://docs.discourse.org/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [JSON responses and natural-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are returned as JSON; the agent can summarize results in text. Write actions create a topic or reply.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

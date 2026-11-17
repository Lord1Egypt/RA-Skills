## Description:

Access Humor API to search for jokes, memes, and reaction GIFs through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to retrieve jokes, memes, and reaction GIFs from Humor API through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or synchronizing the oo CLI may make persistent changes by installing additional agent skills.

Mitigation: Review and separately approve the CLI installation, preferably using a verified release; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization if it is unwanted.

## Reference(s):

- [Humor API documentation](https://humorapi.com/docs/)
- [Humor API homepage](https://humorapi.com)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Humor API ClawHub release](https://clawhub.ai/oomol/skills/oo-humor-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured Humor API results returned as JSON, including joke and meme content or GIF URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Humor API account and the requested action.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

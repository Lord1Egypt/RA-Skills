## Description:

Scrapfly (scrapfly.io). Use this skill for ANY Scrapfly request — searching and reading data. Whenever a task involves Scrapfly, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to access Scrapfly through an OOMOL-connected account, retrieve monitoring metrics, and scrape public URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the setup uses unverified remote installers whose wider effects are not established.

Mitigation: Review and install the oo CLI separately before enabling the skill; consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1 as described in the CLI reference.

Risk: The connected Scrapfly workflow involves OOMOL handling connected credentials and requests.

Mitigation: Use the integration only if you accept that credential and request handling, and review the public URL and action data before sending a request.

## Reference(s):

- [Scrapfly](https://scrapfly.io/)
- [Scrapfly Scrape API documentation](https://scrapfly.io/docs/scrape-api/getting-started)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON connector responses and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses include data and execution metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

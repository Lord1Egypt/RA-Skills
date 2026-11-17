## Description:

Search and read Wisburg content, including research reports, articles, news, and market updates, through a connected Wisburg account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Wisburg users can search and retrieve reports, articles, news, and other research content through their connected account. The skill guides the agent to inspect each action's schema before querying and returns the available content for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute a remote CLI installer whose behavior has not been verified.

Mitigation: Review and approve the CLI installation separately before setup, including any installation changes or additional skills; connect only the intended Wisburg account.

## Reference(s):

- [Wisburg](https://www.wisburg.com)
- [Wisburg API documentation](https://open-docs.wisburg.com/docs/getting-started/first-call)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Wisburg ClawHub release](https://clawhub.ai/oomol/skills/oo-wisburg)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, URLs]

**Output Format:** [Retrieved Wisburg content as text, Markdown, HTML, and download links where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results and fields depend on Wisburg content and connected account access.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

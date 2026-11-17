## Description:

Fetch and read public web pages through Zenscrape using a connected oo CLI account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can fetch and read public web pages through a connected Zenscrape account, with optional rendering and request controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the oo CLI could run an unverified external installer.

Mitigation: Review and explicitly approve installation, and use a verified release rather than automatically executing a downloaded installer.

Risk: Startup skill synchronization could change other agents’ skills.

Mitigation: Review the synchronization behavior or disable it before the first command.

Risk: URLs and headers submitted for fetching pass through OOMOL-mediated requests.

Mitigation: Consider the contents of submitted URLs and headers, and avoid including data that should not be shared with the service.

## Reference(s):

- [Zenscrape API documentation](https://app.zenscrape.com/documentation)
- [Zenscrape homepage](https://zenscrape.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Zenscrape on ClawHub](https://clawhub.ai/oomol/skills/oo-zenscrape)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [oo CLI commands and JSON fetch results, summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches one public URL per action; returned content depends on the page and request options.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

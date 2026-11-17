## Description:

Use the OOMOL-connected Zyte API to retrieve article, page, product, and browser-rendered HTML data from public URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to retrieve article, page, product, or browser-rendered HTML data from public URLs through their OOMOL-connected Zyte API account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run an unverified remote installer and make broader changes to the agent environment.

Mitigation: Review the setup behavior, install the CLI separately from a reviewed source, require approval before running remote installers, and check automatic skill synchronization settings.

Risk: Requests use the connected Zyte credentials and may incur usage charges.

Mitigation: Use an authorized connected account and review expected usage and billing before making requests.

## Reference(s):

- [Zyte API documentation](https://docs.zyte.com/zyte-api/usage/index.html)
- [Zyte API](https://www.zyte.com/zyte-api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON response data and shell command examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include action data and an execution ID; returned content depends on the selected action.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

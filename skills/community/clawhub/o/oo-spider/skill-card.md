## Description:

Search and read public web data through a connected Spider Cloud account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Spider Cloud users can search, scrape, and extract links from public URLs using their connected account. The skill provides command guidance for the available Spider Cloud actions and returns their structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified installers and make broader changes to agent skills; remote installers have not been inspected, and no malicious intent is established.

Mitigation: Review setup before enabling the skill. Install a verified, pinned CLI yourself, require approval for further software changes, and consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking oo.

Risk: Spider Cloud requests are mediated through OOMOL, and usage may incur charges.

Mitigation: Review the connected account and applicable billing before running actions.

## Reference(s):

- [Spider Cloud API documentation](https://spider.cloud/docs/api)
- [Spider Cloud](https://spider.cloud)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Command guidance and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions operate through the user's connected account; usage may incur charges.]

## Skill Version(s):

1.0.4 (source: server-resolved release and metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

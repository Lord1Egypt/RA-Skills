## Description:

Search Benzinga market news, analyst ratings, earnings events, and news channels through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts can retrieve Benzinga market information, including news channels, analyst ratings, earnings events, and consensus ratings for a ticker. The results can support market research and financial workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may involve an unverified remote installer and persistent changes to other agent skills.

Mitigation: Review the oo CLI installer and release before enabling automatic setup. Consider setting OO_SKILLS_SYNC_DISABLED to prevent startup changes to other agent skills.

Risk: Benzinga access through the connected OOMOL account may consume credit.

Mitigation: Check the connected account's credit status and monitor usage when running Benzinga actions.

## Reference(s):

- [Benzinga API documentation](https://docs.benzinga.com/)
- [Benzinga](https://www.benzinga.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [JSON data returned by Benzinga connector actions, suitable for concise textual summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results depend on the selected action, connected Benzinga account, and provider data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

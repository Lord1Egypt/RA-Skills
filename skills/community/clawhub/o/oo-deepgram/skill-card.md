## Description:

Operates Deepgram through an OOMOL-connected account to inspect available projects, models, API keys, and balances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to inspect the Deepgram projects, models, API keys, and balances available through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified software and affect installed agent skills through automatic synchronization.

Mitigation: Review the oo CLI installer before using it, consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED, and connect only the intended Deepgram account. The remote installers and hosted connector implementation were not verified.

## Reference(s):

- [Deepgram API documentation](https://developers.deepgram.com/docs)
- [Deepgram](https://deepgram.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-deepgram)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include result data and execution metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

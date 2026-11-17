## Description:

Blocknative (blocknative.com). Use this skill for ANY Blocknative request — searching and reading data. Whenever a task involves Blocknative, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to retrieve Blocknative gas price estimates and distributions, gas oracle metadata, and supported chain information through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded installer code without a clear approval step; the remote installers were not verified, and no malicious behavior was established.

Mitigation: Require approval before downloaded installer code runs, verify the oo CLI release, and decide whether automatic agent-skill synchronization is acceptable.

## Reference(s):

- [Blocknative Gas Prediction API documentation](https://docs.blocknative.com/gas-prediction.md)
- [Blocknative](https://www.blocknative.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Blocknative skill on ClawHub](https://clawhub.ai/oomol/skills/oo-blocknative)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands]

**Output Format:** [JSON data and text summaries, with oo CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only gas and chain information; requires a connected Blocknative account.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

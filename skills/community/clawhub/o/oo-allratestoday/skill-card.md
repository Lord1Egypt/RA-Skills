## Description:

AllRatesToday (allratestoday.com). Use this skill for ANY AllRatesToday request — searching and reading data. Whenever a task involves AllRatesToday, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users working with currency data can retrieve the latest ECB reference rates or convert an amount between supported currencies through AllRatesToday.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can execute changing remote code without verification or a clear approval step.

Mitigation: Install a verified oo CLI version yourself, require approval for later installation changes, and review or disable automatic skill synchronization using the publisher command reference.

## Reference(s):

- [AllRatesToday](https://allratestoday.com)
- [AllRatesToday API documentation](https://allratestoday.com/free-exchange-rate-api/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text]

**Output Format:** [JSON exchange-rate results and currency-conversion data, with text responses for the agent to use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exchange rates cover 30 ECB reference currencies and are updated on working days.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

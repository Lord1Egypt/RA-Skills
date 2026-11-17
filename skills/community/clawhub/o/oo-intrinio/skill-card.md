## Description:

Intrinio (intrinio.com). Use this skill for ANY Intrinio request — searching and reading data. Whenever a task involves Intrinio, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial data users can search Intrinio company reference data, look up company and security details, and retrieve historical end-of-day stock prices through their connected Intrinio account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute remote code, and its automatic skill synchronization may change other agent skills.

Mitigation: Review and install a verified CLI release before enabling the skill; require approval for any installation fallback, and check whether disabling automatic synchronization with OO_SKILLS_SYNC_DISABLED is appropriate.

Risk: Intrinio requests use the connected OOMOL account and may consume service credits.

Mitigation: Review expected usage and available service credits before making requests.

## Reference(s):

- [Intrinio API documentation](https://docs.intrinio.com/documentation/api_v2/getting_started)
- [Intrinio](https://intrinio.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Intrinio skill release](https://clawhub.ai/oomol/skills/oo-intrinio)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured data returned by Intrinio actions, with text summaries or guidance as requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The returned data depends on the selected action and requested identifiers.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

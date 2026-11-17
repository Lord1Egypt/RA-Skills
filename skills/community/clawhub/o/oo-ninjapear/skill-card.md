## Description:

Search NinjaPear for company information and retrieve business details through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business analysts can look up company websites, profiles, employee counts, products, customers, and competitors, and check disposable email addresses or account credit through NinjaPear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified software without a clear approval step, and the remote installers were not inspected.

Mitigation: Review and install a verified CLI release separately, and check its automatic skill-synchronization settings.

Risk: NinjaPear requests use the connected account and may consume service credit.

Mitigation: Consider the action and possible credit use before running requests.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [NinjaPear](https://nubela.co/)
- [NinjaPear API documentation](https://nubela.co/docs)
- [NinjaPear ClawHub release](https://clawhub.ai/oomol/skills/oo-ninjapear)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON responses with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Company lookup results, email checks, and account credit information.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

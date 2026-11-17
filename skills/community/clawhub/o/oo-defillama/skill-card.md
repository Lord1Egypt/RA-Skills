## Description:

Search and read DeFiLlama data through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to retrieve DeFiLlama data on tokens, protocols, chains, bridges, yields, and related market metrics for research and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructs the agent to run a CLI installer downloaded from the network.

Mitigation: Use an independently verified, preinstalled oo CLI; require approval before software installation or changes to other agent skills.

Risk: The connected service may handle an API key and incur usage charges.

Mitigation: Review OOMOL's handling of the API key and usage charges before use.

## Reference(s):

- [DeFiLlama API documentation](https://api-docs.defillama.com/)
- [DeFiLlama](https://defillama.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-defillama)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON data returned from DeFiLlama, with natural-language summaries as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Data fields vary by selected DeFiLlama action; some actions require a paid API plan.]

## Skill Version(s):

1.0.2 (source: artifact frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

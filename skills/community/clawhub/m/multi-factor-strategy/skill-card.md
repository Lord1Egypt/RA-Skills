## Description:

Guides users to create multi-factor stock selection strategies and generate independent YAML configuration files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wumu2013](https://clawhub.ai/user/wumu2013)

### License/Terms of Use:


## Use Case:

Developers, quantitative analysts, and investment workflow builders use this skill to design stock-screening and ranking strategies with fundamental and technical factors, then generate QuantCLI-compatible YAML configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes normal but unpinned third-party QuantCLI installation steps.

Mitigation: Verify the QuantCLI package and repository before installing, prefer a pinned reviewed version or commit, and run it in a virtual environment.

Risk: Generated stock-screening strategies can be mistaken for investment advice.

Mitigation: Treat generated strategies as decision-support material and review factor choices, screening thresholds, and outputs before making financial decisions.

## Reference(s):

- [QuantCLI homepage](https://gitcode.com/datavoid/quantcli)
- [ClawHub skill page](https://clawhub.ai/wumu2013/skills/multi-factor-strategy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces QuantCLI strategy configuration examples and decision-support guidance; generated stock-screening strategies should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Guides an agent to answer arithmetic, finance, science, unit conversion, algebra, and matrix calculations through a high-precision Node.js math workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjhuaxin](https://clawhub.ai/user/cjhuaxin)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to have an agent perform high-precision calculations and conversions for everyday, finance, science, engineering, algebra, and matrix math tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically charge users through a third-party billing service for broad math requests.

Mitigation: Require clear per-charge user consent or remove automatic billing before deployment.

Risk: The artifact includes a hardcoded API key in the billing command.

Mitigation: Remove and rotate the key, then require credentials to be supplied through a secure user or deployment configuration.

Risk: The activation scope, global install guidance, and shell-based evaluation path increase deployment risk.

Mitigation: Limit activation to explicit precision-calculation requests, avoid global unpinned installs, and evaluate expressions through a safer non-shell argument path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjhuaxin/skills/precision-calc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; the artifact also includes mathjs installation guidance and SkillPay billing commands.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

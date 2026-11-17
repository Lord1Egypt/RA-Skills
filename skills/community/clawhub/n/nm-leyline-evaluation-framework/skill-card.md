## Description:

Provides weighted scoring, evaluation rubrics, thresholds, and expected-gain-versus-cost utility guidance for quality gates and agent-action decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent designers use it to build weighted evaluation rubrics and threshold-based quality gates, and to assess whether tool calls or agent dispatches are worth their expected cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags action-selection guidance that could override other guidance, along with a scoring example that could reward insecure results; the scan evidence is incomplete.

Mitigation: Review and correct the action-selection instructions and penalty calculation before installation, as advised by the security guidance.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance, Configuration]

**Output Format:** [Markdown with scoring rubrics, thresholds, decision guidance, and optional YAML or Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: artifact frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Run an Oxford Union-style multi-agent debate on any motion using Mixture of Agents architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markoxmobs](https://clawhub.ai/user/markoxmobs)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run structured Oxford Union-style debate simulations for motion analysis, argument stress-testing, and formal debate preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad debate or argument stress-testing requests can trigger a full multi-round workflow and consume more model calls than a short critique.

Mitigation: Specify a low hard round cap or ask for lighter analysis when a brief critique is sufficient.

Risk: Generated debate material can be rhetorically persuasive without independently verifying every factual claim.

Mitigation: Review evidence and claims before using the final brief for formal debate preparation or decision support.

## Reference(s):

- [Oxford Union Debate - Reference Guide](references/DEBATE_FORMAT.md)
- [MOA-Debate ClawHub Skill Page](https://clawhub.ai/markoxmobs/skills/mixtureofagents-debate)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown debate transcript and structured debate brief, with JSON used internally for the final brief schema.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configurable completeness threshold and hard round cap; normal runs may produce multiple debate rounds before closing rebuttals and a final brief.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

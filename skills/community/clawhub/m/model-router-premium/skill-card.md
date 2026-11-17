## Description:

Route model requests based on configured models, costs and task complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrjootta](https://clawhub.ai/user/mrjootta)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to choose an LLM for a request from a trusted model configuration, balancing task complexity, declared capabilities, explicit preferences, and cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic routing can choose a model that is too weak for high-stakes legal, medical, security, or accuracy-sensitive tasks.

Mitigation: Treat the selected model as a routing hint and require human review or explicit overrides for high-stakes requests.

Risk: Untrusted model configuration files can bias routing toward unsuitable or unintended models.

Mitigation: Use a trusted, reviewed models JSON file and avoid passing arbitrary paths or unvalidated caller-provided configuration.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mrjootta/skills/model-router-premium)
- [Skill definition](artifact/SKILL.md)
- [Router script](artifact/scripts/router.py)
- [Example model configuration](artifact/examples/models.json)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON model selection with plain-text reasoning; Markdown guidance when used by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a caller-provided models JSON file and task description; no token caps or post-processing requirements are specified.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

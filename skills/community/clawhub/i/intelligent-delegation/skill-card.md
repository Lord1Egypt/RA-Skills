## Description:

A 5-phase framework for reliable AI-to-AI task delegation, inspired by Google DeepMind's "Intelligent AI Delegation" paper (arXiv 2602.11865). Includes task tracking, sub-agent performance logging, automated verification, fallback chains, and multi-axis task scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hogpile](https://clawhub.ai/user/hogpile)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to structure AI-to-AI delegation with task logs, verification contracts, fallback chains, and performance tracking. It helps agents choose delegation posture, monitor delegated work, and decide when human approval is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent scheduled checks and task or performance logs that can change an agent's delegation workflow.

Mitigation: Review planned schedules and logs before enabling the workflow, and keep sensitive task details out of persistent records unless retention is approved.

Risk: The scoring tool can understate risk for irreversible, external, financial, deletion, or sensitive-data actions.

Mitigation: Require separate human approval before using score output to authorize high-impact or irreversible actions.

Risk: Delegated outputs may be accepted too readily if verification contracts are incomplete.

Mitigation: Define machine-checkable success criteria before delegation and require manual review where outputs depend on judgment or sensitive context.

## Reference(s):

- [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865)
- [ClawHub skill page](https://clawhub.ai/hogpile/skills/intelligent-delegation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with templates, Python command-line tools, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task tracking templates, delegation contract templates, fallback guidance, a scoring CLI, and a verification CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

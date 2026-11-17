## Description:

Meta Interpretable Attribution helps agents perform interpretable attribution workflows with added self-verification, reflection, adversarial validation, and cross-session learning notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add interpretable feature attribution, counterfactual analysis, self-checking, and reflection loops to attribution-oriented agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can record local learning notes and is designed for broader self-reflection or meta-agent workflows.

Mitigation: Keep stored notes non-sensitive, review or clear learned_patterns.json when used, and require a separate approval step before downstream agents treat notes as trusted instructions.

Risk: The security verdict is suspicious because cross-session learning and broad meta-agent loops are not tightly scoped.

Mitigation: Install only after reviewing the skill behavior and keep meta-agent integration boundaries explicit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-interpretable-attribution)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local learning notes when the learner script is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

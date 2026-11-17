## Description:

Provides a neuro-symbolic reasoning workflow that combines vector-similarity generalization with Horn-clause forward chaining so agents can return confidence-scored inferences, verifiable conclusions, fallbacks, and conflict signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to combine neural nearest-neighbor inference with symbolic rule-based reasoning for relationship reasoning, knowledge completion, trusted question answering, and anti-hallucination workflows. It is most useful when an agent needs both generalized soft evidence and auditable or falsifiable symbolic conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps persistent local memory of usage, errors, and preferences.

Mitigation: Treat learned_patterns.json as untrusted local state, avoid storing secrets or sensitive notes in it, and review the file before sharing or packaging the skill.

Risk: The skill documentation includes self-editing guidance for updating SKILL.md after repeated errors or usage.

Mitigation: Require explicit review before allowing any automatic rewrite of skill instructions or release artifacts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qq435912743/skills/neuro-symbolic-reasoning)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; runtime helpers return JSON-like dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence scores, verifiability flags, neural hints, fallback decisions, and conflict indicators.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

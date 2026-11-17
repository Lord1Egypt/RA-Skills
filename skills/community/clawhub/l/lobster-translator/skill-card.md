## Description:

Helps agents clarify vague user requests, translate formal or technical content into plain Chinese, and prepare structured task-delegation templates for multi-agent work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to turn ambiguous requests into clearer prompts, rewrite formal or technical wording into approachable Chinese, and package handoffs for other agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation language may cause the skill to intervene on requests that only need direct execution.

Mitigation: Use it when ambiguity, style translation, or delegation packaging is needed, and bypass it for already-clear tasks.

Risk: Playful Chinese wording and emoji-heavy style may be inappropriate for formal or business-critical content.

Mitigation: Ask for a formal tone or reduced stylistic embellishment when the output will be used in professional settings.

Risk: Clarification templates could overfill missing context or imply decisions the user has not made.

Mitigation: Keep unresolved decisions explicit and ask the user to confirm goals, scope, resources, deadlines, and constraints.

## Reference(s):

- [Template library](templates/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown guidance and structured JSON-like response objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces clarification prompts, missing-information lists, recommended templates, translated content, or task-delegation blocks depending on mode.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

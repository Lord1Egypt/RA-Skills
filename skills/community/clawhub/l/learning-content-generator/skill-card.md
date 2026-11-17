## Description:

Generates personalized learning content and short quizzes for selected knowledge-graph nodes, adapting depth by hierarchy and parent context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzp2026](https://clawhub.ai/user/wzp2026)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, learning-platform builders, and agents use this skill to turn a knowledge graph plus a target node into structured study material, source labels, and quiz questions. It is especially suited to Chinese-language learning paths that need different depth for L1, L2, and L3 nodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Possible third-party lookups of learning topics through RAG behavior.

Mitigation: Disable or remove RAG retrieval unless it is needed, and review any external sources before relying on generated content.

Risk: Overconfident or hardcoded educational content can produce inaccurate learning material.

Mitigation: Independently verify generated claims, citations, standards, and quiz answers before publication or learner use.

Risk: Plugin-loading configuration can expand the behavior of the skill.

Mitigation: Disable plugin auto-loading unless all plugins are identified, reviewed, and approved for the deployment environment.

Risk: Local output and progress files may be written during generation.

Mitigation: Run the skill in a controlled workspace and inspect generated files before sharing or importing them elsewhere.

Risk: Chinese/domestic-source defaults may not match every audience or compliance need.

Mitigation: Confirm the source policy and geography fit the intended learners before commercial use.

## Reference(s):

- [Detailed learning content generator README](references/README.md)
- [Learning content generator configuration](references/content_config.yaml)
- [ClawHub skill page](https://clawhub.ai/wzp2026/skills/learning-content-generator)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown study content with quiz sections, plus JSON metadata and verification reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local content, quiz, JSON, progress, and verification files; long content may be split.]

## Skill Version(s):

2.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

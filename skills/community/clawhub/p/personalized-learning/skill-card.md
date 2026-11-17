## Description:

Personalized Learning helps an agent turn a learning request into a structured lesson, curriculum, or self-contained HTML learning page with a progressive outline, complete sections, and instructional visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vaintwyt](https://clawhub.ai/user/vaintwyt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, learners, and content creators use this skill to have an agent design and package tutorial-style learning material for a stated topic and audience. It is most useful when the desired output is a complete lesson page with aligned navigation, prose, examples, and visuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included HTML template uses Simplified Chinese placeholders by default, which can be mismatched for lessons intended for other audiences.

Mitigation: Ask the agent to set the lesson language and replace template placeholders for the intended learner before delivery.

Risk: Generated tutorial pages can include incomplete or misleading explanations if the requested topic or learner background is underspecified.

Mitigation: Review the final lesson for factual accuracy, completeness, and audience fit before using it for instruction.

## Reference(s):

- [HTML template](references/html-template.html)
- [ClawHub skill page](https://clawhub.ai/vaintwyt/skills/personalized-learning)
- [Publisher profile](https://clawhub.ai/user/vaintwyt)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Usually a self-contained HTML file; can adapt to another requested teaching format.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML is intended to inline styles, scripts, graphics, and animation logic so the lesson can be delivered as one file.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

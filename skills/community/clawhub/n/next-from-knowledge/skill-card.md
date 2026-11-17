## Description:

Knowledge-to-action skill that turns notes, research, meeting summaries, documents, and knowledge graph outputs into the next action, decision, plan, or experiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and knowledge workers use this skill after collecting notes, research, meeting summaries, or knowledge graph outputs to choose the next move, build a short plan, make a decision, design a small experiment, or identify the few gaps that would change the recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill turns user-provided notes and research into recommendations, so weak or incomplete source material can lead to overconfident next actions.

Mitigation: Check that the recommendation separates observed facts, assumptions, and missing information before acting on consequential decisions.

Risk: The default prompt and much of the presentation favor Chinese output, which may be unsuitable for teams expecting English-only workflows.

Mitigation: Specify the desired output language in the request or adapt the prompt configuration before using it in a shared workflow.

Risk: The CLI reads local files supplied through --file, which may include sensitive notes or meeting content.

Mitigation: Review file inputs before use and avoid passing confidential material unless the local agent environment is approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/next-from-knowledge)
- [Action Frames](artifact/references/action-frames.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style guidance, plain text CLI output, or JSON analysis depending on the selected mode.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Modes include next-step, plan, decide, experiment, gaps, and analyze; input can come from a file or inline text.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

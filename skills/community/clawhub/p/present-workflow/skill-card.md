## Description:

Guides an installing agent through a staged presentation workflow for clarifying a brief, gathering facts when needed, building an outline, creating page-level planning, producing reviewable intermediate artifacts, and handling limited capabilities honestly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[textboy](https://clawhub.ai/user/textboy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to plan presentation decks from topics, briefs, source materials, or partial outlines. It helps an agent produce research briefs, outlines, planning drafts, sample artifacts, full deck plans, and review notes with explicit checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or private source material may appear in generated research briefs, planning drafts, or Markdown output.

Mitigation: Avoid providing secrets or private content unless it is acceptable for that content to appear in generated deck-planning artifacts; review outputs before sharing.

Risk: The workflow may save a final approved plan under ./output/ and could overwrite an existing file if the agent reuses a path.

Mitigation: Check the target file path before writing and ask for confirmation before overwriting an existing output file.

Risk: Presentation topics that depend on current or uncertain facts can produce weak or unsupported claims if the agent skips verification.

Mitigation: Use the research and review gates for evidence-sensitive decks, label source-limited outputs, and verify key claims before final delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/textboy/skills/present-workflow)
- [PPT Agent Workflow Method](references/method.md)
- [Agent Integration Guide](references/agent-integration.md)
- [Reusable Prompts](references/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, guidance]

**Output Format:** [Markdown, structured text, optional outline JSON, and optional HTML or SVG page representations when the environment supports them.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The final approved deck plan, or the delivered output layer, may be saved as ./output/<name>.md for downstream presentation generation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

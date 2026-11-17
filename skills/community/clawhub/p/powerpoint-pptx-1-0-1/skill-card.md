## Description:

Create, inspect, and edit Microsoft PowerPoint presentations and PPTX decks with reliable layouts, templates, placeholders, notes, charts, and visual QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyzx](https://clawhub.ai/user/gyzx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and presentation authors use this skill to guide agents through creating, inspecting, editing, and quality-checking PowerPoint decks while preserving templates, placeholders, notes, charts, and visual fidelity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deck QA can require reading speaker notes, comments, embedded media, and linked asset references that may contain non-visible or sensitive content.

Mitigation: Install and invoke the skill only for workflows where the agent is expected to inspect or modify PowerPoint files, and review notes, comments, and linked assets as part of handoff.

Risk: PowerPoint edits can produce misleading or incomplete decks through placeholder mismatches, text overflow, broken charts, weak contrast, clipped shapes, or theme and master inheritance issues.

Mitigation: Render or inspect affected slides after edits and run separate content and visual QA passes before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gyzx/skills/powerpoint-pptx-1-0-1)
- [Skill homepage](https://clawic.com/skills/powerpoint-pptx)
- [Publisher profile](https://clawhub.ai/user/gyzx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell commands, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output may include deck inspection notes, edit plans, QA findings, and recommended validation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

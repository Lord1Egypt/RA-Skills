## Description:

Professional storyboard design tool for short drama and video production that helps plan stories, characters, shot breakdowns, CSV review tables, and handoff guidance for downstream image or video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautyaiclub](https://clawhub.ai/user/beautyaiclub)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, production planners, and agent users use this skill to turn story outlines or scripts into character design prompts, relationship matrices, shot-by-shot storyboard CSVs, and review-ready planning notes. It is intended for storyboard planning and handoff; actual image and video generation is delegated to a separate myreels-api workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save story briefs, prompts, request payloads, task IDs, metadata, returned URLs, and generated media references in local project folders.

Mitigation: Use a deliberate output directory and avoid sensitive or confidential story material unless local retention is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beautyaiclub/skills/myreels-storyboard)
- [Character Design Reference](references/character-design.md)
- [Recommended Model List](references/models.md)
- [Multilingual Support Reference](references/multilingual.md)
- [Scene Templates for Short Drama](references/scene-templates.md)
- [Storyboard Template & Format Specification](references/storyboard-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and CSV-compatible planning tables for characters, relationships, and storyboard shots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May organize local project workspaces containing story briefs, prompts, review notes, CSV drafts, approved snapshots, request payloads, task records, metadata, and generated media references.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

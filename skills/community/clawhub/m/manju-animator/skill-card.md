## Description:

Converts static comic storyboards into concise image-to-video prompts, camera motion guidance, and tool parameter suggestions for Kling, Pika Labs, and Runway Gen-3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samwang-001](https://clawhub.ai/user/samwang-001)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to animate vertical comic storyboard shots while keeping character appearance, scene continuity, camera movement, and duration constraints consistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad animation-related requests.

Mitigation: Install it where Chinese-language comic animation prompt workflows are expected, and review activation behavior before deployment.

Risk: Prompt or parameter guidance may still produce visual instability in image-to-video tools.

Mitigation: Review generated shot plans before use and apply the skill's downgrade guidance for high-risk shots.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/samwang-001/manju-skills/tree/main/manju-animator)
- [ClawHub skill page](https://clawhub.ai/samwang-001/skills/manju-animator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown-style Chinese-language shot plan with prompts, tool settings, risk notes, and fallback guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for 9:16 image-to-video workflows; no files, commands, credentials, or API calls are produced.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Converts a Markdown article into a clickable 16:9 interactive HTML presentation with narration planning, Vite React TypeScript implementation guidance, optional generated visuals, and optional text-to-speech audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangzhipengdamon-maker](https://clawhub.ai/user/liangzhipengdamon-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical content creators use this skill to turn articles, product documents, or learning notes into interactive, playable HTML presentation experiences. It guides script and outline creation, project scaffolding, chapter implementation, optional media generation, and static build output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article text or derived narration may be sent to external image or text-to-speech services when multimodal generation is enabled.

Mitigation: Use placeholder or local assets for confidential documents, or switch to an approved provider before generating images or speech.

Risk: The documented build flow may rely on an unpinned npx download.

Mitigation: Inspect or create package.json and a lockfile, then use a pinned local Vite dependency before running the build.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangzhipengdamon-maker/skills/html-interactive-presentation)
- [web-video-presentation dependency](https://github.com/ConardLi/garden-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command blocks; the workflow may produce script and outline files, a Vite React TypeScript project, generated media assets, and static HTML build output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional image and speech generation can be replaced with placeholders or alternate providers when MiniMax is unavailable.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

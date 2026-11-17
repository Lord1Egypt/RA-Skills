## Description:

Turns reference images or text briefs into platform-ready video plans, prompts, negative prompts, shot designs, motion parameters, and, when compatible tools are available, generated videos with optional audio, subtitles, and multi-shot stitching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeshenyue12345](https://clawhub.ai/user/yeshenyue12345)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn still images or text concepts into executable short-video direction packages, platform-specific prompts, and optional local assembly steps for audio, subtitles, and stitched clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local media helper scripts and dependency setup require review before an agent runs them automatically.

Mitigation: Install only in a restricted workspace, review scripts first, pin dependencies, and constrain output paths before execution.

Risk: Text-to-speech or dialogue generation may process sensitive dialogue or create unwanted voice content.

Mitigation: Avoid sensitive dialogue with TTS features and require user confirmation for voice text and style before generation.

Risk: Unbounded media parameters can create excessive runtime, unexpected files, or poor output quality.

Mitigation: Constrain durations, colors, volume values, and output paths before allowing automated script runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yeshenyue12345/skills/multi-platform-video-director)
- [platform-routing.md](artifact/references/platform-routing.md)
- [prompt-patterns.md](artifact/references/prompt-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown instructions, prompts, parameter recommendations, and optional shell command snippets or generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include video-generation prompts, negative prompts or fidelity constraints, shot tables, platform settings, retry guidance, and commands for local audio, subtitle, probing, muxing, or stitching helpers.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and manifest list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

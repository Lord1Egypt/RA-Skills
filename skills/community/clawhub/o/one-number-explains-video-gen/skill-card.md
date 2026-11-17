## Description:

Create vertical data-stat hook videos with a hero number, ramping counter or graph, closing meaning line, and timed English captions through WeryAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and agent users use this skill to turn one metric or chart into a short vertical dataviz video with a hook, animated ramp, concise meaning line, and English subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can upload local image files to WeryAI when non-HTTPS image values are used.

Mitigation: Prefer public HTTPS image URLs and use local image paths only after reviewing the behavior and getting explicit consent for upload.

Risk: Prompts, image URLs, and explicitly approved local image files are sent to WeryAI using a paid API key.

Mitigation: Avoid sensitive inputs, keep WERYAI_API_KEY out of source control, and prefer an isolated or short-lived key for higher assurance.

Risk: Generated videos can imply precision or factual certainty for metrics that were not vetted.

Mitigation: Require user approval for real-stat wording and use illustrative-counter language when no source is supplied.

## Reference(s):

- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/one-number-explains-video-gen)
- [ClawHub publisher profile](https://clawhub.ai/user/zoucdr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and final video links or errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts are structured into hook, ramp, and meaning beats; normal operation requires Node.js 18+, WERYAI_API_KEY, network access, and paid WeryAI API use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

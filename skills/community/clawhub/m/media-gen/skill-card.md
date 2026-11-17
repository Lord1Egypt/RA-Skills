## Description:

Generate AI images or videos through AIsa for creative generation, asset drafts, and media workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for AIsa-backed image and video generation workflows, including prompt-based image drafts, short video tasks, task polling, and optional media downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and AISA_API_KEY are used with the AIsa service.

Mitigation: Install only if the publisher and AIsa service are trusted; prefer the AISA_API_KEY environment variable over passing secrets on the command line.

Risk: Returned media URLs can be fetched and written to local output paths without host or size checks.

Mitigation: Run the script from a limited workspace, avoid sensitive --out paths, and review download behavior before enabling automatic downloads.

## Reference(s):

- [Media Gen ClawHub page](https://clawhub.ai/bibaofeng/skills/media-gen)
- [AIsa API base](https://api.aisa.one/v1)
- [AIsa video API base](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; bundled CLI emits JSON status and can write image or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; generated media may be returned as base64 data or downloaded from service-provided URLs.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

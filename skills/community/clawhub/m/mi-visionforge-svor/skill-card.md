## Description:

Removes selected objects from short videos using SVOR-based segmentation and video object removal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangfei1204](https://clawhub.ai/user/wangfei1204)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to segment target objects in short videos, inspect suggested object IDs, and remove selected objects through the XiaomiTools SVOR service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video inputs, prompts, masks, and API-key authenticated requests are sent to the XiaomiTools service.

Mitigation: Use non-sensitive test videos first, avoid media with personal or confidential content, and keep SVOR_API_KEY out of shared machines, logs, and version control.

Risk: The remote service controls returned result-download URLs, and the evidence notes no local URL validation or size/time limits.

Mitigation: Run the skill in an isolated environment, review returned URLs before relying on outputs, and avoid networks with sensitive internal services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangfei1204/skills/mi-visionforge-svor)
- [Publisher Profile](https://clawhub.ai/user/wangfei1204)
- [SVOR Project Reference](https://github.com/xiaomi-research/svor)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and generated video or mask files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, ffmpeg, and SVOR_API_KEY; uploads video inputs to a remote service and downloads returned results.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

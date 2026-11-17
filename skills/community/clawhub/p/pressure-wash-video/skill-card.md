## Description:

Generate vertical satisfying pressure-wash shorts with WeryAI from text prompts or dirty-surface images, producing rinse motion with a moving clean/dirty line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to generate vertical pressure-washing videos from text briefs or public HTTPS dirty-surface images. The agent expands the prompt, checks WeryAI parameters, asks for confirmation, and returns playable video URLs or a clear failure explanation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local image path can cause a readable local file to be uploaded to WeryAI.

Mitigation: Use public HTTPS image URLs by default; only use local paths after reviewing the script, isolating the runtime, and explicitly consenting to upload that exact file.

Risk: Paid WeryAI generation can consume credits when wait or submit commands are run.

Mitigation: Show the full parameter table and get user confirmation before submitting a real generation request; use dry-run when checking payload shape.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/pressure-wash-video)
- [WeryAI video CLI and JSON reference](artifact/resources/WERYAI_VIDEO_API.md)
- [WeryAI video API host](https://api.weryai.com)
- [WeryAI model registry and upload host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with parameter tables, JSON command payloads, and returned video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and user confirmation before paid generation.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

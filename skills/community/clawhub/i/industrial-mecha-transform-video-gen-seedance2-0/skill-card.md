## Description:

Reforge everyday actions as factory-floor power fantasy with hydraulics, sparks, armor plates, heavy synchronized motion, and WeryAI Seedance 2.0 video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative agents use this skill to turn text prompts or a single image into short industrial mecha-style videos through WeryAI Seedance 2.0. It guides prompt expansion, parameter confirmation, submission, polling, and delivery of playable video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a WeryAI API key and outbound network access for paid video generation.

Mitigation: Use an isolated runtime or separate account, keep WERYAI_API_KEY secret, and install only when this external access is acceptable.

Risk: Local image paths may cause local files to be uploaded to WeryAI.

Mitigation: Use public HTTPS image URLs by default and require explicit user consent before any local file upload path is used.

Risk: Documented shell examples can create command-injection risk if prompts are interpolated into shell command strings.

Mitigation: Invoke the Node CLI with structured JSON arguments and avoid constructing shell commands directly from untrusted prompt text.

## Reference(s):

- [WeryAI Video API Reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/industrial-mecha-transform-video-gen-seedance2-0)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline video links, confirmation tables, JSON-backed CLI calls, and clear failure guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, outbound network access, and paid WeryAI generation credits.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Creates, checks, previews, and schedules Pinterest pins from a user's page and their photos or videos, with scheduling only after approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Bloggers, creators, and shop owners use this skill to turn pages and their own media into distinct Pinterest pins, check and preview a batch, then schedule it after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious, citing media uploads, image redirects, and undeclared tool scope; the scan was partial and its evidence is incomplete.

Mitigation: Review the upload destination, timing, and credential handling; limit the files and connected tools available to the agent; inspect the preview and approve the batch before publishing.

## Reference(s):

- [Pinterest: limits, rules and how pins are found](artifact/references/pinterest-specs.md)
- [Pin plan format](artifact/references/plan-json.md)
- [Writing pin titles, descriptions, and alt text](artifact/references/writing.md)
- [WoopSocial Pinterest MCP](https://woopsocial.com/social-media-mcp/pinterest-mcp?utm_source=pinterest-skill&utm_medium=skill)

## Skill Output:

**Output Type(s):** [Images, Video, Text, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JPEG or PNG pins and MP4 videos, with JSON plans and manifests, Markdown schedules and pin copy, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's supplied media and page details; scheduling requires explicit approval.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

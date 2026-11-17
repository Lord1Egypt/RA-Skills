## Description:

Generate vertical WeryAI shorts that transform organizing and decluttering scenes from chaos to order, including closets, fridges, vanities, desks, luggage, and similar satisfying before-and-after clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn short organizing or decluttering briefs, and optional image references, into confirmed WeryAI video generation requests and playable vertical short links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled video script can upload a readable local image path to WeryAI when local paths are used as image inputs.

Mitigation: Prefer public HTTPS image URLs; allow local image paths only after verifying the exact file, size, and destination and obtaining explicit user consent.

Risk: Prompts and media are sent to WeryAI during non-dry-run generation.

Mitigation: Use dry runs to inspect request payloads before paid submits, avoid sensitive prompts or media, and run in an isolated workspace when sensitive files may be readable.

Risk: WERYAI_API_KEY is required for generation, status checks, model lookups, and local-image upload.

Mitigation: Use a limited-scope or test API key, keep the key out of chat and logs, and install only if the publisher and WeryAI processing are acceptable.

## Reference(s):

- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/organize-room-video)
- [WeryAI video generation API](https://api.weryai.com)
- [WeryAI model registry and upload API](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with parameter tables, JSON command payloads, shell commands, and video result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and WERYAI_API_KEY; non-dry-run generation uses paid authenticated network calls.]

## Skill Version(s):

1.0.5 (source: server release evidence; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

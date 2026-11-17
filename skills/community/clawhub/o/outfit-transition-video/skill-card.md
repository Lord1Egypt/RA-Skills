## Description:

Generate vertical shorts of anthropomorphic outfit changes on beat with WeryAI, including one-second cuts, style jumps, and accessory detail macros.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate short vertical outfit-transition videos through WeryAI from text prompts or public HTTPS image URLs. It is aimed at fashion look-change clips, beat-synced reels, and accessory-focused video macros.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can upload a readable local file supplied as an image path to WeryAI.

Mitigation: Prefer public HTTPS image URLs; use local paths only after reviewing the script, getting explicit user consent, and running from an isolated working directory or container.

Risk: Generation requires a WERYAI_API_KEY and makes paid network calls.

Mitigation: Treat the API key as a secret, do not commit it, confirm parameters before each paid run, and warn that successful wait runs consume WeryAI credits.

Risk: Unsupported model fields or invalid image URLs can cause failed paid generation attempts.

Mitigation: Validate model, duration, aspect ratio, and image URL requirements against the bundled WeryAI API reference before submitting a request.

## Reference(s):

- [WeryAI Video CLI and JSON Reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/outfit-transition-video)
- [WeryAI Video API Host](https://api.weryai.com)
- [WeryAI Model and Upload API Host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON parameters, confirmation tables, status summaries, and video URLs or failure details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, paid WeryAI credits, and user confirmation before paid generation runs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

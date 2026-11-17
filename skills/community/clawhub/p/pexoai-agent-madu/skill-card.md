## Description:

Creates short AI-generated videos for ads, social media, brand, product, UGC-style, promo, and explainer content in multiple aspect ratios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madu1seo-bit](https://clawhub.ai/user/madu1seo-bit)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to request short social videos, product ads, promotional clips, UGC-style content, and revisions through Pexo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell helpers source a local config file before making requests.

Mitigation: Keep ~/.pexo/config private and writable only by the current user.

Risk: The API key is sent to the configured PEXO_BASE_URL.

Mitigation: Set PEXO_BASE_URL to https://pexo.ai unless intentionally using another trusted endpoint.

Risk: Video prompts and uploaded media are sent to Pexo for generation.

Mitigation: Avoid sensitive or proprietary files unless Pexo's retention and deletion policies are acceptable.

## Reference(s):

- [Setup and Troubleshooting](references/SETUP.md)
- [Pexo OpenClaw Setup Guide](https://pexo.ai/connect/openclaw)
- [Pexo Homepage](https://pexo.ai)
- [ClawHub Skill Page](https://clawhub.ai/madu1seo-bit/skills/pexoai-agent-madu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON status responses, and plain-text video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project links, asset IDs, preview choices, status updates, and final video URLs; requires PEXO_API_KEY and PEXO_BASE_URL.]

## Skill Version(s):

0.2.0 (source: server release evidence; artifact frontmatter states 0.3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

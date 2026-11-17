## Description:

ZeeLin Music helps users generate complete AI songs from a short prompt, with support for vocal or instrumental music and styles such as pop, rock, and folk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongjiangliu9-tech](https://clawhub.ai/user/dongjiangliu9-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create songs from prompts, lyrics, style preferences, and vocal or instrumental choices. The skill guides the agent through ZeeLin App-Key validation, lyric generation, music generation, status polling, and presenting generated audio links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a ZeeLin billing App-Key and sends that key to MelodyLab for billing-related operations.

Mitigation: Use the skill only if comfortable sharing that key with MelodyLab; prefer a dedicated, revocable, low-balance key if supported and monitor charges.

Risk: The server security summary notes that the privacy policy does not clearly disclose the App-Key credential flow.

Mitigation: Review the privacy and billing disclosures before installation, and avoid entering personal or sensitive content into song prompts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongjiangliu9-tech/skills/melodylab-ai-song)
- [MelodyLab Homepage](https://melodylab.top)
- [ZeeLin Skill Platform](https://skills.zeelin.cn)
- [README](artifact/README.md)
- [Privacy Policy](artifact/PRIVACY.md)

## Skill Output:

**Output Type(s):** [guidance, API calls, markdown, configuration]

**Output Format:** [Markdown conversation with API request instructions and generated audio links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated lyrics, task status updates, remaining balance notices, and links to generated audio files.]

## Skill Version(s):

1.2.0 (source: frontmatter, release evidence, README version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

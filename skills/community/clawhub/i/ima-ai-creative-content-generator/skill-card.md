## Description:

All-in-one AI content generator for creative, marketing, and social media workflows across image, video, music, and text-to-speech generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dai-shuo](https://clawhub.ai/user/dai-shuo)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, social media teams, and developers use this skill to generate campaign assets, product visuals, promotional clips, background music, jingles, narration, and multi-media creative workflows through IMA Studio services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose API keys, prompts, URLs, and local files beyond the clearly bounded generation flow.

Mitigation: Review before installing, use a scoped or test IMA API key, and avoid passing sensitive local paths as image inputs.

Risk: A custom base URL can receive the API key and prompts.

Mitigation: Use the default IMA endpoint or another destination only when you fully control and trust it.

Risk: Local preference and log files may retain workflow details after use.

Mitigation: Check or clear ~/.openclaw/memory/ima_prefs.json and ~/.openclaw/logs/ima_skills/ after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dai-shuo/skills/ima-ai-creative-content-generator)
- [IMA Studio homepage](https://imastudio.com)
- [IMA API key management](https://www.imaclaw.ai/imaclaw/apikey)
- [IMA credits and subscription](https://www.imaclaw.ai/imaclaw/subscription)
- [Security disclosure](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, media URLs]

**Output Format:** [Markdown guidance with shell command examples, progress messages, and generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses IMA_API_KEY for IMA service requests; generated outputs may include image, video, audio, or speech URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

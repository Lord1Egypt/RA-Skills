## Description:

Find memes, 表情包 / 斗图 and reaction images and place them into articles, newsletters, docs or video scripts. Use when the user asks to add memes / 表情包 / reaction images to a piece of writing, to "配图" with memes, or to find a meme for a feeling, reaction or character (熊猫头, 奶龙, Drake, This Is Fine…). Searches the memecub library over HTTP with curl; every result says whether it is cleared for commercial use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyupi](https://clawhub.ai/user/liyupi)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and content creators use the skill to find reaction images that fit a passage and place them in articles, newsletters, documentation, or video scripts while preserving license and attribution details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server-side matching sends the article text to memecub, which may expose confidential writing.

Mitigation: Use short searches for confidential material; submit a full article only when you intend to share it with memecub.

Risk: Authenticated searches spend account credits and can search the user's private library.

Mitigation: Use keyless searches when suitable, and review intended account use before making authenticated requests.

Risk: Some collected memes are not cleared for commercial use, and some openly licensed images require attribution.

Mitigation: Check each result's license fields, filter for commercial use when needed, and retain any required credit line.

## Reference(s):

- [Memecub on ClawHub](https://clawhub.ai/liyupi/skills/memecub)
- [Memecub search API](https://memecub.com/api/v1/search)
- [Memecub account keys](https://memecub.com/dashboard?tab=keys)
- [Memecub pricing](https://memecub.com/pricing)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, API Calls]

**Output Format:** [Markdown image embeds with attribution when required, plus placement guidance or meme suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results identify whether each image is cleared for commercial use; credit lines should be kept when required.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

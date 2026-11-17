## Description:

Create and edit Instagram Shop Reels, Stories sequences, product demos, creator UGC adaptations and paid-social video variants. Use this skill for Instagram电商视频、INS Reels、Instagram Shop、Story、UGC种草、产品标签内容、Meta Ads、创作者合作、品牌账号视频和社交电商；supports Seedance modes through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams, creators, and marketers use this skill to generate and adapt Instagram Reels, Stories, Shop demos, UGC cuts, and Meta Ads video variants through AI Hive Seedance video modes while preserving product, brand, rights, and placement constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API client can send the user's bearer API key to an arbitrary configured base URL.

Mitigation: Review configuration before running, avoid custom base URLs or inherited AI_HIVE_BASE_URL values, and prefer the default AI Hive endpoint only when trusted.

Risk: The skill uploads user-provided media to AI Hive for video generation workflows.

Mitigation: Use the skill only when the user trusts AI Hive with the API key and uploaded media, and run it in an isolated environment with pinned dependencies.

Risk: Generated ecommerce videos may include unsupported claims, synthetic platform UI, engagement counts, or rights-sensitive creator references if prompts and outputs are not reviewed.

Mitigation: Review outputs against current Instagram commerce, branded-content, advertising, and asset-rights requirements; add tags, links, handles, and disclosures in Instagram rather than generating them into footage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/instagram-ins-ecommerce-video-generation-editing)
- [AI Hive API base endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON API responses, and downloaded media files when generation succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an AI Hive bearer API key, optional media uploads, routing controls, model parameters, and a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Generate Instagram marketing content from product URLs, including product summaries, image or video briefs, captions, calls to action, hashtags, and posting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, creators, and agents use this skill to turn public e-commerce product URLs into ready-to-review Instagram content packages for feed posts, carousels, stories, or reels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product URLs and extracted page content may be sent to SkillBoss API Hub during automated extraction. <br>
Mitigation: Use a dedicated API key and avoid internal, private, tokenized, or otherwise sensitive storefront URLs. <br>
Risk: Generated marketing copy, prices, claims, and hashtags may be inaccurate, outdated, or unsuitable for publication. <br>
Mitigation: Review all generated content against the product page, brand guidance, and applicable marketing requirements before posting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kirkraman/jx-marketing) <br>
- [Instagram Hashtag Strategy](references/HASHTAG_STRATEGY.md) <br>
- [Instagram Content Package Output Template](templates/OUTPUT_TEMPLATE.md) <br>
- [SkillBoss API Hub](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown content package with optional JSON product extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automated extraction requires SKILLBOSS_API_KEY; generated prices, claims, captions, hashtags, and posting guidance should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

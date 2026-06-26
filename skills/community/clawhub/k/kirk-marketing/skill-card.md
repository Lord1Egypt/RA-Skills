## Description: <br>
Generate Instagram marketing content from product URLs, including product extraction, image or video briefs, captions, calls to action, hashtag strategy, and posting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and commerce teams use this skill to turn public e-commerce product URLs into ready-to-post Instagram content packages. It helps select feed, carousel, story, or reel formats and drafts visual direction, captions, hashtags, posting strategy, and engagement prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public product URLs and scraped page text are sent to SkillBoss API Hub for scraping and extraction. <br>
Mitigation: Use a dedicated SkillBoss API key, submit only public product URLs without sensitive query tokens, and avoid sending private or regulated data. <br>
Risk: Generated marketing claims or extracted product details may be inaccurate or unsuitable for publication. <br>
Mitigation: Review all extracted details, product claims, pricing, captions, and hashtags before posting. <br>


## Reference(s): <br>
- [Instagram Hashtag Strategy](references/HASHTAG_STRATEGY.md) <br>
- [Instagram Content Package Output Template](templates/OUTPUT_TEMPLATE.md) <br>
- [SkillBoss API Hub](https://api.skillbossai.com/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/kirkraman/kirk-marketing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown content package with optional JSON product extraction] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include image or video briefs, captions, hashtags, posting strategy, engagement prompts, and manual extraction fallback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

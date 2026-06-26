## Description: <br>
Generate Instagram marketing content from product URLs, including image suggestions, captions, calls to action, hashtags, and posting strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketers use this skill to turn e-commerce product URLs into ready-to-post Instagram content packages. The skill supports feed posts, carousels, stories, reels, caption copy, hashtag sets, and visual briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automated extraction workflow sends product URLs and extracted page text to the SkillBoss/HeyBoss API service using the user's API key. <br>
Mitigation: Use public product pages, avoid links containing secrets or unpublished business data, and verify the API host before running the helper script. <br>
Risk: Generated marketing copy, hashtags, and posting strategy may be inaccurate or unsuitable for a brand, product category, or regulated claim. <br>
Mitigation: Review generated content before publishing and adapt claims, captions, hashtags, and calls to action to the brand's requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tobeyrebecca/godfery-mkt) <br>
- [Hashtag Strategy](references/HASHTAG_STRATEGY.md) <br>
- [Output Template](templates/OUTPUT_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content package with optional JSON product extraction output and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require SKILLBOSS_API_KEY for automated product extraction; manual extraction fallback is documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

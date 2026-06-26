## Description: <br>
Hot Content Creator helps agents fetch multi-platform trending topics, select content directions, generate Xiaohongshu-style cover and avatar assets, and draft human-facing social content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and marketers use this skill to turn current Chinese social platform trends into five candidate content angles, visual cover or avatar generation workflows, and platform-ready post copy. <br>

### Deployment Geography for Use: <br>
Global, with practical dependence on access to the configured trend, search, and image-generation services. <br>

## Known Risks and Mitigations: <br>
Risk: Trend, search, or image-generation requests may send user-provided topics to external services. <br>
Mitigation: Avoid entering sensitive private topics and review the configured providers before using the skill for confidential work. <br>
Risk: The artifact references user-configured API credentials through a missing TOOLS.md setup path. <br>
Mitigation: Verify the intended API provider and use narrowly scoped keys before installation or execution. <br>
Risk: Broad trigger phrases such as hot content creation or trend chasing could activate the workflow unintentionally. <br>
Mitigation: Narrow or customize trigger phrases if accidental activation would disrupt normal agent use. <br>
Risk: AI-generated visuals or copy may be mistaken for non-AI content. <br>
Mitigation: Keep the workflow's AI-generated image and copy disclosures, and review generated claims before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengpengliu1212-art/hot-content-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style trend reports, numbered content direction options, image-generation guidance, and social post copy.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured trend, search, and image-generation services; generated images and final copy should include AI-generated content disclosure where appropriate.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Provides AI-powered optical character recognition through SkillBoss, letting agents choose hosted models by cost, speed, and quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill when they need OCR or AI-assisted text extraction and want to compare hosted model choices for cost, speed, and quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes work through a broad paid SkillBoss API gateway even though it is presented as an OCR skill. <br>
Mitigation: Review the SkillBoss setup and scope before installation, and use a restricted or low-quota API key. <br>
Risk: OCR inputs may contain sensitive images, PDFs, business records, or personal documents. <br>
Mitigation: Avoid sending sensitive content unless SkillBoss and the selected upstream model provider meet the user's privacy, retention, and billing requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kirkraman/kirk-ai-ocr) <br>
- [SkillBoss console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-ocr) <br>
- [SkillBoss products](https://skillboss.co/products) <br>
- [SkillBoss API endpoint](https://api.skillboss.co/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

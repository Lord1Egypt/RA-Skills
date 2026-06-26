## Description: <br>
Generate AI videos from text prompts or images with Seedance 2.0 on SkillBoss. Best for short ads, product demos, launch clips, and social videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and marketing teams use this skill to generate short AI videos from text prompts or reference images through SkillBoss, especially for ads, product demos, launch clips, and social video formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference image URLs are sent to SkillBoss for paid video generation. <br>
Mitigation: Use the skill only when third-party SkillBoss processing is approved, and avoid submitting secrets, confidential media, internal URLs, or personal data unless policy allows it. <br>
Risk: The skill uses a SkillBoss API key and can incur pay-as-you-go generation charges. <br>
Mitigation: Use a scoped SkillBoss API key where possible and confirm duration, aspect ratio, and request intent before running paid generations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-seedance-video) <br>
- [SkillBoss Seedance Video page](https://skillboss.co/skills/seedance-video) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss run endpoint](https://api.skillboss.co/v1/run) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request payloads, curl examples, and generated video URLs or task payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes prompt, duration, and aspect ratio; reports API errors with retry guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Use the SkillBoss API Hub to plan and implement multimodal media workflows for image, video, speech, and audio generation and understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to choose SkillBoss media capabilities and adapt Node.js or REST templates for generating, editing, analyzing, transcribing, and narrating media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, audio, and video selected by the user are sent to SkillBoss for processing. <br>
Mitigation: Avoid sensitive, regulated, confidential, or copyrighted media unless the user has permission and has reviewed the provider terms. <br>
Risk: The required SKILLBOSS_API_KEY is a paid-service secret. <br>
Mitigation: Store the key in a secret manager or local environment variable, avoid committing it, and avoid logging request headers. <br>
Risk: Generated media and analysis can be inaccurate, misleading, or unsuitable for publication. <br>
Mitigation: Review generated outputs before release and apply human checks for rights, safety, and factual claims. <br>
Risk: Video and media generation may take longer than expected or fail intermittently. <br>
Mitigation: Use timeouts, retries, and fallback handling before relying on generated media in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/martin-media) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and curl code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API request templates, environment variable setup, response parsing notes, and operational cautions for media workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

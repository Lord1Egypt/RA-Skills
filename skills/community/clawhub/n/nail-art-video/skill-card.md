## Description: <br>
生成美甲制作过程短视频。猫眼、流沙、星空、奶油胶、微缩立体美甲——小尺寸极高细节，近景治愈感强，支持节日主题，一句话出片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to generate short vertical nail-art process videos through WeryAI, with prompts focused on macro hand or material shots, ASMR cues, and detailed nail styles. The skill guides parameter selection, confirmation, and video generation calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and generation parameters are sent to WeryAI. <br>
Mitigation: Avoid submitting sensitive content and review the generated prompt and parameters before confirming a request. <br>
Risk: Video generation requires WERYAI_API_KEY and may consume provider credits. <br>
Mitigation: Use a dedicated API key when possible, keep it out of prompts and logs, and confirm cost-sensitive requests before execution. <br>
Risk: The bundled WeryAI client supports broader video-generation behavior than the nail-art framing. <br>
Mitigation: Keep use aligned with the documented nail-art workflow and review parameters before running generated commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/nail-art-video) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with confirmation tables, JSON parameters, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js and WERYAI_API_KEY to submit and monitor WeryAI video generation requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

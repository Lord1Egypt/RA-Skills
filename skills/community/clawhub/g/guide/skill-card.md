## Description: <br>
文物讲解词一键生成。用户只需提供文物名称和 API 信息，系统自动判断讲解风格并生成400-500字的专业讲解词。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangzw0707](https://clawhub.ai/user/jiangzw0707) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Museum educators, guides, and cultural content creators use this skill to generate Chinese narration for cultural relics from a relic name, optional museum context, audience profile, and optional visitor question. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the configured model API key in a local JSON file. <br>
Mitigation: Use a trusted local environment, restrict file access, and prefer a limited-scope API key that can be rotated. <br>
Risk: Relic names, audience descriptions, and optional questions are sent to the configured API endpoint. <br>
Mitigation: Use a trusted HTTPS provider and avoid entering private, unpublished, or sensitive information. <br>
Risk: Broad Chinese trigger phrases may activate the skill for generic introduction or explanation requests. <br>
Mitigation: Review the trigger list before deployment and narrow activation phrases if the host agent routes unrelated requests to the skill. <br>
Risk: Generated museum narration may contain inaccurate cultural or historical details. <br>
Mitigation: Have a qualified reviewer check generated narration before public or educational use. <br>


## Reference(s): <br>
- [Cultural Relics Guide on ClawHub](https://clawhub.ai/jiangzw0707/guide) <br>
- [Required local API configuration](artifact/config/user_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Guidance] <br>
**Output Format:** [Plain text narration printed to the console and saved as a UTF-8 .txt file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 400-500 Chinese characters and uses the user's configured OpenAI-compatible chat completion API endpoint.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

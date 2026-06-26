## Description: <br>
Generate, Edit, Collaborate. Access all mainstream AI models in one toolkit. Simply describe your vision to create videos, images, and avatars-zero manual operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litmedia-ai](https://clawhub.ai/user/litmedia-ai) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users and agent operators use Litmedia to create videos, images, talking avatars, voice outputs, and edited media through the LitMedia service. The skill helps an agent choose generation tools, authenticate the user, estimate costs, submit jobs, and return generated media results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts, URLs, images, audio, and videos may be sent to external LitMedia services. <br>
Mitigation: Use the skill only with media and prompts that the user is authorized to process externally; avoid confidential, biometric, or third-party likeness and voice material without consent. <br>
Risk: Generation tasks can consume account credits. <br>
Mitigation: Estimate cost and confirm task parameters before submitting paid generation work. <br>
Risk: Credentials may remain on disk until logout succeeds. <br>
Mitigation: Use the skill only on trusted machines, protect saved credentials, and run the logout flow when access is no longer needed. <br>
Risk: Security evidence reports sensitive data exposure in logs. <br>
Mitigation: Avoid sharing raw command output or logs, and review logs for credentials, personal data, prompts, or private media URLs before disclosure. <br>


## Reference(s): <br>
- [Litmedia ClawHub release](https://clawhub.ai/litmedia-ai/litmedia) <br>
- [LitMedia AI](https://www.litmedia.ai) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [Auth Module](references/auth.md) <br>
- [AI Image Module](references/ai_image.md) <br>
- [Video Generation Module](references/video_gen.md) <br>
- [Avatar4 Module](references/avatar4.md) <br>
- [Character Replace Module](references/video_mimic.md) <br>
- [User Module](references/user.md) <br>
- [Error Handling Guide](references/error_handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Chat guidance with command invocations, generated media URLs, and optional downloaded media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May consume LitMedia account credits and may send selected prompts, URLs, images, audio, or videos to external LitMedia services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

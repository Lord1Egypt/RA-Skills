## Description: <br>
Create AI digital human videos with the HeyGen API using a free starter guide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dAAAb](https://clawhub.ai/user/dAAAb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and creators use this skill to configure HeyGen API access, inspect available avatars and voices, and generate AI avatar videos from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HeyGen API keys are sensitive credentials. <br>
Mitigation: Store the API key outside source control and avoid sharing logs or screenshots that expose it; rotate the key if it is disclosed. <br>
Risk: Text, avatar, and voice inputs are sent to a third-party video generation service. <br>
Mitigation: Review inputs before sending them to HeyGen and avoid submitting data that is confidential, regulated, or unauthorized for avatar or voice use. <br>
Risk: The skill includes affiliate signup and premium upsell links. <br>
Mitigation: Verify payment, plan, and signup links independently before purchasing or entering billing details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dAAAb/heygen-avatar-lite) <br>
- [HeyGen avatars API endpoint](https://api.heygen.com/v2/avatars) <br>
- [HeyGen voices API endpoint](https://api.heygen.com/v2/voices) <br>
- [HeyGen video generation API endpoint](https://api.heygen.com/v2/video/generate) <br>
- [HeyGen video status API endpoint](https://api.heygen.com/v1/video_status.get?video_id=$VIDEO_ID) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a HeyGen API key and sends avatar, voice, and script inputs to HeyGen.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

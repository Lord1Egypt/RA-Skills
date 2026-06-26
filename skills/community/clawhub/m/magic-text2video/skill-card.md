## Description: <br>
Create a text-to-video job from user-provided copy. Submits to the remote video service via one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyuangao](https://clawhub.ai/user/zhangyuangao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit user-provided scripts or paragraphs to a remote text-to-video service, then report the resulting task_id and video_url. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the API key and user-provided text to a remote video service. <br>
Mitigation: Use a dedicated, revocable MAGIC_API_KEY and avoid submitting confidential or personal text. <br>
Risk: The current client disables TLS certificate verification for remote service calls. <br>
Mitigation: Treat the client as unsafe on untrusted networks until TLS verification is restored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyuangao/magic-text2video) <br>
- [MagicLight remote API host](https://open-test.magiclight.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAGIC_API_KEY; reports task_id and video_url when the remote service succeeds.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

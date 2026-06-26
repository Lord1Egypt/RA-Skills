## Description: <br>
Helps agents retrieve JFTech device livestream URLs for multi-client playback using HLS, RTSP, RTMP, FLV, MP4, and WebRTC protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to request live video stream URLs for already-bound, online JFTech devices and choose playback protocols for web, mobile, mini-program, or third-party player integrations. <br>

### Deployment Geography for Use: <br>
Global, with documented JFTech API endpoints for China Mainland, Asia, Europe, and North America. <br>

## Known Risks and Mitigations: <br>
Risk: Generated livestream URLs and device credentials can expose sensitive camera access if logged, shared, or stored insecurely. <br>
Mitigation: Store app secrets, device tokens, and device passwords in a secure secret manager; avoid logging generated stream URLs; and share URLs only with authorized viewers. <br>
Risk: Long-lived stream URLs increase exposure if a URL is copied or intercepted. <br>
Mitigation: Use the shortest practical URL expiry for the playback scenario and rotate credentials or regenerate URLs when access should end. <br>
Risk: The configurable API endpoint and URL test action can contact destinations outside the expected vendor service. <br>
Mitigation: Restrict JF_ENDPOINT to trusted JFTech domains and use test-url only when the returned livestream destination is trusted. <br>


## Reference(s): <br>
- [JFTech Open Platform documentation](https://docs.jftech.com) <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-livestream) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plaintext livestream URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print sensitive livestream URLs and playback guidance; generated URLs can remain usable until their configured expiry.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

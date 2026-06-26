## Description: <br>
Generates a shareable 2026 Year of the Horse New Year fortune MP4 video, using HTML as an intermediate screenshot and preview asset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiweidesigner](https://clawhub.ai/user/weiweidesigner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn personal New Year fortune inputs, such as name, birth details, personality, and wishes, into a short festive fortune video with narration, background imagery, and music. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags this release as suspicious and recommends review before installation, especially in shared or sensitive environments. <br>
Mitigation: Review the skill and scan result before deployment, and run it only in environments where its behavior and external service use are acceptable. <br>
Risk: The skill requires sensitive credentials and includes embedded API keys for external AI, image, and speech services. <br>
Mitigation: Replace embedded keys with secure user-managed configuration, rotate any exposed credentials, and avoid sharing secrets in the skill artifact. <br>
Risk: Personal fortune inputs and generated text may be sent to external AI, image, and speech services. <br>
Mitigation: Inform users before use, avoid entering sensitive personal data, and confirm that external service handling is acceptable for the intended audience. <br>
Risk: Runtime dependency installation and disabled HTTPS certificate verification can weaken environment and network security. <br>
Mitigation: Preinstall pinned dependencies through a trusted package process and restore normal HTTPS certificate verification before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weiweidesigner/happynewyear) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Video, HTML, JSON status] <br>
**Output Format:** [MP4 video with an HTML preview/intermediate file and JSON status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary output is new_year_blessing_video.mp4; new_year_blessing.html is retained as an intermediate preview asset.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

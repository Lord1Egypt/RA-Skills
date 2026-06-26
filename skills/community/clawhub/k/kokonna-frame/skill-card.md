## Description: <br>
Control KoKonna AI e-ink art frames by uploading images, querying device info, and managing multiple frames when users ask to send or display images on a frame. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guooscar](https://clawhub.ai/user/guooscar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw agents to configured KoKonna e-ink frames, upload selected images, and query frame status such as battery, connectivity, and firmware. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and frame status requests are sent to the configured KoKonna API. <br>
Mitigation: Verify the API host and device keys before use, and configure only devices the user intends to control. <br>
Risk: Private or sensitive photos could be uploaded to a frame service. <br>
Mitigation: Avoid uploading sensitive photos and confirm the selected image before sending it. <br>
Risk: The all-device upload option can push an image to every configured frame. <br>
Mitigation: Confirm the target device list before using the all-device option. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guooscar/kokonna-frame) <br>
- [KoKonna](https://kokonna.art) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Python, and YAML examples; runtime commands may return text or JSON device status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload user-selected images and query device status through the configured KoKonna API.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter, manifest.yaml, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

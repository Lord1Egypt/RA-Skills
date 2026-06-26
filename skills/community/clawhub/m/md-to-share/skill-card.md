## Description: <br>
Converts Markdown files into long JPEG or PNG images that AI agents can generate for sharing on channels such as WeChat, Discord, iMessage, or local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dtacheng](https://clawhub.ai/user/dtacheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn Markdown reports, notes, or responses into shareable long-form images with channel-aware sizing and splitting behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsanitized Markdown or embedded HTML can render inside a network-enabled browser and may trigger remote resource requests. <br>
Mitigation: Use trusted Markdown when possible, review image output before sharing, and avoid processing content with unexpected embedded HTML or external resources. <br>
Risk: Broad trigger wording could cause an agent to process or share Markdown when the destination channel is unclear. <br>
Mitigation: Confirm the target channel before conversion when the user has not specified Discord, WeChat, iMessage, or local output. <br>
Risk: Installation can download Chromium and npm dependencies. <br>
Mitigation: Install from trusted release sources and use normal dependency review controls before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dtacheng/md-to-share) <br>
- [Publisher Profile](https://clawhub.ai/user/dtacheng) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands that produce JPEG or PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be a single long image or multiple split image files depending on channel, file size, and height settings.] <br>

## Skill Version(s): <br>
2.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

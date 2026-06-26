## Description: <br>
Search and send GIFs on WhatsApp. Handles the Tenor-to-MP4 conversion required for WhatsApp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaharsha](https://clawhub.ai/user/shaharsha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search trusted GIF providers, convert a selected GIF into a WhatsApp-compatible MP4, and send it through the configured WhatsApp message tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent downloads GIF media, converts it locally, and copies generated MP4 files into the workspace. <br>
Mitigation: Use the skill only when local media processing and temporary workspace files are acceptable; delete generated workspace MP4 files when local retention matters. <br>
Risk: The skill sends media through the configured WhatsApp message tool. <br>
Mitigation: Confirm the intended recipient before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaharsha/gif-whatsapp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and message tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gifgrep, ffmpeg, curl, and the configured message tool.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Create mobile-first newspaper-style brief images from raw content or existing summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EisonMe](https://clawhub.ai/user/EisonMe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to turn raw articles, chats, notes, meeting records, or existing summaries into structured mobile newspaper-style briefs. It helps prepare concise HTML or PNG long-image outputs for reading, sharing, and archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive source material can be written into generated local HTML or PNG files. <br>
Mitigation: Avoid using highly sensitive inputs unless local file output and storage are acceptable. <br>
Risk: Optional PNG generation may invoke a local browser in headless mode. <br>
Mitigation: Run the renderer in a trusted local environment and review the generated HTML when handling sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EisonMe/newspaper-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Structured brief content with JSON input guidance, HTML output, optional PNG rendering, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Python renderer and may optionally invoke a local Edge or Chrome browser for screenshots.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

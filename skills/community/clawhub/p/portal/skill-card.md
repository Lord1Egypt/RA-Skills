## Description: <br>
Portal helps agents create shareable live browser sessions for website demos, product tours, interactive sandboxes, and guided or guarded browser experiences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zach213](https://clawhub.ai/user/Zach213) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and support teams use Portal to turn public, authenticated, or local web experiences into shareable Watch demos or guarded Play sessions for external viewers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portal can save authenticated browser sessions for demos. <br>
Mitigation: Use disposable or least-privilege demo accounts and avoid production admin sessions. <br>
Risk: Portal can upload local project files to a cloud service. <br>
Mitigation: Remove secrets such as .env files and credentials before uploading local projects. <br>
Risk: The release depends on a separate Portal plugin for cloud browser actions. <br>
Mitigation: Verify the Portal plugin before trusting it with private sites or source code. <br>


## Reference(s): <br>
- [Portal Skill on ClawHub](https://clawhub.ai/Zach213/portal) <br>
- [Portal Website](https://makeportals.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline JSON, shell commands, URLs, and PTL configuration objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Portal URLs, hosted browser URLs, checkout URLs, session replay links, and draft demo scripts that require user review before deployment.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

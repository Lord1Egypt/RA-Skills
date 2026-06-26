## Description: <br>
Use the OpenClaw-managed browser for real website interaction, page operations, snapshots, clicks, typing, waits, screenshots, and tab control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haohao-ui](https://clawhub.ai/user/haohao-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate real websites through an OpenClaw-managed browser when tasks require page navigation, clicking, typing, screenshots, tab control, or stateful browser profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser actions can affect logged-in pages, forms, downloads, uploads, or account state. <br>
Mitigation: Use a dedicated or task-specific browser profile for normal work, and supervise any use of the user's live profile. <br>
Risk: Screenshots, snapshots, request inspection, cookies, storage, and downloaded files can expose sensitive page data. <br>
Mitigation: Limit the skill to tasks that require real browser operation, keep sessions isolated by profile, and review captured browser data before sharing or retaining it. <br>


## Reference(s): <br>
- [OpenClaw Browser on ClawHub](https://clawhub.ai/haohao-ui/haohao-ui-openclaw-browser) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is intended to be applied through OpenClaw browser tools or the OpenClaw browser CLI with an explicit browser profile.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

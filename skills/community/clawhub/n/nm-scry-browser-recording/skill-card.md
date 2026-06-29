## Description: <br>
Records browser sessions via Playwright and converts video to GIF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation teams use this skill to run Playwright-based browser recordings for web UI tutorials and demos, locate WebM output, and convert recordings to GIF when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser recordings can capture sensitive application data and save WebM or GIF artifacts locally. <br>
Mitigation: Use sanitized test accounts and non-production data, review generated media before sharing, and delete output directories when no longer needed. <br>
Risk: The skill is intended for explicit browser demo recording tasks and may be overly broad if invoked for unrelated browser work. <br>
Mitigation: Invoke it only for deliberate recording workflows and narrow triggers or task wording where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scry-browser-recording) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scry) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell command and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent through Playwright validation, recording execution, WebM output discovery, and optional GIF conversion.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

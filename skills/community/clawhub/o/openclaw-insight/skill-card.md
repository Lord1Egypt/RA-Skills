## Description: <br>
Analyze OpenClaw AI assistant usage patterns and generate interactive insight reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linsheng9731](https://clawhub.ai/user/linsheng9731) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to analyze local OpenClaw session history, estimate usage and cost, identify friction patterns, and generate HTML or JSON reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recommended install path runs a remote shell script before the user has reviewed the installer. <br>
Mitigation: Download and inspect the installer first, and verify release checksums or signatures when available. <br>
Risk: The skill analyzes local OpenClaw session history, which may include sensitive usage details in generated reports. <br>
Mitigation: Keep generated reports local by default and review report contents before sharing them. <br>


## Reference(s): <br>
- [OpenClaw Insight on ClawHub](https://clawhub.ai/linsheng9731/openclaw-insight) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and references to local HTML or JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local HTML or JSON report files through the openclaw-insight CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

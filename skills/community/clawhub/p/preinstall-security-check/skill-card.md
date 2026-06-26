## Description: <br>
Pre-installation security assessment for ClawHub skills. Run before any skill install. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marianachow0321](https://clawhub.ai/user/marianachow0321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to assess ClawHub skills before installation, review risk signals, and decide whether to proceed with an install. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may rely on the skill as a replacement for the platform's normal install confirmation flow. <br>
Mitigation: Keep the platform's normal install confirmation flow enabled and use this skill as an additional review step. <br>
Risk: A security report may be incomplete or misleading if metadata is unavailable or the skill under review cannot be fetched. <br>
Mitigation: Cancel or defer installation when required metadata cannot be reviewed, and verify findings against the source artifact before proceeding. <br>
Risk: The skill may execute review or sandbox steps outside the user's intended install-review workflow. <br>
Mitigation: Run it only when intentionally reviewing a ClawHub or OpenClaw skill before installation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/marianachow0321/preinstall-security-check) <br>
- [Project homepage](https://github.com/marianachow0321/openclaw-preinstall-security-check) <br>
- [Risk Scoring Reference](references/risk-scoring.md) <br>
- [Sandbox Testing Procedure](references/sandbox-procedure.md) <br>
- [Report Templates](references/report-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security report with verdict, findings, and install guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured sandbox findings and explicit user confirmation prompts before installation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Manage Jotform forms, submissions, labels, and user accounts. Create and clone forms, retrieve submissions and reports, manage form labels, and monitor account usage and settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to work with Jotform forms, submissions, labels, reports, and account settings through a connected Jotform account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Jotform account through ClawLink and uses sensitive credentials. <br>
Mitigation: Install only when comfortable connecting the account through ClawLink, and verify the active Jotform integration before making tool calls. <br>
Risk: Write actions can change labels, user settings, or clone forms in the connected account. <br>
Mitigation: Preview and confirm the target resource and intended effect before executing write operations. <br>
Risk: Jotform submissions and account settings can contain personal or sensitive information. <br>
Mitigation: Handle returned data according to applicable data policies and limit requests to the user's stated task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/jotform-forms) <br>
- [Jotform API Documentation](https://api.jotform.com/docs/) <br>
- [Jotform Form Management](https://www.jotform.com/form-management/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ClawLink tool calls against the live Jotform catalog; write operations should be previewed and confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

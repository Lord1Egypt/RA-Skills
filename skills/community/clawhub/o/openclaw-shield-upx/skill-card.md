## Description: <br>
Security monitoring and threat detection for OpenClaw agents, using the OpenClaw Shield plugin to check health, inspect events, review redaction-vault context, and manage security cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunopradof](https://clawhub.ai/user/brunopradof) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw agent activity, inspect Shield health and logs, triage security cases, and guide remediation decisions through the Shield plugin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Shield plugin and sends redacted agent activity telemetry to UPX. <br>
Mitigation: Install only when the organization accepts that data flow and review the plugin privacy details before activation. <br>
Risk: The Shield installation key is sensitive configuration. <br>
Mitigation: Treat the installation key as a secret and avoid exposing it in chat, logs, or shared artifacts. <br>
Risk: Shield logs can contain sensitive diagnostic details such as file paths, commands, URLs, or investigation context. <br>
Mitigation: Summarize findings instead of sharing raw log values, unless the user explicitly requests raw content for the current investigation. <br>
Risk: Case close or resolve actions change the state of security investigations. <br>
Mitigation: Confirm the intended resolution with the user before closing or resolving a case. <br>
Risk: Optional local data deletion removes Shield history and redaction-vault lookup data. <br>
Mitigation: Run deletion only when intentionally removing Shield history and after checking retention needs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brunopradof/openclaw-shield-upx) <br>
- [UPX Shield Plugin](https://www.npmjs.com/package/@upx-us/shield) <br>
- [OpenClaw Shield Trial](https://www.upx.com/en/lp/openclaw-shield-upx) <br>
- [UPX Dashboard](https://uss.upx.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise security case summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should avoid raw diagnostic log values unless the user explicitly asks for them in the current session.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

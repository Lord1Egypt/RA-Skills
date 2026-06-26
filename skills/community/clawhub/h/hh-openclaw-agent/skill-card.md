## Description: <br>
HH OpenClaw Agent helps prepare reviewed hh.ru application packets, execute logged-in browser application flows through OpenClaw, and produce auditable submission bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to prepare, review, execute, and document an hh.ru job application workflow in OpenClaw, with a machine-readable packet, step log, bundle check, and shareable report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live application could be submitted before the packet content is approved. <br>
Mitigation: Require packet review status to be approved before treating a browser run as submitted or counting the bundle as complete. <br>
Risk: Application packets, browser notes, screenshots, or reports may contain sensitive application details or authentication context. <br>
Mitigation: Use only the intended hh.ru browser profile, stop for login, CAPTCHA, passkey, or 2FA challenges, avoid cookies, tokens, and secrets in notes or artifacts, and share the default redacted report unless a full export is intentionally required. <br>
Risk: Blocked or failed browser runs can be difficult to audit without durable evidence. <br>
Mitigation: Record expected and actual results for meaningful steps, include screenshots for failed or blocked steps, and run the bundle checker before handoff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/hh-openclaw-agent) <br>
- [Project homepage](https://github.com/zack-dev-cm/hh-openclaw-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/Markdown file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local application packet JSON, execution-log entries, bundle-check JSON, and a redacted Markdown report; full sensitive report export is opt-in.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

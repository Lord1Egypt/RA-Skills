## Description: <br>
Manage terminal notifications with scheduling, filtering, and delivery tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and terminal users can use this skill for local command-line notification-style logging, search, status checks, and exports. Review it as a local logging utility rather than a functional notification delivery system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is presented as a notification manager, but the authoritative security summary says it mainly stores arbitrary command text in local log files rather than sending or tracking notifications. <br>
Mitigation: Treat it as a local logging utility and verify any actual notification delivery or alerting requirements outside this skill. <br>
Risk: Command text may be stored under ~/.local/share/notification and may be exported later. <br>
Mitigation: Do not pass secrets, private messages, operational alerts, tokens, or sensitive identifiers to its commands unless local storage and later export are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/notification) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create, query, search, and export local log files under ~/.local/share/notification.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

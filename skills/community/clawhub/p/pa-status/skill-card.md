## Description: <br>
Pa Status generates PA network health reports from data/pa-directory.json, checking PA activity, billing, calendar connection, and status fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Administrators and operators use this skill to monitor a PA network, generate daily or on-demand status reports, and identify billing, calendar, inactive, or reachability issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PA directory contains operational and contact data used to produce status reports. <br>
Mitigation: Secure data/pa-directory.json and install the skill only for maintaining a PA network dashboard from a local directory. <br>
Risk: Optional WhatsApp reachability pings may contact PAs unexpectedly. <br>
Mitigation: Require admin confirmation before pings and confirm PAs have consented to reachability checks. <br>
Risk: The documented script does not fully incorporate last_seen and calendar_connected into the health classification. <br>
Mitigation: Update the script so last_seen and calendar_connected affect health results before relying on it for operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/pa-status) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, JSON, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a human-readable PA status report and operational guidance for optional scoped reachability checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

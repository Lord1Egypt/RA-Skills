## Description:

PA network health dashboard for checking active PAs, billing status, calendar connections, and network status reports from data/pa-directory.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Administrators and PA network operators use this skill to generate daily, event-triggered, or on-demand health reports that identify active assistants, billing issues, calendar connection state, and offline entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status reports can be misleading when PA directory fields such as last_seen, calendar_connected, billing_error, or status are stale or incomplete.

Mitigation: Treat generated reports as advisory and validate the directory data before acting on the report.

Risk: WhatsApp reachability checks or distributed status reports can contact assistants without proper authorization.

Mitigation: Install and use the skill only where PA directory access and WhatsApp checks are authorized, and require explicit confirmation before sending pings or distributing reports.

Risk: Broad pings can create unnecessary operational noise or rate-limit pressure.

Mitigation: Ping only PAs already flagged in the issues list and avoid pinging healthy PAs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python and JSON snippets for status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory PA health reports from local directory data; pings and report distribution require operator confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

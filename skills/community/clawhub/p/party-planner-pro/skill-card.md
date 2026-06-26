## Description: <br>
Party Planner Pro helps an agent plan events by organizing guest lists, budgets, menus, timelines, vendors, day-of logistics, and post-event wrap-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People planning private, social, or team events use this skill to coordinate event details, guest needs, spending, schedules, vendors, and follow-up tasks. Agents can also use its helper scripts and structured templates to export plans and generate budget reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Guest contact details, dietary needs, addresses, vendor information, and budget data can be sensitive. <br>
Mitigation: Share only the event details needed for planning and treat exported reports as private. <br>
Risk: Setup and helper scripts can create or modify local planning files. <br>
Mitigation: Install only from a trusted copy, inspect setup commands before execution, and back up data before uninstalling. <br>
Risk: Event details discussed with an agent may remain in the host platform's chat or session context. <br>
Mitigation: Review the host agent platform's data retention controls and use appropriate local storage protections for sensitive event data. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nollio/party-planner-pro) <br>
- [README](artifact/README.md) <br>
- [Security notes](artifact/SECURITY.md) <br>
- [Codex security audit](artifact/CODEX-SECURITY-AUDIT.md) <br>
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational guidance with structured JSON event data, Markdown exports, and optional generated budget reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May handle guest, dietary, venue, vendor, and budget details that should be treated as private.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

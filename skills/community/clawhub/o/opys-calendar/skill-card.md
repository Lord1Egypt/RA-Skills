## Description: <br>
A local markdown-backed calendar with CLI and optional two-way Google Calendar sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[21J3phy](https://clawhub.ai/user/21J3phy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, external users, and agents use this skill to inspect and update a local Markdown-backed schedule, manage events through a CLI, and optionally synchronize with Google Calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled calendar and sync-state files may contain private schedule data. <br>
Mitigation: Review and clean bundled calendar and state files before installation or sharing, and treat calendar.md as private data. <br>
Risk: Optional Google Calendar sync can grant calendar access to the local server. <br>
Mitigation: Connect a Google account only after reviewing the OAuth configuration and trusting the local server. <br>
Risk: Broad unauthenticated local mutation APIs can alter calendar data if exposed. <br>
Mitigation: Run the service bound to localhost with restricted CORS and authentication before allowing browser or agent access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/21J3phy/opys-calendar) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples and calendar-state file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local Markdown calendar data and write rolling agent snapshots.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

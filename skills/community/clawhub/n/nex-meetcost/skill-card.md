## Description: <br>
Meeting cost calculator. See what meetings actually cost in billable time. Per-attendee rates by role, recurring meeting projections (weekly/monthly/yearly), cost-per-type breakdowns. Python stdlib only, SQLite storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and teams use this skill to estimate and log meeting costs from attendee roles, custom hourly rates, duration, meeting type, and recurrence. It helps compare one-off and recurring meeting costs while storing data locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script creates local directories, initializes a SQLite database, and installs a CLI wrapper in the user's home directory. <br>
Mitigation: Review the setup script before running it and install only in an environment where creating local files and a user-level command wrapper is acceptable. <br>
Risk: Meeting titles, attendee names, roles, hourly rates, notes, and cost history may reveal sensitive compensation, billing, or operational information. <br>
Mitigation: Keep the local SQLite database and exports in protected storage, avoid entering sensitive details that are not needed, and review exported JSON or CSV files before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-meetcost) <br>
- [Nex AI website](https://nex-ai.be) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local CLI guidance and meeting cost calculations; the installed tool can export logged meetings as JSON or CSV.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

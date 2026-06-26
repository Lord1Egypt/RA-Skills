## Description: <br>
Create, list, and cancel Microsoft Teams online meetings with calendar invites through Microsoft Graph API using a Microsoft 365 account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pingukim225](https://clawhub.ai/user/pingukim225) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents supporting them use this skill to schedule Microsoft Teams meetings, inspect upcoming Teams-enabled calendar events, and cancel meetings from a Microsoft 365 calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth credentials and delegated Microsoft Graph permissions that can create and modify calendar events and Teams meetings. <br>
Mitigation: Install only with a Microsoft app registration you control and grant the minimum required delegated permissions for the intended account or tenant. <br>
Risk: The release evidence reports a missing setup.py despite documentation that references it, and first use can install unpinned Python packages. <br>
Mitigation: Confirm or supply the setup workflow before use and install reviewed, pinned dependencies in a controlled Python environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pingukim225/ms-teams-meetings) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, lists, and cancels calendar-backed Teams meetings through Microsoft Graph after OAuth authentication.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

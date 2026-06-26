## Description: <br>
Provides a real-time dashboard to visualize AI agent project progress, decision trees, and test results, with commands to manage and configure the dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sakilmostak](https://clawhub.ai/user/sakilmostak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install, start, stop, configure, export, and import a local PM Dashboard for tracking AI agent project status, implementation progress, decision trees, and test results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install and run the external npm CLI @reghoul/pm-dashboard. <br>
Mitigation: Verify the npm package and publisher before installation, and install it only in environments where running that CLI is acceptable. <br>
Risk: The dashboard starts a local server and persists configuration, database, and log files under ~/.openclaw/pm-dashboard/. <br>
Mitigation: Start the dashboard only when a local server is intended, and remove ~/.openclaw/pm-dashboard/ when the saved configuration, database, or logs are no longer wanted. <br>


## Reference(s): <br>
- [ClawHub PM Dashboard skill page](https://clawhub.ai/sakilmostak/pm-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands install and operate an external npm CLI and preserve local state under ~/.openclaw/pm-dashboard/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Harvest helps agents read and manage Harvest users, clients, projects, tasks, assignments, and time entries through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams with connected Harvest and OOMOL accounts use this skill to inspect Harvest records and perform time-entry workflows without handling raw credentials. It supports read actions as well as confirmed create, update, stop, restart, and delete operations for time entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, stop, restart, or delete Harvest time entries. <br>
Mitigation: Review the exact payload and user-visible effect before approving write operations, and require explicit approval for destructive actions. <br>
Risk: The skill operates through the local oo CLI and can depend on installer or account-connection state. <br>
Mitigation: Verify the CLI installer before running it, use setup commands only after authentication or connection failures, and confirm the Harvest account connection before retrying. <br>


## Reference(s): <br>
- [Harvest on ClawHub](https://clawhub.ai/oomol/oo-harvest) <br>
- [Harvest homepage](https://www.getharvest.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before actions; state-changing and destructive operations require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

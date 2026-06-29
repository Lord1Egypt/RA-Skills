## Description: <br>
ClickHouse (clickhouse.com). Use this skill for ANY ClickHouse request -- searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to inspect ClickHouse database structure and run SQL against an OOMOL-connected ClickHouse account through the oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The execute_query action may be able to change or delete ClickHouse data. <br>
Mitigation: Require explicit review of execute_query payloads before execution unless the connected account or backend is known to enforce read-only queries. <br>
Risk: The skill operates through a connected OOMOL account with server-side credentials. <br>
Mitigation: Install and use it only with ClickHouse accounts where agent-run SQL is acceptable, and prefer least-privilege or read-only database access when possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-clickhouse) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClickHouse](https://clickhouse.com) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [ClickHouse Service Icon](https://static.oomol.com/logo/third-party/clickhouse.svg) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, SQL, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, text, and JSON-oriented command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and meta.executionId when actions are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

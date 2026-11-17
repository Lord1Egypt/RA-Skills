## Description:

MEC platform CLI for generating and validating Hive SQL from natural-language requests, creating and executing SQL tasks, querying task status and results, and running batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dylanjor](https://clawhub.ai/user/dylanjor)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and operations teams use this skill to turn MEC analytics requests into Hive SQL workflows, submit or monitor MEC SQL tasks, and retrieve structured task outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles MEC account credentials and persists access tokens locally.

Mitigation: Use a dedicated low-privilege MEC account, avoid passing real passwords on the command line, and protect or remove ~/.minglue/tokens.json after use.

Risk: Bot and auto-perform flows can submit backend SQL work orders.

Mitigation: Run auto-perform only when task submission is intended, and review the generated SQL, customer, brand, and date parameters before execution.

Risk: Generated SQL may be incorrect or misleading even when it passes the built-in statistical SQL guard.

Mitigation: Keep the SQL guard and backend validation enabled, then inspect task status, errors, and result outputs before relying on the data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dylanjor/skills/mec-aisql-cli)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [MEC task management endpoint](https://mec.miaozhen.com/taskmng)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, SQL snippets, and JSON task outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger authenticated MEC API calls and backend SQL task execution when users run auto-perform workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact pyproject.toml reports 0.3.3 and CHANGELOG reports 0.3.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

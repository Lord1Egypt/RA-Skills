## Description: <br>
Connect to and explore PostgreSQL, MySQL, SQLite, MongoDB, and Redis databases by running queries, inspecting schemas, exporting data, and diagnosing database issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect to supported databases, inspect schemas, run bounded diagnostic queries, export query results, and troubleshoot database issues from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes high-impact restore, import, migration, dump, and export workflows that can affect production data or expose sensitive data if run without clear scoping. <br>
Mitigation: Before any export, backup, restore, import, migration, or write operation, require the exact command, confirm the target database and environment, choose a protected destination path, and avoid production unless explicitly intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/lrg913427-db-explorer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lrg913427-dot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes database connection guidance, schema exploration steps, export workflows, diagnostic queries, and safety checks.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

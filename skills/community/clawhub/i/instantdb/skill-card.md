## Description: <br>
Provides InstantDB admin operations and real-time subscriptions for querying, mutating, linking, and monitoring app data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ubyjerome](https://clawhub.ai/user/ubyjerome) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to administer InstantDB apps, perform entity and relationship operations, run queries, and publish real-time status updates for human monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live-database authority, including update, delete, unlink, and transaction operations. <br>
Mitigation: Install only for intended InstantDB administration, protect the admin token as a secret, use a test or least-privileged environment where possible, and require explicit human approval before mutating important data. <br>
Risk: Queries and real-time subscriptions can expose data from the configured InstantDB app. <br>
Mitigation: Scope queries and namespaces to the task at hand and avoid connecting the skill to sensitive production data without prior review. <br>


## Reference(s): <br>
- [InstantDB Documentation](https://www.instantdb.com/docs) <br>
- [InstantDB Admin SDK](https://www.instantdb.com/docs/admin) <br>
- [InstantDB Query Syntax Reference](references/query_syntax.md) <br>
- [InstantDB Transaction Patterns](references/transactions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets, shell commands, and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an InstantDB app ID and admin token; mutating commands affect the configured app.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

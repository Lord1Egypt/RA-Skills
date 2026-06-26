## Description: <br>
Hizal Search helps agents retrieve prior Hizal context, including semantic search results, exact query-key lookups, scoped reads, compactions, and version history, before starting work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkerscobey](https://clawhub.ai/user/parkerscobey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to consult existing project, agent, and organization context before code search, research, or implementation work so prior decisions and conventions inform the next task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic activation may cause agents to query agent memory or organization-wide context without clear user control. <br>
Mitigation: Narrow activation to explicit prior-context requests, default to project scope, and require approval before AGENT memory or ORG-wide searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkerscobey/hizal-search) <br>
- [Publisher profile](https://clawhub.ai/user/parkerscobey) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline Hizal tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only context search and retrieval guidance covering semantic search, query_key lookup, scoped reads, compaction, and version history inspection.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

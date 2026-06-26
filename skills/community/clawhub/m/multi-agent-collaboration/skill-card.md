## Description: <br>
Multi Agent Collaboration helps agents coordinate multi-agent work with typed memory retrieval, role-based coordination, evidence-focused verification, command safety checks, and cost observability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e2e5g](https://clawhub.ai/user/e2e5g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add structured multi-agent collaboration, memory retrieval, verification, safety auditing, and cost tracking to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and personal or workflow profiling may retain sensitive context beyond a single task. <br>
Mitigation: Review and restrict the memory directory, avoid entering secrets or sensitive personal details, and use a sandboxed or test namespace until retention and deletion behavior is clearly documented. <br>
Risk: Broad social and content monitoring capabilities are present but not fully disclosed in the main description. <br>
Mitigation: Review the included prompts and module documentation before deployment, and enable only the modules that are appropriate for the intended use case. <br>


## Reference(s): <br>
- [Claude Grade Patterns](references/claude-grade-patterns.md) <br>
- [Multi-Agent Workflow Design](references/workflow-design.md) <br>
- [Module Data Flow](references/data-flow.md) <br>
- [Claude Grade Runbook Template](assets/templates/claudegrade-runbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/e2e5g/multi-agent-collaboration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JavaScript examples, JSON-like workflow data, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persistent memory records, verification results, safety audit decisions, and cost or cache observations.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

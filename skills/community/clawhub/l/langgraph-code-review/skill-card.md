## Description:

Reviews LangGraph code for bugs, anti-patterns, and improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review LangGraph projects for state-management, graph-structure, checkpointing, tool-integration, and async-pattern issues with cited source evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review guidance can produce incorrect or misleading findings if the agent does not ground each claim in the reviewed code.

Mitigation: The skill requires same-turn quotation of the exact code artifact and file location before any bug, anti-pattern, or improvement is reported.

Risk: The skill directs the agent to inspect LangGraph project files, so review output may quote sensitive source snippets from the user's repository.

Mitigation: Use the skill only in authorized review scopes and keep quoted evidence minimal, limited to the code needed to substantiate each finding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/langgraph-code-review)
- [Publisher profile](https://clawhub.ai/user/anderskev)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review findings with cited file paths, line numbers, quoted code evidence, and checklist status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires same-turn source quotation before issuing review findings.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

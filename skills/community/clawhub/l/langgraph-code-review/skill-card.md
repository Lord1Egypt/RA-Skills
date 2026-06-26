## Description: <br>
Reviews LangGraph code for bugs, anti-patterns, and improvements across StateGraph usage, nodes, edges, checkpointing, state management, graph structure, and async patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review LangGraph implementations for state-management, graph-structure, checkpointing, async, tool-integration, and persistence issues. It guides reviewers to cite freshly read source artifacts before issuing findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative scan marks the release suspicious because related maintainer workflows can run nested review agents with full local access or perform admin moderation actions. <br>
Mitigation: Install only when those maintainer or operator workflows are needed, disable full-access autoreview where possible, and use moderation workflows only with intended staff credentials, explicit targets, and a clear reason. <br>
Risk: Code review guidance can produce incorrect or misleading findings if it relies on context rather than the reviewed source. <br>
Mitigation: Require each finding to quote the freshly read source artifact and include file and line evidence before making the claim. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown code review findings with file and line citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings must quote the relevant same-turn source artifact before making a claim.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

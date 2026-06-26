## Description: <br>
Parallel Responder helps an agent classify requests by complexity, estimate response time, choose direct or parallel execution, and report progress while longer work continues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsa03](https://clawhub.ai/user/lsa03) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users can use this skill to make longer agent tasks more transparent by returning immediate status, estimating duration, and issuing progress updates for medium and complex work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad automated task handling, including installs, deletes, restarts, file writes, and child-agent workflows without clear permission boundaries. <br>
Mitigation: Require explicit user approval before installs, deletes, restarts, sub-agent launches, or file writes. <br>
Risk: Background-style execution and progress reporting can obscure what context is shared with child agents and when work should stop. <br>
Mitigation: Document allowed shared context, write locations, cancellation behavior, and cleanup expectations before using the skill for complex tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lsa03/parallel-responder) <br>
- [Publisher profile](https://clawhub.ai/user/lsa03) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown progress messages with JSON task classification and execution metadata from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose immediate replies, time estimates, task IDs, progress percentages, and completion summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Coordinate and manage multiple AI agents working together on complex tasks, including orchestration, communication patterns, and workflow management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuyu28](https://clawhub.ai/user/zhuyu28) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to decompose complex work into agent-specific tasks, track progress, coordinate handoffs, and aggregate results across a multi-agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions and results may be saved in a local JSON session file. <br>
Mitigation: Avoid putting secrets or sensitive personal data into coordination sessions unless the storage location is controlled and the file is cleaned up when no longer needed. <br>
Risk: Coordinated agent outputs may become stale, inconsistent, or blocked if task status is not actively maintained. <br>
Mitigation: Review session status regularly, define clear handoffs, and update failed or completed tasks before using aggregated results. <br>


## Reference(s): <br>
- [Multi-Agent Coordination Patterns](references/coordination_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional Python command-line usage and JSON session state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local coordination session JSON file when the bundled script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

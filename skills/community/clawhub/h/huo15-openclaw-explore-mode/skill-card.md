## Description: <br>
Guides an agent through read-only, systematic exploration of a codebase, system, or topic before answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need a structured investigation of an unfamiliar codebase, implementation, or bug before deciding what to do next. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface repository paths, line numbers, implementation details, or other sensitive context from repositories or systems the user asks it to explore. <br>
Mitigation: Use it only on workspaces whose contents may be summarized, and avoid using it on repositories or systems containing secrets that should not appear in reports. <br>
Risk: Exploration findings may include incomplete inferences if relevant files or history are missed. <br>
Mitigation: Cross-check multiple relevant files, distinguish observed facts from inference, and review the report before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-explore-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown report with file paths, line references, findings, answers, and optional recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only exploration; may include observed facts, clearly labeled inferences, and repository path references.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Applies modular monolith with enforced internal boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and architects use this skill to plan modular monolith boundaries, public contracts, and enforcement checks for large codebases that need team autonomy without distributed-system overhead. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture guidance may not match a project's domain boundaries or current operational constraints. <br>
Mitigation: Review the skill guidance against the target codebase and have architecture owners confirm module boundaries before adoption. <br>
Risk: Weak enforcement can allow modular monolith boundaries to erode over time. <br>
Mitigation: Use automated dependency checks and CI jobs to fail builds when forbidden module dependencies are introduced. <br>
Risk: Shared database ownership can create coupling and performance hotspots. <br>
Mitigation: Define schema ownership and restrict cross-module data access through documented contracts or controlled views. <br>


## Reference(s): <br>
- [claude-night-market archetypes](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with structured architecture steps, deliverables, and troubleshooting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no tool calls, credentials, or hidden execution were identified in server security evidence.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

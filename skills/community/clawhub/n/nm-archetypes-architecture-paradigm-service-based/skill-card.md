## Description: <br>
Applies coarse-grained service architecture for deployment independence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and architects use this skill to assess when coarse-grained service-based architecture fits systems that need deployment independence without full microservice autonomy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may influence architecture decisions toward service-based architecture even when project constraints favor a monolith, microservices, or another pattern. <br>
Mitigation: Review the skill's when-to-use and when-not-to-use guidance against team size, latency constraints, database ownership, and deployment requirements before adopting the pattern. <br>
Risk: Shared databases can create coupling between services and make changes cascade across teams. <br>
Mitigation: Assign schema or table ownership, gate breaking changes through review, and use views, replication, or schema deprecation schedules to manage change. <br>
Risk: Weak service and data governance can turn a service-based system into a distributed monolith. <br>
Mitigation: Define service contracts, enforce ownership boundaries, track coupling metrics, and maintain runbooks for deployments, rollbacks, and dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-service-based) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with architecture recommendations, adoption steps, deliverables, and risk mitigations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, persistence, credential use, or hidden data handling reported by security evidence.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Applies microservices for independent deployment and per-service scaling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and architecture teams use this skill to assess when a microservices architecture is appropriate and to plan service boundaries, platform requirements, observability, resilience, governance, and delivery practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad architecture triggers may cause the skill to be invoked for general scalability or architecture questions and bias advice toward microservices. <br>
Mitigation: Check the skill's own "When NOT to Use" guidance and validate organizational maturity, team size, platform capacity, and consistency requirements before applying the pattern. <br>
Risk: Microservices recommendations can add operational complexity, distributed data consistency challenges, and over-splitting risk. <br>
Mitigation: Require architecture review, explicit bounded contexts, observability and incident-response readiness, contract testing, and a documented rollback or consolidation path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-microservices) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with architecture checklists and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only guidance; no executable tools, MCP servers, API keys, or shell commands are required by the artifact.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

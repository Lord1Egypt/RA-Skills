## Description: <br>
Applies layered n-tier architecture with enforced boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and architecture reviewers use this skill to decide when layered n-tier architecture fits a moderate system and to produce guidance for layer boundaries, dependency direction, enforcement, and ADR or diagram deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may activate the skill during general architecture or domain-design discussions. <br>
Mitigation: Confirm that the user wants layered architecture guidance before applying the paradigm, or tighten trigger wording for narrower activation. <br>
Risk: Layered architecture can be a poor fit for systems needing independent component scaling, independent team deployments, frequent cross-layer business flows, or low-latency real-time processing. <br>
Mitigation: Check those constraints before recommending the paradigm and consider another architecture when they dominate the system requirements. <br>
Risk: Strict layers can become rigid or leaky when teams bypass dependency rules for expedience. <br>
Mitigation: Document allowed dependencies in an ADR, maintain dependency diagrams, and enforce layer rules with automated architecture checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-layered) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance for architecture decisions, layer definitions, dependency rules, enforcement checks, and risk mitigations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only skill; security evidence reports no code execution or data access behavior.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

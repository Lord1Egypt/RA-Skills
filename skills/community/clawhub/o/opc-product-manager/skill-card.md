## Description: <br>
Generates build-ready product specs for solo entrepreneurs from short product ideas, including MVP scope, tech stack recommendations, data models, API sketches, and agent handoff guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeonFJR](https://clawhub.ai/user/LeonFJR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo entrepreneurs and builders use this skill to turn rough product ideas or existing PRDs into concise, AI-agent-executable specs, scope checks, stack recommendations, and handoff documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save product specs and metadata locally, which may include sensitive product plans or business context. <br>
Mitigation: Use a dedicated products directory and review generated files before sharing them or handing them to another agent. <br>
Risk: Cross-skill linkage can read or reference landing-page, contract, or invoice records without clear user scoping. <br>
Mitigation: Require explicit approval before reading or linking related business records, and limit access to the records needed for the current product spec. <br>


## Reference(s): <br>
- [OPC Product Manager on ClawHub](https://clawhub.ai/LeonFJR/opc-product-manager) <br>
- [Tech Stack Guide](references/tech-stack-guide.md) <br>
- [User Story Patterns](references/user-story-patterns.md) <br>
- [Scope Assessment](references/scope-assessment.md) <br>
- [Product Metadata Schema](templates/product-metadata-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown specs with JSON metadata and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local product spec, metadata, handoff, and index files when archive modes are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Converts PRDs and business requirements into AI-friendly DDD domain design documents in Markdown, including domain models, aggregate and entity design, ER diagrams, domain logic placement, and sequence or flow diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qitongfire](https://clawhub.ai/user/qitongfire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, product teams, and domain modelers use this skill to turn a PRD or business description into a structured DDD design document before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DDD designs may be incomplete, incorrect, or misaligned with implementation constraints. <br>
Mitigation: Review the generated design, diagrams, schema mappings, and cross-layer contracts before using them for implementation. <br>
Risk: PRDs can contain confidential product, customer, or business information. <br>
Mitigation: Use the skill only in an agent environment that is already trusted for the PRD contents, and avoid sharing confidential PRDs in untrusted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qitongfire/prd-to-ddd-design) <br>
- [Phase Guide](phase-guide.md) <br>
- [DDD Design Template](ddd-design-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Mermaid diagrams, tables, schema mappings, API contracts, and code-style type or method definitions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a docs/design/<feature-name>-ddd-design.md file when the agent has workspace write access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

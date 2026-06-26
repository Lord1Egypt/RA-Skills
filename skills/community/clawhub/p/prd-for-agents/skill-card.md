## Description: <br>
Produces agent-optimized Product Requirements Documents from a vision or idea, including success metrics, user stories, risks, dependencies, open questions, and a sequenced build order for AI coding or developer agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanketsao](https://clawhub.ai/user/sanketsao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, product managers, founders, and developers use this skill to turn a product vision or feature idea into a build-ready PRD for AI agents. It is also used to review existing PRDs for completeness and handoff readiness before a builder or developer agent starts implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PRDs can shape downstream agent plans even though the skill does not access or change the system directly. <br>
Mitigation: Review the generated PRD, assumptions, open questions, and Agent Build Order before allowing another agent to implement it. <br>
Risk: Broad routing in a multi-agent pipeline could select this PRD template for adjacent requirements-writing tasks. <br>
Mitigation: Confirm the task is a PRD, product requirements document, product spec, or feature spec before relying on the output. <br>


## Reference(s): <br>
- [PRD Sections Reference](references/prd-sections.md) <br>
- [PRD Examples Reference](references/prd-examples.md) <br>
- [ClawHub listing](https://clawhub.ai/sanketsao/prd-for-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown PRD with structured sections, checklists, tables, and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PRDs include quantitative metrics, user stories, acceptance criteria, open questions, assumptions, dependencies, risks, and an agent build order.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

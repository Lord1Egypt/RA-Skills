## Description: <br>
Design system architecture, evaluate patterns, and produce architecture artifacts for new or existing systems, including monolith and microservices choices, database or tech-stack decisions, diagrams, ADRs, dependency analysis, and scalability planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, software architects, and engineering teams use this skill to structure architecture decisions, review project design, create diagrams or ADRs, and identify dependency or coupling issues before implementation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect files in the project directory selected by the user. <br>
Mitigation: Run it only on the intended project folder, and avoid using it on broad locations such as a home directory, filesystem root, or folders containing unrelated secrets. <br>
Risk: The skill can write reports or diagrams when an output path is provided. <br>
Mitigation: Use explicit output paths only when you want a report or diagram written there. <br>


## Reference(s): <br>
- [Architecture Patterns Reference](references/architecture_patterns.md) <br>
- [System Design Workflows](references/system_design_workflows.md) <br>
- [Technology Decision Guide](references/tech_decision_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/felix-antonio-sl/kv-senior-architect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with architecture diagrams, ADRs, assessment reports, JSON reports, and shell command examples when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one primary architecture artifact per request; scripts may write a report or diagram when the user provides an explicit output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

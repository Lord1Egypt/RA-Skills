## Description: <br>
Generates Mermaid architecture and sequence diagrams and renders them as PNG files using Mermaid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpieTaylor911](https://clawhub.ai/user/OpieTaylor911) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn architecture, network, cloud, microservice, API, authentication, CI/CD, and data-flow descriptions into Mermaid diagram source and rendered PNG outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram contents are sent to the mermaid.ink external renderer by default, which may expose internal architecture, network, authentication, API, or data-flow details. <br>
Mitigation: Use the skill only for non-sensitive diagrams, or redact hostnames, service names, secrets, and internal topology before rendering; for sensitive diagrams, use a local Mermaid renderer instead. <br>


## Reference(s): <br>
- [Architecture diagram patterns](references/architecture-patterns.md) <br>
- [Sequence diagram patterns](references/sequence-patterns.md) <br>
- [mermaid.ink renderer endpoint](https://mermaid.ink/img/${ENCODED}?bgColor=white&width=2048) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with Mermaid source, shell commands, and saved .mmd/.png file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates Mermaid source and PNG diagram files under the configured diagrams workspace; uses mermaid.ink as the default renderer.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

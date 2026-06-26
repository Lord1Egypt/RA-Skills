## Description: <br>
Openclaw Design Consult helps agents act as senior product design system consultants that clarify requirements, make explainable design recommendations, and generate DESIGN.md plus CLAUDE.md design guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product teams, designers, and developers use this skill to have an agent assess project context, ask clarifying design questions, propose a coherent visual system, preview typography and colors, and update local design guidance files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local project context to infer product and design needs. <br>
Mitigation: Run it only in workspaces where README, package, source, and design-context reads are acceptable. <br>
Risk: Optional competitor research may browse external sites. <br>
Mitigation: Decline the research step when browsing is not appropriate for the project. <br>
Risk: Generated design guidance or file changes may introduce unwanted product direction. <br>
Mitigation: Review proposed DESIGN.md and CLAUDE.md changes before committing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/x-rayluan/openclaw-design-consult) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate an HTML preview and update DESIGN.md and CLAUDE.md when directed by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

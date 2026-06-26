## Description: <br>
Project Doc Analyst reads a software repository deeply and produces structured project documentation covering architecture, implementation details, design rationale, tradeoffs, complex topics, and diagrams for human and AI readers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z-zihan](https://clawhub.ai/user/z-zihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, architects, reviewers, and AI coding agents use this skill to analyze a target repository and generate self-contained project documentation for onboarding, architecture review, handoff, and future agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a chosen repository and may summarize sensitive source, configuration, or documentation content. <br>
Mitigation: Use it only on repositories approved for documentation generation, and avoid projects containing secrets or sensitive material unless that content may be included in generated docs. <br>
Risk: Generated project documentation can be incomplete or misleading if the repository evidence is incomplete or the target path is ambiguous. <br>
Mitigation: Specify the target repository and output directory clearly, then review generated documents against the repository before relying on them for architecture or handoff decisions. <br>


## Reference(s): <br>
- [Project Doc Analyst on ClawHub](https://clawhub.ai/z-zihan/project-doc-analyst) <br>
- [Awesome Skills repository](https://github.com/z-Zihan/awesome-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown documents with structured analysis and Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce multiple documentation files; output language follows the user request or project context.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

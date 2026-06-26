## Description: <br>
Recommends production-ready Golang libraries and frameworks. Apply when the user explicitly asks for library suggestions, wants to compare alternatives, needs to choose a library for a specific task, or when a new dependency is being added to the project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when choosing Go standard-library features, third-party libraries, frameworks, and development tools for production-oriented Go projects. It helps compare alternatives, prefer standard-library solutions when sufficient, and reason about dependency tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Library recommendations can introduce third-party dependencies with security, maintenance, license, or transitive dependency impact. <br>
Mitigation: Prefer the Go standard library when it satisfies the requirement, and review maintenance status, license, community adoption, and dependency footprint before adding a library. <br>
Risk: Go-related commands or project changes may affect the user's local workspace when acted on by an agent. <br>
Mitigation: Review the target project and command details before running high-impact workflows, especially when local tools or authenticated accounts may be used. <br>


## Reference(s): <br>
- [Golang Popular Libraries homepage](https://github.com/samber/cc-skills-golang) <br>
- [Standard Library - New & Experimental](references/stdlib.md) <br>
- [Top Go Libraries by Category](references/libraries.md) <br>
- [Go Development Tools](references/tools.md) <br>
- [Awesome Go](https://github.com/avelino/awesome-go) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with library recommendations, tradeoff analysis, and optional Go-related commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Go tooling such as go and golangci-lint when relevant.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

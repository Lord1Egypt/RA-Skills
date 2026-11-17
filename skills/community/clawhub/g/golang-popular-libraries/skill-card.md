## Description:

Recommends production-ready Golang libraries and frameworks. Apply when the user explicitly asks for library suggestions, wants to compare alternatives, needs to choose a library for a specific task, or when a new dependency is being added to the project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose Go standard-library features, third-party libraries, frameworks, and tooling for production Go projects. It emphasizes standard-library-first decisions, dependency maturity, maintenance status, license checks, and measured performance needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local project authority for an advisory workflow, including file editing, Go and Git commands, web lookup, and agent delegation.

Mitigation: Use it in a constrained session for advice and documentation lookup, and allow edits, commands, or delegation only when explicitly requested for project changes.

Risk: Library recommendations can introduce unnecessary, stale, poorly maintained, or vulnerable dependencies into a Go project.

Mitigation: Require standard-library consideration first, then verify maintenance status, license, import adoption, and known vulnerabilities before adding a dependency.

## Reference(s):

- [Skill homepage](https://github.com/samber/cc-skills-golang)
- [Standard Library - New & Experimental](references/stdlib.md)
- [Top Go Libraries by Category](references/libraries.md)
- [Go Development Tools](references/tools.md)
- [Awesome Go](https://github.com/avelino/awesome-go)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with inline Go snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include comparative recommendations, standard-library alternatives, dependency-vetting checks, and follow-up commands.]

## Skill Version(s):

1.2.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

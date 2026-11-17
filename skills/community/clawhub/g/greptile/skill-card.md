## Description:

Query, search, and manage repositories indexed by Greptile (AI codebase intelligence). Use when asking questions about a codebase, searching for code patterns, indexing repos for Greptile review, or checking Greptile index status. Requires GREPTILE_TOKEN and a GitHub/GitLab token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iahmadzain](https://clawhub.ai/user/iahmadzain)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to index repositories with Greptile, check indexing status, ask codebase questions, and search for relevant source files or snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends repository access tokens and repository context to Greptile API endpoints.

Mitigation: Use it only with repositories you are allowed to share with Greptile and prefer a fine-grained token dedicated to this integration.

Risk: The authoritative security evidence reports a command-injection flaw in the status command.

Mitigation: Fix or avoid the status command until the Python string construction is replaced with safe argument passing.

Risk: The skill depends on high-impact repository tokens with limited safeguards.

Mitigation: Scope tokens narrowly, rotate them regularly, and avoid using broad personal access tokens when a dedicated token is sufficient.

## Reference(s):

- [Greptile skill page](https://clawhub.ai/iahmadzain/skills/greptile)
- [Greptile app](https://app.greptile.com)
- [Greptile API endpoint](https://api.greptile.com/v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return AI-generated answers with source file references, ranked search results, repository indexing status, or Greptile API response JSON.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

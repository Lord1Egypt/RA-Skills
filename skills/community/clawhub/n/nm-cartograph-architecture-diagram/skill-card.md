## Description:

Generates a Mermaid architecture diagram showing high-level component relationships

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to understand and communicate high-level relationships among packages, plugins, and modules during onboarding, architecture documentation, and pull request reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagram workflow may send codebase architecture details to Mermaid Chart, which may expose sensitive information from a private or confidential repository.

Mitigation: Before use, check whether the renderer's data handling is acceptable for the repository and use local diagram output when external sharing is not permitted.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-cartograph-architecture-diagram)
- [Cartograph project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Code, Markdown]

**Output Format:** [Markdown containing Mermaid flowchart syntax and a brief description of the architecture diagram]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A high-level component map grouped by package; the skill guidance limits diagrams to 15–20 nodes and calls for at least 3 nodes.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

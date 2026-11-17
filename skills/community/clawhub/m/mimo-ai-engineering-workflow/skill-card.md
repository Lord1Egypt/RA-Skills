## Description:

Guides AI-assisted software projects through a five-gate engineering workflow covering design, planning, test-first implementation, incremental delivery, review, CI/CD, and technical debt management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure AI-assisted coding work into enforceable quality gates, with concrete outputs for design, implementation planning, test coverage, code review, CI/CD, and technical debt tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation terms around AI engineering workflows, which may cause it to influence tasks where a user only wants narrow coding help.

Mitigation: Installers who want narrower behavior should restrict trigger terms or invoke the skill explicitly.

Risk: The CI/CD example includes an audit-ci command that could be copied into a repository without dependency pinning or project-specific validation.

Mitigation: Pin or lock audit-ci and test the security-scan step against controlled project dependencies before adopting the example.

## Reference(s):

- [AI编程工程化 detailed reference](references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-ai-engineering-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown guidance with checklists, tables, and inline code or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are workflow artifacts such as design documents, execution plans, test plans, review reports, progress updates, TODO lists, and CI/CD examples.]

## Skill Version(s):

1.3.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

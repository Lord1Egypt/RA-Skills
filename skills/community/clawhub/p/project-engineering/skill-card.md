## Description:

Evidence-driven project engineering for greenfield software projects and existing repositories, guiding coding agents through architecture baselines, codebase discovery, cross-file development, refactoring, API/protocol/database changes, code review, testing, and delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubai00](https://clawhub.ai/user/liubai00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software engineering teams use this skill to guide coding agents through greenfield architecture, repository discovery, cross-file implementation, refactoring, review, testing, and delivery work. It helps agents separate confirmed facts, assumptions, current implementation, and verification evidence before making or recommending changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository inventory reports can expose repository paths, branch or commit metadata, and structural filenames.

Mitigation: Review and redact generated reports before sharing them outside the organization.

Risk: The skill can guide high-impact engineering changes, but invoking it does not itself authorize commits, pushes, migrations, deployments, production access, credential changes, or external writes.

Mitigation: Require explicit authorization for external operations and apply risk-proportionate human review and validation before acting on high-impact recommendations.

## Reference(s):

- [Project Engineering Homepage](https://github.com/liubai00/project-engineering)
- [ClawHub Skill Page](https://clawhub.ai/liubai00/skills/project-engineering)
- [Usage Guide](docs/USAGE.md)
- [Greenfield Workflow](references/greenfield.md)
- [Discovery Workflow](references/discovery.md)
- [Architecture Workflow](references/architecture.md)
- [Implementation Workflow](references/implementation.md)
- [Risk and Archetypes](references/risk-and-archetypes.md)
- [Delivery Workflow](references/delivery.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, file references, command suggestions, plans, review findings, and delivery reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository inventory summaries and risk-proportionate validation evidence; does not authorize commits, pushes, deployments, migrations, production access, or external writes.]

## Skill Version(s):

1.0.2 (source: release metadata and changelog, released 2026-08-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

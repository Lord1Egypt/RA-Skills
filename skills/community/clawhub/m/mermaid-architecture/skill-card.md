## Description:

Use when generating, documenting, or updating architecture diagrams, flowcharts, sequence, ER, class, or state diagrams using Mermaid in docs/architecture/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to generate, document, validate, and update Mermaid architecture diagrams and design documents in docs/architecture/.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may invoke an unpinned Mermaid CLI through npx when a local Mermaid CLI is unavailable.

Mitigation: Prefer a preinstalled or pinned Mermaid CLI before use.

Risk: Generated diagrams and documentation can be incomplete or misleading if the agent reads stale or partial repository context.

Mitigation: Review generated Mermaid source, exported images, and design documents before publishing or relying on them.

Risk: The workflow writes diagram artifacts and documentation into the target repository.

Mitigation: Keep generated outputs constrained to docs/architecture/ and review file changes before committing.

## Reference(s):

- [Architecture diagram guide](references/guides/diagrams/architecture-diagrams.md)
- [Sequence diagram guide](references/guides/diagrams/sequence-diagrams.md)
- [Activity diagram guide](references/guides/diagrams/activity-diagrams.md)
- [Deployment diagram guide](references/guides/diagrams/deployment-diagrams.md)
- [Mermaid diagram guide](references/mermaid-diagram-guide.md)
- [Troubleshooting guide](references/guides/troubleshooting.md)
- [Resilient workflow guide](references/guides/resilient-workflow.md)
- [Publisher skills repository](https://github.com/afonsoft/skills)
- [Metadata homepage](https://github.com/SpillwaveSolutions/design-doc-mermaid)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with Mermaid code blocks, optional .mmd source files, optional PNG or SVG exports, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs are intended to be kept under docs/architecture/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

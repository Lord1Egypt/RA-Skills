## Description:

Generates documentation from code. Creates API docs, README updates, architecture diagrams, and keeps documentation in sync with code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate API documentation, update README content, create simple architecture diagrams, and check whether project documentation is in sync with source code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation and README updates can introduce incorrect or unwanted repository changes.

Mitigation: Run the skill only in repositories approved for source scanning and documentation edits, then inspect diffs before committing generated files.

Risk: C/C++ support can load an optional c_parser module from a sibling c-support/lib directory.

Mitigation: Use the C/C++ path only when that sibling dependency is trusted, controlled, and reviewed.

Risk: The documented CI example commits and pushes generated documentation from a push workflow.

Mitigation: Use pull-request review, branch protection, or another approval gate before adopting automated documentation pushes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michealxie001/skills/oc-docgen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, Mermaid diagram text, status text, and repository file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated documentation files and update README content when invoked with output or README options.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Analyzes Oracle PL/SQL package files for a requested stored procedure, including upstream callers, downstream calls, data flow, mechanism notes, verified line references, and the procedure body.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsrun](https://clawhub.ai/user/johnsrun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database engineers, and application maintainers use this skill to inspect Oracle package files and understand stored procedure dependencies, data reads, call sites, and implementation details with workspace-relative Markdown links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes SQL package files supplied by the user, which may contain proprietary schema, business logic, or sensitive implementation details.

Mitigation: Run it only on files the user is permitted to share with the agent and avoid attaching SQL packages that contain secrets or unnecessary sensitive data.

Risk: Generated procedure names, dependency relationships, and line references may be incorrect; the evidence notes a target-name consistency issue in the included example.

Mitigation: Review the generated stored procedure names, call relationships, and every cited line link against the original package file before relying on the analysis.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/johnsrun/skills/plsql-package-analysis)
- [Example output](artifact/examples/examples_output.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report with dependency sections, mechanism analysis, clickable source links, and a procedure body code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses None for missing upstream or downstream procedures and requires exact workspace-relative line references.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

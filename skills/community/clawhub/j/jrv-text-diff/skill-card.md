## Description:

Compare two text files or strings side-by-side or unified. Highlights additions, deletions, and changes with color. Supports word-level diff, ignore-whitespace, and JSON/YAML structural diff modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare files, inline strings, code snippets, and JSON/YAML configuration data during review, auditing, editing, and CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Comparing untrusted files that contain terminal control characters may affect a sensitive terminal session.

Mitigation: Avoid comparing untrusted files in sensitive terminals; use no-color output or inspect content in a controlled environment when needed.

Risk: YAML structural diff mode depends on PyYAML being installed in the runtime environment.

Mitigation: Use a virtual environment with pinned dependencies before enabling YAML mode.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON, with optional ANSI-colored terminal diff output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports unified, context, side-by-side, word-level, JSON structural, and YAML structural diff output; exit codes distinguish identical inputs, differences, and errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

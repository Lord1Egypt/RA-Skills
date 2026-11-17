## Description:

Code uses a symbol that isn't imported, or imports a symbol that doesn't exist in the source module.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to diagnose missing or incorrect imports and to verify that newly referenced symbols are defined locally or exported by their source modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Import-fix guidance can be wrong if proposed symbols or modules are assumed instead of checked.

Mitigation: Verify each symbol against local definitions or module exports, then run the project's static checker before accepting changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline code identifiers and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable behavior is bundled; any checker commands should be reviewed in the local project context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

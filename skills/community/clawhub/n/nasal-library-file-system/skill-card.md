## Description:

Explains the input/output (IO) file handling, property serialization, and directory-path manipulation methods in Nasal, combining raw stream operations ('io') with high-level path parsing wrappers ('os.path').

This skill is ready for commercial/non-commercial use.

## Publisher:

[container32](https://clawhub.ai/user/container32)

### License/Terms of Use:

MIT-0

## Use Case:

Developers working with FlightGear Nasal use this skill as a reference for file streams, property tree XML serialization, and os.path directory/path operations. It helps them generate or review Nasal snippets that read, write, inspect, and manage files within FlightGear's security constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Nasal examples may write, truncate, rename, or delete files if paths are chosen incorrectly.

Mitigation: Review generated code and constrain file operations to the intended FlightGear export area, commonly $FG_HOME/Export/.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown prose with Nasal code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no tools, API calls, or shell commands are required by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

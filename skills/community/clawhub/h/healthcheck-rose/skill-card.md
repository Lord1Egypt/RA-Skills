## Description:

Track water and sleep with JSON file storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roseknife520](https://clawhub.ai/user/roseknife520)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to record water intake and sleep or wake events in a local JSON file and view simple daily totals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inline Node commands use user-derived cup counts in executable JavaScript without clear validation.

Mitigation: Parse and validate cup counts as numeric data before execution, and review generated commands before running them.

Risk: The skill stores water and sleep records as local personal health data in {baseDir}/health-data.json.

Mitigation: Keep the file in an appropriate local directory, limit access to it, and delete or archive it when no longer needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local health records to {baseDir}/health-data.json using Node.js built-in modules.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

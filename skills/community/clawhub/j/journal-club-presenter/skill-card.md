## Description:

Generate journal club slides with background, critique, and discussion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and academic teams use this skill to create bounded journal-club presentation outlines for lab meetings, graduate training, literature reviews, and critical appraisal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged script can overwrite arbitrary writable files when an unrestricted output path is supplied.

Mitigation: Choose an output path inside the intended workspace and avoid letting untrusted content control the --output argument until path validation and overwrite safeguards are added.

Risk: Journal-club outlines could overstate or drift beyond the source paper if the request lacks sufficient paper context.

Mitigation: Use the skill only for journal-club presentation outlines and keep assumptions, missing inputs, risks, and validation needs explicit in the final response.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/journal-club-presenter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured text or Markdown slide outline, optionally accompanied by local shell commands for validation and execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local outline file; output path should be constrained to the intended workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

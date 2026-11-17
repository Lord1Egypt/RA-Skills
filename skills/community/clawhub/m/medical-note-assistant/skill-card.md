## Description:

Automatically converts outpatient or inpatient medical records into structured summaries covering chief complaint, history, exam findings, assessment, treatment plan, and medication suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isaacloi1995-dot](https://clawhub.ai/user/isaacloi1995-dot)

### License/Terms of Use:


## Use Case:

Healthcare professionals can use this skill to draft structured summaries from authorized outpatient or inpatient records for qualified clinical review and editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive health records.

Mitigation: Use only records the user is authorized to process, remove direct identifiers where possible, and confirm that the workflow satisfies applicable privacy and compliance requirements.

Risk: The skill may produce diagnostic, treatment, or medication suggestions.

Mitigation: Treat outputs as draft support only and require review by a qualified clinician before clinical use.

Risk: The artifact does not state privacy, compliance, or clinical scope limits.

Mitigation: Add explicit privacy, compliance, and scope limits before using the skill in regulated healthcare workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/isaacloi1995-dot/skills/medical-note-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured medical-note summary in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include draft diagnostic, treatment, and medication suggestions that require qualified clinician review.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

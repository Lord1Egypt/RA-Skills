## Description:

Hiring Memory helps recruiting agents store, recall, and search candidate and interview context using BlueColumn persistent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and agents use this skill to add, retrieve, and search candidate notes and interview memories during hiring workflows. It is intended for environments with an approved BlueColumn API key and approved handling rules for recruiting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive candidate and interview information in an external memory service.

Mitigation: Use only with an approved BlueColumn account and approved recruiting-data handling rules; avoid storing unnecessary personal details, protected characteristics, compensation details, credentials, or confidential notes unless explicitly approved.

Risk: Stored hiring memories may be broadly recalled without clear controls or retention guidance.

Mitigation: Confirm who can recall records, how records are deleted or retained, and whether candidates and interviewers have appropriate notice or consent before use.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/hiring-memory)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key; stores and retrieves hiring context through BlueColumn endpoints.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

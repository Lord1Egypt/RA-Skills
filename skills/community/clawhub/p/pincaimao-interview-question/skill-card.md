## Description:

聘才猫（Pincaimao）面试出题大师 helps an agent call the Pincaimao Interview Question Master API to generate interview questions from a job description and candidate resume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

External hiring teams and recruiting agents use this skill to combine a job description with a candidate resume and request interview questions from Pincaimao.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads sensitive resumes and job descriptions to Pincaimao for processing.

Mitigation: Use it only when the user approves the upload and trusts Pincaimao to handle candidate and job data.

Risk: Uploaded files are stored remotely and returned storage keys should be treated as sensitive.

Mitigation: Avoid exposing returned storage keys and follow the publisher's data handling policy for uploaded files.

Risk: The skill requires an unspecified companion skill, `pincaimao-basic`, before use.

Mitigation: Verify the exact source and contents of `pincaimao-basic` before installing or loading it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pincaimao/skills/pincaimao-interview-question)
- [Pincaimao publisher profile](https://clawhub.ai/user/pincaimao)
- [Pincaimao homepage](https://www.pincaimao.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or raw API text, with shell command examples when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return organized interview questions by default, or raw API output when the user requests raw output.]

## Skill Version(s):

1.0.1 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

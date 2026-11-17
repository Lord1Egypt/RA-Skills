## Description:

Generates Pincaimao interview reports or coaching materials from a job description and interview recording using the Pincaimao API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and recruiting teams use this skill to upload an interview recording and job description to Pincaimao and receive a generated interview report or coaching material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interview recordings, job descriptions, and uploaded file identifiers are sent to Pincaimao for processing.

Mitigation: Install only if that data sharing is acceptable; confirm Pincaimao retention and deletion terms and treat returned COS keys as sensitive.

Risk: The Pincaimao API key can authorize uploads and report generation if exposed.

Mitigation: Keep PCM_INTERVIEW_REPORT_KEY in an environment variable, avoid hardcoding it, and rotate the key if it is shared or logged.

Risk: The sample shell request interpolates user-provided text into JSON.

Mitigation: Prefer a JSON serializer for production use so job descriptions and filenames are escaped correctly.

## Reference(s):

- [Pincaimao Homepage](https://www.pincaimao.com)
- [ClawHub Skill Page](https://clawhub.ai/pincaimao/skills/pincaimao-interview-reports)
- [Pincaimao Platform API](https://api.pincaimao.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose or raw API answer in a code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize the API answer for readability unless the user requests raw output.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

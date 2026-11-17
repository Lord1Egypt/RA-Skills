## Description:

List all files uploaded by this API key. Returns URL and creation timestamp, ordered newest first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to list uploaded PDF API Hub files for the authenticated API key, including file URLs and creation timestamps for file management, audit review, pipeline monitoring, and cleanup planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a PDF API Hub API key and returns file URLs that may expose private document locations or upload history.

Mitigation: Install only when the agent should access this account's uploaded file list, and treat the API key and returned URLs as sensitive.

## Reference(s):

- [PDF API Hub Documentation](https://pdfapihub.com/docs)
- [PDF API Hub](https://pdfapihub.com)
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/skills/list-files)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files]

**Output Format:** [JSON response with file URLs, creation timestamps, success status, and count]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional limit query parameter from 1 to 500, default 100.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

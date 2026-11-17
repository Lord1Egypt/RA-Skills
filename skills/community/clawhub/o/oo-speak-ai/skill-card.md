## Description:

Operate Speak AI through an OOMOL-connected account to list media and folders, retrieve transcripts, status, and insights, and upload public media URLs for processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Speak AI users can manage media through an already connected OOMOL account: browse folders and media, retrieve transcripts and AI insights, check processing status, and submit public audio or video URLs for processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run downloaded software and add agent skills without a clear approval step; the remote installers' exact effects were unavailable for inspection.

Mitigation: Review setup first, preinstall a verified CLI release, approve its local changes explicitly, and set OO_SKILLS_SYNC_DISABLED=1 before invoking oo if startup skill synchronization should be prevented.

## Reference(s):

- [Speak AI API documentation](https://docs.speakai.co/)
- [Speak AI](https://speakai.co)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Speak AI ClawHub release](https://clawhub.ai/oomol/skills/oo-speak-ai)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [Structured Speak AI results in JSON, with text summaries and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can retrieve media information or submit a public audio or video URL for asynchronous processing.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

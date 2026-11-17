## Description:

Query MeetGeek meeting intelligence from CLI - list meetings, get AI summaries, transcripts, action items, and search across all your calls with natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexty5870](https://clawhub.ai/user/nexty5870)

### License/Terms of Use:


## Use Case:

Developers, employees, and external users with MeetGeek access use this skill to configure the MeetGeek CLI and retrieve meeting lists, AI summaries, transcripts, highlights, action items, and meeting search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned global `meetgeek-cli` npm package.

Mitigation: Use only a trusted, reviewed package version and pin the version where operational policy requires reproducible installs.

Risk: The CLI handles MeetGeek API keys and meeting content, including transcripts that can be exported to local files.

Mitigation: Protect the saved API key, keep transcript exports in managed access-controlled locations, and avoid shared or unmanaged paths for sensitive meeting data.

## Reference(s):

- [MeetGeek ClawHub Skill Page](https://clawhub.ai/nexty5870/skills/meetgeek)
- [meetgeek-cli npm package](https://www.npmjs.com/package/meetgeek-cli)
- [meetgeek-cli GitHub repository](https://github.com/nexty5870/meetgeek-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Text, Guidance]

**Output Format:** [Markdown with inline bash commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MeetGeek API key and the meetgeek-cli npm package; transcript exports may write meeting content to local files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

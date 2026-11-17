## Description:

Summarize or transcribe URLs, YouTube/videos, podcasts, articles, transcripts, PDFs, and local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers can use this skill to summarize or transcribe web pages, videos, podcasts, PDFs, and local files. It supports quick summaries, extracted content, and best-effort video transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Summarizing a local file may send its contents to the configured external model provider.

Mitigation: Check the configured provider and its data handling before use, and avoid sending sensitive files unless that handling is acceptable.

Risk: The security inspection was partial because a referenced local path was not present in the bundled artifact.

Mitigation: Review the missing referenced path and complete the inspection before relying on the scan result.

## Reference(s):

- [Summarize](https://summarize.sh)
- [ClawHub skill release](https://clawhub.ai/hillstreet-ph/skills/oc-summarize)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text or JSON; summaries and extracted transcripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output length is configurable; transcript extraction is best-effort.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

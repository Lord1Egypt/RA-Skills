## Description:

LovTrip Video to Article uses Gemini AI to convert public YouTube videos into structured articles with a title, author, summary, and Markdown body.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

External users, developers, and content creators use this skill to turn public YouTube videos into structured articles for LovTrip guides or other publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended MCP setup runs an unpinned npm package with the user's local privileges and Gemini API key.

Mitigation: Prefer a pinned and reviewed package version or the included standalone script, use a restricted Gemini API key with quotas, and submit only public YouTube videos that may be sent to Google Gemini.

## Reference(s):

- [LovTrip](https://lovtrip.app)
- [LovTrip Guides](https://lovtrip.app/guides)
- [LovTrip Developer Documentation](https://lovtrip.app/developer)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [JSON object with title, author, summary, and Markdown body fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill accepts a public YouTube URL, an optional output language, and an optional custom prompt.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

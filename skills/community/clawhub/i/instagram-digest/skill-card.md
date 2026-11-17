## Description:

Scrape recent Instagram reels, transcribe audio, summarize with OpenRouter, and save a digest.html file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirimaddala99](https://clawhub.ai/user/sirimaddala99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect recent Instagram reels from configured accounts, transcribe reel audio, and generate a local HTML digest of concise summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram session cookies may be stored in plaintext in scripts/.instagram_session.json.

Mitigation: Use a dedicated Instagram account, keep the skill directory private, and delete scripts/.instagram_session.json when finished.

Risk: The generated digest.html can contain untrusted Instagram or model-generated content.

Mitigation: Treat digest.html as untrusted local content and review it before opening, sharing, or reusing it.

Risk: Transcripts and captions may be sent to OpenRouter for summarization.

Mitigation: Avoid processing private or sensitive reels unless that data sharing is acceptable.

Risk: Dependencies are not pinned.

Mitigation: Pin and review dependencies before routine or automated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sirimaddala99/skills/instagram-digest)
- [OpenRouter API endpoint](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands; runtime output is a local digest.html file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY; optional Instagram credentials can be used for account access.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

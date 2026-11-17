## Description:

AI meeting assistant via ghostmeet. Start sessions, get live transcripts, and generate AI summaries from any browser meeting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[higangssh](https://clawhub.ai/user/higangssh)

### License/Terms of Use:


## Use Case:

People who record browser-based meetings use this skill to check a self-hosted ghostmeet backend, retrieve meeting transcripts, and request summaries or action items. It is suited for users who can run Docker, install the companion Chrome extension, and manage meeting transcript privacy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup requires running external Docker and Chrome extension code that can process meeting audio, transcripts, and an Anthropic API key.

Mitigation: Install only from a trusted repository revision, inspect Docker Compose and extension permissions before use, and restrict backend network exposure.

Risk: Summary generation may send meeting transcript text to Anthropic.

Mitigation: Avoid generating summaries for meetings whose transcript should not leave the local environment.

## Reference(s):

- [Ghostmeet ClawHub listing](https://clawhub.ai/higangssh/skills/ghostmeet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summarized meeting content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transcript excerpts, summaries, action items, backend health results, and setup guidance.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

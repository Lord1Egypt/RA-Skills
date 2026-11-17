## Description:

Send a public video URL directly to a Google Gemini model so Codex can summarize video content, answer questions, or extract key points without local download or file upload steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze publicly accessible video URLs with Gemini and return summaries, answers, key points, or timestamp-oriented reports from agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video URLs and prompts are sent to Gemini for processing.

Mitigation: Use only public video URLs and prompts that are appropriate to send to the configured Gemini service.

Risk: Passing API keys on the command line can expose credentials through shell history or process listings.

Mitigation: Configure credentials with MAVERICK_GEMINI_API_KEY or MAVERICK_GOOGLE_API_KEY instead of the --api-key flag when possible.

Risk: Installing dependencies from an untrusted or unpinned environment can introduce supply-chain risk.

Mitigation: Install google-genai from a trusted, pinned Python environment before use.

## Reference(s):

- [Google Video URL Analysis on ClawHub](https://clawhub.ai/maverick/skills/maverick-google-video-url-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text analysis with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a public video URL, a task-specific prompt, the google-genai dependency, and a Gemini API key provided through environment variables or the optional CLI flag.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

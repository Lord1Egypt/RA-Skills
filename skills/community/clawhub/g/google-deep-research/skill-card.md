## Description:

Uses Gemini Deep Research Agent to run autonomous multi-step research and produce detailed Markdown reports with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juan-xin-cai](https://clawhub.ai/user/juan-xin-cai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn a research topic into a long-running Gemini Deep Research session, then present the resulting cited Markdown report and support follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Gemini API key and sends research prompts to Gemini.

Mitigation: Use an approved Gemini API key and avoid submitting secrets or sensitive data unless that use is authorized.

Risk: The optional GOOGLE_GENAI_SDK_PATH override can execute local JavaScript with the same environment as the skill, including access to the Gemini API key.

Mitigation: Prefer the default @google/genai package, or set GOOGLE_GENAI_SDK_PATH only to a fully trusted SDK file.

## Reference(s):

- [@google/genai NPM package](https://www.npmjs.com/package/@google/genai)
- [ClawHub skill page](https://clawhub.ai/juan-xin-cai/skills/google-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report on stdout, with progress status and follow-up interaction ID on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include citation links; runs can be streamed or polled and may take 5-20 minutes.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

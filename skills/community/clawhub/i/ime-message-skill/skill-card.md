## Description:

This skill rewrites recognized input-method or voice-input text into concise, natural instant-message prose, and translates it only when the user explicitly requests a target language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hei-maom](https://clawhub.ai/user/hei-maom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill after an input method or speech system has already produced text, so short chat messages can be cleaned up before sending. It is suited for polishing casual message text and optional user-requested translation, not for audio transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided message text is sent to the configured model service.

Mitigation: Avoid highly sensitive chats unless the deployment has appropriate privacy, logging, and retention controls.

Risk: Managed environments may drift if the OpenAI SDK dependency is not pinned.

Mitigation: Pin the SDK dependency in managed deployments and validate the configured endpoint before release.

Risk: Rewritten text can preserve mistakes from the original recognized text or shift the intended tone.

Mitigation: Return the rewrite to the input box for user review and keep an undo path to the original text.

## Reference(s):

- [Model API reference](references/api_cn.md)
- [Product integration guidance](references/integration_cn.md)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text by default; JSON is available when the script is invoked with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns only the final rewritten message by default and requires the caller to provide the model API token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Listenhub helps agents turn topics, URLs, plain text, and image prompts into podcasts, explainer videos, voice narration, speech audio, or generated images through provided shell scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xfango](https://clawhub.ai/user/0xfango)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create generated audio, video, and image assets from prompts, article URLs, YouTube links, or pasted text. It is best suited for content creation workflows that can safely send source material to the ListenHub and Labnana services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, pasted text, URLs, and reference images may be sent to external ListenHub, Marswave, or Labnana services for processing.

Mitigation: Avoid confidential or sensitive inputs, use trusted source URLs, and confirm the user is comfortable with external processing before generation.

Risk: The image-generation setup can modify persistent shell startup files and may run package-manager installs with elevated privileges.

Mitigation: Preinstall dependencies manually, set LISTENHUB_API_KEY and LISTENHUB_OUTPUT_DIR yourself in an approved secrets location, and review the script before first use.

Risk: Generated content jobs are long-running and depend on remote service status responses.

Mitigation: Use the provided status-check script, handle timeout or rate-limit responses as pending work, and avoid assuming completion until the service reports success.

## Reference(s):

- [Listenhub ClawHub Skill Page](https://clawhub.ai/0xfango/skills/listenhub-2)
- [0xfango Publisher Profile](https://clawhub.ai/user/0xfango)
- [ListenHub API Key Settings](https://listenhub.ai/settings/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON status payloads, generated media links, and local image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation can produce long-running podcast, explainer, TTS, speech, video, or image jobs that require status checks and external service access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

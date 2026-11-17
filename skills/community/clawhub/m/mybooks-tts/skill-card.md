## Description:

MyBooks TTS helps agents configure MiMo or OpenAI-compatible text-to-speech, convert EPUB books into audiobooks, monitor conversion progress, and manage cloned voices and voice prompts on an administrator-authorized MyBooks server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiningsprk-arch](https://clawhub.ai/user/shiningsprk-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MyBooks administrators use this skill to automate EPUB-to-audiobook conversion and voice management workflows through an authenticated MyBooks TTS server. It is intended for trusted operators who can provide administrator credentials and review persistent server changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles MyBooks administrator credentials and can perform admin-level actions.

Mitigation: Use session-scoped environment variables or a dedicated secret manager, and run the skill only against trusted MyBooks servers.

Risk: The skill can make persistent or destructive server changes, including deleting cloned voices or saved voice prompts.

Mitigation: Require manual review before delete actions or configuration changes are executed.

Risk: Disabling TLS certificate verification weakens transport security.

Mitigation: Use HTTPS with certificate verification enabled whenever possible, and disable verification only for trusted self-signed deployments.

Risk: Clone-audio preview downloads can write files to local paths.

Mitigation: Allow only user-approved save paths and do not let untrusted prompts choose local destinations.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/shiningsprk-arch/mybooks-tts-skill/tree/main/skills/mybooks_tts)
- [ClawHub skill page](https://clawhub.ai/shiningsprk-arch/skills/mybooks-tts)
- [MyBooks project homepage](https://www.mybooks.top)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON command arguments, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save cloned voice preview audio to a local path when requested.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

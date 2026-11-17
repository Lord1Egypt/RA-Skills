## Description:

Generate custom music tracks (vocal or instrumental) via OhYesAI asynchronously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bajie-git](https://clawhub.ai/user/bajie-git)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate vocal or instrumental music by collecting song parameters, submitting an OhYesAI generation task, polling for completion, and downloading the resulting MP3 audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command templates include user-provided song parameters, which can enable command injection if copied directly into a shell.

Mitigation: Build request JSON with a serializer or validated variables, quote shell values, and review commands before execution.

Risk: The OhYesAI API key is passed in request URLs and may be exposed through logs, shell history, or shared command output.

Mitigation: Use a restricted workspace, avoid logging commands or responses containing the key, and rotate OHEYSAI_API_KEY if exposure is suspected.

Risk: Downloaded MP3 output may overwrite existing files when fixed filenames are reused.

Mitigation: Download to unique, user-approved filenames in the current workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bajie-git/skills/ohyesai-music)
- [OhYesAI developer homepage](https://dev.ohyesai.com)
- [OhYesAI API key homepage](https://ohyesai.com?from=https://clawhub.ai)
- [Publisher profile](https://clawhub.ai/user/bajie-git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with bash commands and downloaded MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, grep, sleep, and OHEYSAI_API_KEY; uses asynchronous task submission and polling before download.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

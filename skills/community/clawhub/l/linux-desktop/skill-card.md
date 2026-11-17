## Description:

Linux Desktop Control helps agents automate a Linux desktop by taking screenshots, moving and clicking the mouse, typing text, pressing keys, and managing windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouyangabel](https://clawhub.ai/user/ouyangabel)

### License/Terms of Use:


## Use Case:

Developers and automation-focused agents use this skill to inspect and control Linux desktop sessions through screenshots, mouse actions, keyboard input, window discovery, and screen information commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command-injection exposure can turn normal helper-script arguments into arbitrary shell commands.

Mitigation: Do not expose the script to untrusted prompts, wrappers, filenames, window IDs, typed text, or key values until shell=True is removed and arguments are validated.

Risk: Desktop automation can interact with sensitive windows or simulate privileged commands through typed input.

Mitigation: Use only in a non-sensitive desktop session, avoid password or financial windows, verify the active window before typing, and do not run privileged commands through simulated typing.

## Reference(s):

- [Linux Desktop Control on ClawHub](https://clawhub.ai/ouyangabel/skills/linux-desktop)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PNG screenshot files at requested paths or timestamped /tmp defaults.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

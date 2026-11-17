## Description:

GUI automation via visual detection for clicking, typing, reading content, navigating menus, and filling forms through a screenshot, detect, and act workflow that supports macOS and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfredjamesli](https://clawhub.ai/user/alfredjamesli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use GUI Agent to operate desktop and browser interfaces in OpenClaw by observing screenshots, detecting UI elements, taking actions, verifying results, and saving visual memory for repeated workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control the desktop and capture screenshots, which may expose sensitive applications or documents.

Mitigation: Use it only in trusted sessions, avoid sensitive screens, and disable or regularly delete visual memory when handling private content.

Risk: Remote GUI control can be unsafe when pointed at arbitrary HTTP endpoints.

Mitigation: Use remote mode only with trusted, isolated virtual machines or endpoints that you control.

Risk: Security evidence calls out command-injection paths through shell=True and remote python3 -c usage.

Mitigation: Review and harden those execution paths before passing untrusted task parameters to the skill.

Risk: Setup installs latest packages and model artifacts without pinned hashes.

Mitigation: Pin and review dependencies or install in an isolated environment before operational use.

## Reference(s):

- [ClawHub GUI Agent release page](https://clawhub.ai/alfredjamesli/skills/gui-claw)
- [GPA-GUI-Detector model](https://huggingface.co/Salesforce/GPA-GUI-Detector)
- [Core principles](docs/core.md)
- [OSWorld benchmark notes](benchmarks/osworld/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GUI action commands, detected UI targets, setup steps, verification guidance, and local visual-memory workflow notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Automates the Jianying desktop client's AI text-to-video workflow to turn a user-provided storyboard script into a 9:16 future-science-fiction video with a preset voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infiniteask](https://clawhub.ai/user/infiniteask)

### License/Terms of Use:

MIT-0

## Use Case:

External users or creators can use this skill through an agent to configure Jianying Professional desktop settings and launch its AI text-to-video flow for storyboard-to-video generation. It is intended for controlled Windows desktop sessions with Jianying installed and preconfigured screen coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad desktop automation can click or type into the wrong window if the desktop changes during execution.

Mitigation: Run only in a dedicated Windows desktop session with non-sensitive windows closed, and avoid user interaction while the automation is active.

Risk: The skill overwrites the clipboard and may store storyboard text and screenshots locally.

Mitigation: Use non-sensitive storyboard content, clear the clipboard after use, and review or delete local temporary files and screenshots.

Risk: Runtime package installation and self-modification directives weaken deployment control.

Mitigation: Preinstall and pin dependencies in a controlled environment, and review or remove self-modification and no-other-skills directives before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infiniteask/skills/jianying-ai-text-video-infinite)
- [ClawHub publisher profile](https://clawhub.ai/user/infiniteask)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python and PowerShell code blocks plus local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local coordinate JSON and user-provided storyboard text; may save local screenshots during verification.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Pixshop CLI helps agents guide users through command-line image generation, video creation, media editing, app discovery, and prompt search workflows for the Pixshop service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

External users, developers, and creative automation agents use this skill to install and operate Pixshop CLI commands for generating images, creating videos, editing media, checking credits, browsing Pixshop apps, and searching prompt libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install and use a mutable global third-party CLI with OAuth and remote media processing.

Mitigation: Install only if the Pixshop npm package and service are trusted, prefer a pinned or project-local install, avoid elevated privileges, and review where credentials are stored.

Risk: Prompts, images, and videos submitted through the CLI may be sent to the Pixshop service for processing.

Mitigation: Do not submit private, regulated, proprietary, or unauthorized media and prompts unless the user is authorized to send them to Pixshop.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizhijun/skills/pixshop-cli)
- [Publisher profile](https://clawhub.ai/user/lizhijun)
- [Pixshop](https://pixshop.app)
- [Pixshop CLI documentation](https://pixshop.app/docs/cli)
- [Nano Banana Apps](https://pixshop.app/apps)
- [Pixshop prompt library](https://pixshop.app/prompt-library)
- [Pixshop effects](https://pixshop.app/effects)
- [Pixshop Design Agent](https://pixshop.app/agent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Pixshop CLI commands that authenticate with a remote service, consume credits, and process user-provided image, video, or prompt data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

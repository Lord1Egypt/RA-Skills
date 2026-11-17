## Description:

Download manga from Kmoe (kxx.moe / mox.moe) with concurrent downloads, credential management, and automation callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inphinitiz](https://clawhub.ai/user/inphinitiz)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to guide manga downloads from Kmoe with the kmdr CLI, including batch volume selection, credential pools, proxies, mirror switching, and post-download callbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external CLI package that handles account credentials.

Mitigation: Install only when comfortable with the package and keep credential pools minimal.

Risk: Password examples may encourage placing credentials on the command line.

Mitigation: Prefer prompted password entry and avoid storing passwords in shell history.

Risk: Post-download callbacks run local commands.

Mitigation: Use callbacks only with trusted commands and reviewed metadata templates.

## Reference(s):

- [Kmoe Manga Download on ClawHub](https://clawhub.ai/inphinitiz/skills/kmoe-manga-download)
- [Kmoe mirror](https://mox.moe)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the external kmdr command from the kmoe-manga-downloader Python package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

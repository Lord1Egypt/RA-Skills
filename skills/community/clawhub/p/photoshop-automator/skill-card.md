## Description:

Professional Adobe Photoshop automation via COM/ExtendScript bridge. Supports text updates, filters, and action playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdul-karim-mia](https://clawhub.ai/user/abdul-karim-mia)

### License/Terms of Use:


## Use Case:

Developers, designers, and automation engineers use this skill to automate Adobe Photoshop tasks such as running ExtendScript, updating text layers, creating layers, applying filters, playing actions, and exporting active documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The raw runScript command can execute arbitrary Photoshop ExtendScript with broad local scripting and filesystem power.

Mitigation: Review every generated script before execution and add confirmation or allowlist controls before unattended use.

Risk: Photoshop scripts and export operations can create, modify, overwrite, or delete local files.

Mitigation: Use explicit output paths in non-sensitive directories, validate paths, and add overwrite checks.

Risk: Temporary script files are written locally before execution.

Mitigation: Use safer temporary-file creation and cleanup controls when adapting the skill for unattended workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdul-karim-mia/skills/photoshop-automator)
- [Publisher profile](https://clawhub.ai/user/abdul-karim-mia)
- [Project homepage from artifact metadata](https://github.com/abdul-karim-mia/photoshop-automator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text returned from local Photoshop automation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Adobe Photoshop and platform automation tools such as cscript on Windows or osascript on macOS.]

## Skill Version(s):

1.2.4 (source: server release metadata, package.json, _meta.json, handler.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

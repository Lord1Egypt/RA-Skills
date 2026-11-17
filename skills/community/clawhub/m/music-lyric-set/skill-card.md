## Description:

Turns user-supplied song lyrics into a four-to-eight still music lyric card set, with one still for each named lyric section.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to plan and generate a consistent pack of lyric-card stills from lyric sections they already supplied and approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the package requests a broad Beatra Device Token with account powers.

Mitigation: Install only when that access is acceptable, keep the token out of prompts and logs, and disconnect or uninstall the package when access is no longer needed.

Risk: The security evidence says package code silently self-updates by default.

Mitigation: Consider disabling automatic updates with the documented update command and check updates explicitly before use.

Risk: Generated lyric-card stills can contain incorrect or unintended printed text.

Mitigation: Use only user-supplied approved lyric lines and review generated text against the confirmed pack list before publishing or reusing the images.

## Reference(s):

- [Music lyric card pack workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Bundled MCP Client diagnostics](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/music-lyric-set)
- [Publisher profile](https://clawhub.ai/user/beatra-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command and JSON payload examples; final generated stills are delivered as returned files or artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one image-generation task per approved lyric-section still and caps the pack at eight stills.]

## Skill Version(s):

0.1.2 (source: release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

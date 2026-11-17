## Description:

Copies large or long local files into a configured OneDrive OpenClaw folder so users can open or share the full document from Telegram or WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moodykong](https://clawhub.ai/user/moodykong)

### License/Terms of Use:


## Use Case:

Agents use this skill when a user needs a full local document or long file copied into OneDrive for opening or sharing from Telegram or WhatsApp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a persistent machine-specific OneDrive destination configuration.

Mitigation: Remove or replace the packaged config.env before installation and confirm the active OneDrive root and subfolder with the user.

Risk: Copied files may be written outside the intended OneDrive subfolder if destination containment is not enforced.

Mitigation: Avoid absolute paths or .. in the subdir and add destination containment checks before use with sensitive documents or shared directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moodykong/skills/onedrive-integration)
- [Publisher profile](https://clawhub.ai/user/moodykong)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command snippets and destination path text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May copy files into a configured OneDrive subdirectory and print destination paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
PixVerse CLI helps agents generate, edit, post-process, manage, and download AI images and videos from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pixverse-official](https://clawhub.ai/user/pixverse-official) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agents, developers, and creative automation users use this skill to script PixVerse media generation workflows, including text-to-video, image-to-video, image editing, prompt enhancement, post-processing, workspace management, and asset handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation actions can consume PixVerse account credits. <br>
Mitigation: Require explicit user confirmation before paid generations and check account credits before starting a workflow. <br>
Risk: Local media supplied to creation or editing commands can be uploaded for cloud processing. <br>
Mitigation: Confirm uploads before execution and avoid sensitive, private, confidential, or voice media. <br>
Risk: Asset management commands can delete generated images or videos. <br>
Mitigation: Require confirmation before deletion and verify the asset ID and workspace context. <br>
Risk: Workspace switching changes which credits and assets the CLI operates on. <br>
Mitigation: Require confirmation before workspace switches and check the active workspace before creating, deleting, or downloading assets. <br>
Risk: Authentication and workspace state can persist in ~/.pixverse/ or be overridden with PIXVERSE_TOKEN. <br>
Mitigation: Protect stored credentials, avoid exposing environment tokens, and log out when shared environments are used. <br>
Risk: Bundled update scripts can modify a local git checkout. <br>
Mitigation: Run update scripts only in a trusted checkout after reviewing local changes and expected remote updates. <br>


## Reference(s): <br>
- [PixVerse Homepage](https://pixverse.ai) <br>
- [PixVerse App](https://app.pixverse.ai) <br>
- [Mondo Artist Styles](references/mondo-poster/artist-styles.md) <br>
- [Mondo Composition Patterns](references/mondo-poster/composition-patterns.md) <br>
- [Mondo Genre Templates](references/mondo-poster/genre-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide agents through PixVerse CLI operations that create, modify, download, or delete generated media assets.] <br>

## Skill Version(s): <br>
1.5.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

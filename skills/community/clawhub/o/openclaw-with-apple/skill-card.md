## Description: <br>
Provides agent guidance and Python tools for Apple iCloud access, Apple Health analysis, and two-way task and note synchronization with iPhone apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gzww](https://clawhub.ai/user/gzww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual users use this skill to let an agent configure iCloud calendar access, capture tasks and notes into local sync files, and analyze Apple Health exports. It is intended for Apple account automation where the user explicitly accepts the credential and device-control risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad Apple/iCloud control, including Drive, photos, device lookup, calendar, reminders, notes, and Health-derived data. <br>
Mitigation: Install it only for users who intentionally want this scope; review commands before execution and keep sensitive or destructive actions manually confirmed. <br>
Risk: The skill asks for Apple ID credentials and may involve 2FA codes in chat. <br>
Mitigation: Prefer app-specific passwords or local interactive login where possible, avoid pasting the main Apple ID password into chat, and remove sensitive conversation history after setup. <br>
Risk: Cached iCloud session files can grant continued access while valid. <br>
Mitigation: Protect ~/.pyicloud with local user-only permissions, remove cached sessions when access is no longer needed, and revoke app-specific passwords from the Apple ID account page. <br>
Risk: Automatic scheduled sync can persistently move task and note data into iCloud Drive and iPhone apps. <br>
Mitigation: Inspect imported Shortcuts before disabling prompts, confirm scheduled jobs are expected, and know how to remove the launchd job or sync files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gzww/openclaw-with-apple) <br>
- [README.md](artifact/README.md) <br>
- [SECURITY.md](artifact/SECURITY.md) <br>
- [TUTORIAL.md](artifact/TUTORIAL.md) <br>
- [Health Daily Export Shortcut](https://www.icloud.com/shortcuts/94862224a4b64ca0bf037b89c8f81cb7) <br>
- [Tasks Import Shortcut](https://www.icloud.com/shortcuts/de68c5443f054355bdb332f246c24a94) <br>
- [Notes Import Shortcut](https://www.icloud.com/shortcuts/2229591d96a849a6ad9b4e44b4b6ce80) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/file operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Python scripts that access iCloud and CalDAV services, write local task or note JSON files, cache iCloud sessions, and configure scheduled synchronization.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata, SKILL.md frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

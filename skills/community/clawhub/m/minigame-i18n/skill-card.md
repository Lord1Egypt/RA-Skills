## Description:

Guides agents through localizing WeChat mini-games from Chinese into target languages, including text scanning, glossary planning, translation, resource application, optional image translation, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and localization engineers use this skill to prepare WeChat mini-game projects for international markets by finding Chinese text, planning terminology, generating translations, applying language resources, and checking localization quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project images may be uploaded when image translation is enabled.

Mitigation: Enable image translation only for assets approved for upload, and provide MCP credentials explicitly over HTTPS.

Risk: The workflow can rewrite project files while applying text, language-pack, and image changes.

Mitigation: Run in an isolated workspace, keep backups, review dry-run results, and verify replacement reports before accepting changes.

Risk: The workflow may install Node dependencies and execute local helper scripts.

Mitigation: Review the artifact before installation and install dependencies only in the skill scripts directory or another isolated environment.

Risk: Stored MCP credentials may be read from IDE configuration files.

Mitigation: Use scoped credentials, avoid broadly copying tokens across IDE configs, and prefer explicit credential arguments where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/minigame-i18n)
- [Scan analysis workflow](artifact/references/scan-analysis.md)
- [Execution plan and glossary workflow](artifact/references/plan-glossary.md)
- [Translation execution workflow](artifact/references/execute-translation.md)
- [Apply localization resources workflow](artifact/references/apply-resources.md)
- [Quality verification workflow](artifact/references/quality-verification.md)
- [Scan report schema](artifact/references/scan-report-schema.md)
- [MCP image translation reference](artifact/references/mcp-image-translation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON reports, generated language-pack files, code edits, configuration updates, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project-local i18n files, translation tables, replacement reports, verification reports, backups, and optional translated image assets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

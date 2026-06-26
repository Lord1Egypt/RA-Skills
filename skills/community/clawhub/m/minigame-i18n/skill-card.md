## Description: <br>
Helps developers localize WeChat mini-games for international markets by scanning Chinese text, planning terminology, generating translations and language packs, replacing localized text and images, and validating the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and localization engineers use this skill to internationalize WeChat mini-games from Chinese into target languages. It guides scanning, terminology review, translation generation, language-pack creation, source and asset replacement, and quality verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically modify source files and assets. <br>
Mitigation: Install on a clean branch, review generated plans and diffs, and run dry-run and verification steps before accepting replacements. <br>
Risk: The skill can install npm dependencies and read or store MCP credentials in IDE configuration files. <br>
Mitigation: Use explicit credentials, limit where tokens are written, and review MCP configuration files before use. <br>
Risk: Image translation can upload game images to an external service. <br>
Mitigation: Skip image translation for sensitive assets or confirm upload approval before enabling that stage. <br>


## Reference(s): <br>
- [Skill workflow](SKILL.md) <br>
- [Skill - Scan analysis](references/scan-analysis.md) <br>
- [Skill - Execution plan and glossary generation](references/plan-glossary.md) <br>
- [Skill - Execute translation](references/execute-translation.md) <br>
- [Skill - Apply localization resources](references/apply-resources.md) <br>
- [Skill - Localization quality verification](references/quality-verification.md) <br>
- [MCP image translation interface](references/mcp-image-translation.md) <br>
- [Scan report schema](references/scan-report-schema.md) <br>
- [ClawHub skill listing](https://clawhub.ai/tencent-adm/minigame-i18n) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON and file artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create scan reports, translation JSON files, language packs, backups, replacement reports, and verification reports in the user's project.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

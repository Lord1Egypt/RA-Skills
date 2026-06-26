## Description: <br>
Interactive guide for integrating MobTech MobLink into HarmonyOS NEXT projects with a confirmation-gated workflow for SDK setup, privacy compliance, deep-link configuration, and scene restore code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration engineers use this skill to add MobTech MobLink capabilities to HarmonyOS NEXT applications, including ohpm dependency setup, project configuration, privacy authorization handling, scene restore listeners, mobID examples, and generated integration notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose edits to HarmonyOS project files and install ohpm dependencies. <br>
Mitigation: Install only for a HarmonyOS project you control and review every proposed diff before accepting changes. <br>
Risk: The workflow handles MobTech app credentials, including appSecret, through the MobLink configuration spreadsheet. <br>
Mitigation: Keep MobLink_Config.xlsx out of version control, avoid pasting appSecret into chat or logs, and delete or secure the file after integration. <br>
Risk: Incorrect privacy authorization or permission configuration could create compliance issues in the target app. <br>
Mitigation: Verify the privacy consent flow, permissions, and MobTech compliance requirements before release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mobsupport/harmonyos-moblink-integration) <br>
- [MobTech Documentation Entry](https://www.mob.com/wiki/detailed?wiki=661&id=34) <br>
- [HarmonyOS NEXT Integration Guide](https://mob.com/wiki/detailed?wiki=731&id=34) <br>
- [MobLink Console Basic Configuration](https://mob.com/wiki/detailed?wiki=527&id=34) <br>
- [MobLink HarmonyOS Compliance Guide](https://mob.com/wiki/detailed?wiki=758&id=34) <br>
- [MobLink FAQ](https://mob.com/wiki/detailed?wiki=530&id=34) <br>
- [MobLink Privacy Policy](https://mob.com/wiki/detailed?wiki=97&id=34) <br>
- [Extended Business Function Settings](https://www.mob.com/wiki/detailed?wiki=730&id=34) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, HarmonyOS configuration snippets, TypeScript code examples, and generated project files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive workflow gated by user confirmation; may generate MobLink_Config.xlsx and MOBLINK_README.md in the target HarmonyOS project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

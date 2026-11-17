## Description:

Interactive guide for integrating MobTech ShareSDK into HarmonyOS NEXT projects. Use when the user wants ShareSDK sharing or Huawei authorization in a HarmonyOS app, and needs help with ohpm dependencies, module.json5 permissions, AppKey/AppSecret setup, privacy compliance, or post-integration ShareSDK extension capability guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate MobTech ShareSDK sharing, Huawei authorization, Weibo, and WeChat capabilities into HarmonyOS NEXT projects. It helps validate project structure, generate a configuration workbook, install ohpm dependencies, update module.json5 settings, and place privacy, initialization, sharing, authorization, and project documentation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to place app secrets in project-root files, which can expose credentials if those files are committed or shared.

Mitigation: Keep secrets out of source control, add generated configuration files to ignore rules, and rotate any credentials that were exposed.

Risk: Unpinned ohpm dependencies can change between runs and introduce unexpected behavior.

Mitigation: Pin and review @zztsdk/zztcore and @zztsdk/sharesdk versions before running install commands.

Risk: ShareSDK initialization and privacy authorization code can create privacy compliance issues if called before user consent.

Mitigation: Call ShareSDK privacy authorization only after the app's privacy notice is shown and the user explicitly agrees.

## Reference(s):

- [MobTech ShareSDK HarmonyOS Integration Guide](https://www.mob.com/wiki/detailed?wiki=696&id=14)
- [MobTech ShareSDK Extended Business Function Settings](https://www.mob.com/wiki/detailed?wiki=711&id=14)
- [MobTech ShareSDK HarmonyOS Compliance Guide](https://www.mob.com/wiki/detailed?wiki=748&id=14)
- [MobTech ShareSDK Weibo Authorization and Sharing](https://www.mob.com/wiki/detailed?wiki=722&id=14)
- [MobTech ShareSDK WeChat Authorization and Sharing](https://www.mob.com/wiki/detailed?wiki=724&id=14)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, configuration snippets, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate an Excel configuration template and project README after user confirmation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

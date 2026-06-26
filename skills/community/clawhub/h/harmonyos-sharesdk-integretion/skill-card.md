## Description: <br>
Interactive guide for integrating MobTech ShareSDK into HarmonyOS NEXT projects, including sharing, Huawei authorization, ohpm dependencies, module.json5 permissions, AppKey/AppSecret setup, privacy compliance, and post-integration ShareSDK extension guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add MobTech ShareSDK sharing and authorization features to HarmonyOS NEXT applications. It guides project inspection, dependency installation, configuration template generation, module.json5 edits, privacy consent wiring, and platform-specific Weibo or WeChat setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure during ShareSDK setup. <br>
Mitigation: Treat appSecret, WeChat AppSecret, and client_id values as sensitive; keep the generated Excel file out of version control and remove or protect it after integration. <br>
Risk: Unreviewed project edits or package commands could alter a HarmonyOS project unexpectedly. <br>
Mitigation: Use the skill only for a HarmonyOS project where MobTech ShareSDK integration is intended, and review each proposed file change and ohpm command before approving it. <br>
Risk: Privacy compliance can be broken if ShareSDK authorization is called before user consent. <br>
Mitigation: Wire privacy authorization only after the user agrees to the app privacy policy and include the required ShareSDK disclosures in the app privacy materials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mobsupport/harmonyos-sharesdk-integretion) <br>
- [MobTech ShareSDK integration guide](https://www.mob.com/wiki/detailed?wiki=696&id=14) <br>
- [MobTech ShareSDK extension capability settings](https://www.mob.com/wiki/detailed?wiki=711&id=14) <br>
- [MobTech HarmonyOS compliance guidance](https://www.mob.com/wiki/detailed?wiki=748&id=14) <br>
- [MobTech Weibo authorization and sharing](https://www.mob.com/wiki/detailed?wiki=722&id=14) <br>
- [MobTech WeChat authorization and sharing](https://www.mob.com/wiki/detailed?wiki=724&id=14) <br>
- [ShareSDK privacy policy](https://policy.zztfly.com/sdk/share/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, ArkTS snippets, JSON5 configuration examples, and generated XLSX configuration template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to request confirmation before file edits, review ohpm commands before execution, and protect credential-bearing configuration files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

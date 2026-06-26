## Description: <br>
Interactive guide for integrating MobTech FlyVerify into HarmonyOS NEXT projects, including dependency setup, project configuration, privacy timing, verification calls, authorization page customization, and return-code troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add MobTech FlyVerify one-click verification or one-click login to HarmonyOS NEXT apps. It helps gather configuration, inspect project structure, propose confirmed file changes, and provide integration and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose edits to HarmonyOS project files and dependency state. <br>
Mitigation: Review exact diffs, ohpm commands, and added INTERNET/GET_NETWORK_INFO permissions before approving any changes. <br>
Risk: MobTech appKey/appSecret and the generated Excel configuration file are sensitive integration materials. <br>
Mitigation: Keep credentials and filled configuration spreadsheets out of version control and share them only with authorized project maintainers. <br>
Risk: FlyVerify privacy-consent timing affects compliance and app behavior. <br>
Mitigation: Call the privacy grant API only after the user accepts the app privacy policy, and do not proceed with SDK use before that consent path is confirmed. <br>
Risk: The source artifact notes inconsistent controller names in upstream extension-business documentation. <br>
Mitigation: Check the installed dependency exports before adding extension controller code, and avoid copying ambiguous class names directly into the app. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mobsupport/harmonyos-flyverify-integretion) <br>
- [MobTech FlyVerify HarmonyOS integration guide](https://www.mob.com/wiki/detailed?wiki=717&id=78) <br>
- [MobTech FlyVerify HarmonyOS compliance guide](https://www.mob.com/wiki/detailed?wiki=754&id=78) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, ArkTS code snippets, JSON5 configuration examples, and generated Excel template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the user one blocking question at a time and requires confirmation before proposed project file changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

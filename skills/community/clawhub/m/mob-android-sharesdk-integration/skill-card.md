## Description: <br>
Interactive guide for integrating MobTech ShareSDK into Android projects with a six-step workflow covering project validation, platform credential collection, Gradle configuration, privacy consent wiring, share-code insertion, and project documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Android developers use this skill to add MobTech ShareSDK sharing capabilities to an Android app through an interactive, confirmation-based integration flow. It helps configure Gradle, validate ShareSDK platform credentials, add privacy authorization callbacks, generate sharing code, and document the resulting integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles MobTech appKey and appSecret values from a local ShareSDK configuration spreadsheet. <br>
Mitigation: Keep real appSecret values out of chat and public repositories, and review generated configuration before committing or sharing project files. <br>
Risk: The skill can edit Android project Gradle files and insert Java integration code. <br>
Mitigation: Review proposed Gradle and source-code changes before applying them, and use version control to inspect the final diff. <br>
Risk: The skill can run Gradle synchronization in the target Android project. <br>
Mitigation: Run Gradle only in projects you trust and review dependency changes before continuing development or release work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mobsupport/mob-android-sharesdk-integration) <br>
- [Mob documentation center](https://www.mob.com/wiki/list) <br>
- [Mob SDK compliance guide](https://www.mob.com/wiki/detailed?wiki=421&id=717) <br>
- [Mob Android Maven repository](https://mvn.mob.com/android) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Gradle, Java, shell command, and configuration snippets; may also create or edit Android project files after user confirmation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow asks for confirmation before project edits, reads a local ShareSDK credential spreadsheet, and may run Gradle dependency synchronization in the target Android project.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

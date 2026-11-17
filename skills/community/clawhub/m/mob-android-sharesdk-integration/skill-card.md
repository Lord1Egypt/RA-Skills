## Description:

Interactive guide for integrating MobTech ShareSDK into Android projects with a 6-step workflow for project validation, platform configuration, Gradle setup, privacy authorization, share code insertion, and project documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Android engineers use this skill to add MobTech ShareSDK sharing support to Android apps. It guides configuration of app credentials, social platform devInfo blocks, privacy authorization callbacks, share invocation code, and integration documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to handle MobTech and social platform app secrets in Excel, Gradle, and properties files.

Mitigation: Use placeholder values in chat, keep populated secret-bearing files out of version control, and review generated project files before committing changes.

Risk: The Gradle examples include dynamic dependency versions and additional Maven repositories.

Mitigation: Pin Gradle plugin versions where possible and use only trusted repositories approved for the target project.

Risk: The skill may propose direct Android project edits and Gradle dependency refresh commands.

Mitigation: Approve project edits and Gradle commands only after reviewing the exact files, diffs, and commands to be run.

## Reference(s):

- [Mob Documentation Center](https://www.mob.com/wiki/list)
- [Mob SDK Download Center](https://www.mob.com/download)
- [Mob SDK Compliance Guide](https://www.mob.com/wiki/detailed?wiki=421&id=717)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Interactive Markdown guidance with inline Gradle, Java, shell, and configuration snippets; may create Excel and README files in the target Android project.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before project edits and Gradle commands.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

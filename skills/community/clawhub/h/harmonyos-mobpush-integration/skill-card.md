## Description:

Guides developers through a confirmed, step-by-step MobTech MobPush integration for HarmonyOS NEXT projects, including SDK setup, project configuration, privacy-gated initialization, push handling, aliases, tags, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating MobTech MobPush into HarmonyOS NEXT Stage-model apps use this skill to generate a configuration workbook, install ohpm SDK dependencies, update HarmonyOS project configuration, add privacy-gated initialization, and implement push message handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MobPush app secrets may be written into project files, source code, or repository-backed workbooks.

Mitigation: Use test credentials during evaluation, keep configuration workbooks and generated files out of source control when they contain secrets, and rotate any secret that was committed, shared, or built into an app by mistake.

Risk: The workflow installs third-party ohpm packages into a HarmonyOS project.

Mitigation: Pin and review the @zztsdk/zztcore and @zztsdk/mobpush packages before use, preferably in an isolated test project before applying changes to production code.

Risk: Push SDK initialization before user consent can create privacy compliance issues.

Mitigation: Initialize MobPush only after the app has presented its privacy notice and the user has granted consent, then call the documented privacy grant method from the consent callback.

## Reference(s):

- [Mob Documentation Center](https://www.mob.com/wiki/list)
- [HarmonyOS MobPush Integration Guide](https://www.mob.com/wiki/detailed?wiki=697&id=136)
- [MobPush SDK API Reference](https://www.mob.com/wiki/detailed?wiki=698&id=136)
- [MobPush Backend Configuration Guide](https://www.mob.com/wiki/detailed?wiki=560&id=136)
- [HarmonyOS Compliance Notes](https://www.mob.com/wiki/detailed?wiki=745&id=136)
- [Huawei AppGallery Connect](https://developer.huawei.com/consumer/cn/service/josp/agc/index.html)
- [MobPush SDK Privacy Policy](https://policy.zztfly.com/sdk/mobpush/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, configuration snippets, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive workflow that asks for confirmation before each project change and uses a user-filled Excel workbook for MobPush configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

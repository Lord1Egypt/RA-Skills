## Description:

Interactive guide for integrating MobTech FlyVerify into HarmonyOS NEXT projects for one-click verification or one-click login, including dependency setup, HarmonyOS configuration, privacy timing, API calls, auth page customization, and return-code troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide MobTech FlyVerify integration in HarmonyOS NEXT apps. It helps collect app configuration, plan and confirm project changes, add SDK setup and privacy-gated login flows, and document troubleshooting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects and may persist a MobTech app secret while preparing FlyVerify configuration.

Mitigation: Keep generated configuration files local, exclude files containing appSecret from version control, delete them after use, and rotate any secret that was shared or committed.

Risk: The skill can change HarmonyOS dependencies, permissions, configuration, and login code.

Mitigation: Review each proposed change before applying it, use the skill only on projects where these changes are acceptable, and pin and review SDK package versions where possible.

Risk: MobTech documentation uses inconsistent controller class names for extended business controller flows.

Mitigation: Verify the actual SDK exports and compile the project before committing code that uses extended controller APIs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mobsupport/skills/harmonyos-flyverify-integretion)
- [MobTech FlyVerify integration guide](https://www.mob.com/wiki/detailed?wiki=717&id=78)
- [MobTech FlyVerify HarmonyOS compliance guide](https://www.mob.com/wiki/detailed?wiki=754&id=78)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, configuration snippets, and generated Excel template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to HarmonyOS project configuration and ArkTS code after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

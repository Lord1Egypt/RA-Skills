## Description:

Assists developers with HarmonyOS 7 and API 26 application work, including ArkTS and ArkUI code generation, deprecated API migration guidance, architecture patterns, performance practices, testing, debugging, and multi-device adaptation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fff-119](https://clawhub.ai/user/fff-119)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate and review HarmonyOS ArkTS and ArkUI code, plan Stage-model application structure, migrate deprecated APIs, and apply HarmonyOS-focused quality, performance, security, and release checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill includes self-learning behavior that directs an agent to rewrite and re-register expert files after conversations.

Mitigation: Disable that behavior or require explicit diff review and approval before any expert-file edits, chat-derived knowledge appends, or registration commands are run.

Risk: The security guidance identifies analytics, background location, enterprise quarantine/delete, and provider-endpoint examples as sensitive implementation patterns.

Mitigation: Use consent, HTTPS, least-privilege credentials, and project-specific privacy and security safeguards before adapting those examples.

## Reference(s):

- [HarmonyOS UIAbility Component Overview](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/uiability-overview-V5)
- [HarmonyOS UIAbility Lifecycle](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/uiability-lifecycle-V5)
- [HarmonyOS Spatialization Sample](https://gitcode.com/HarmonyOS_Samples/Spatialization)
- [ArkTS Patterns](https://github.com/OpeNopEn2007/arkts-patterns)
- [ClawHub Skill Page](https://clawhub.ai/fff-119/skills/harmonyos-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with ArkTS, ArkUI, JSON, and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-version labels, code self-check summaries, migration notes, and release or debugging checklists.]

## Skill Version(s):

5.0.0 (source: ClawHub release metadata; artifact frontmatter version is 6.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Build ORBCAFE application shell and navigation with CAppPageLayout, NavigationIsland, useNavigationIsland, i18n, markdown rendering, and CPageTransition patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenruiyang](https://clawhub.ai/user/shenruiyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to implement ORBCAFE UI app frames, navigation, locale switching, menu actions, markdown rendering, and page transitions, especially when rendered UI appears inactive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and frontend bootstrapping can introduce ordinary supply-chain or project-configuration risk.

Mitigation: Install in a normal project sandbox and pin dependency versions or use a reviewed lockfile before production use.

Risk: Locale, hydration, route highlighting, user-menu wiring, or motion choices can make a rendered UI appear inactive or inconsistent.

Mitigation: Apply the guardrails for i18n, Server-to-Client page layering, menu handlers, mounted route highlighting, reduced motion, and explicit verification steps.

Risk: Chinese-language workflow notes and examples may be misread by non-Chinese readers or copied with the wrong locale.

Mitigation: Translate the workflow text where needed and choose the project locale intentionally instead of copying locale="zh" blindly.

## Reference(s):

- [ORBCAFE Layout + Navigation on ClawHub](https://clawhub.ai/shenruiyang/skills/orbcafe-layout-navigation)
- [Layout Guardrails](references/guardrails.md)
- [Layout Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Hook-first layout decision, runtime safety checks, verification steps, and troubleshooting tips.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

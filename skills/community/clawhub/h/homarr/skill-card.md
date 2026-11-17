## Description:

Work on Homarr dashboards, board styling, custom CSS, iframe widgets, embedded mini-apps, native widgets, apps, and integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kretkas](https://clawhub.ai/user/kretkas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to choose safe, maintainable paths for Homarr dashboard customization, iframe embeds, native widgets, apps, and integrations. It helps classify tasks, avoid fragile CSS or unsupported extension assumptions, and verify Homarr-related changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested shell commands or configuration changes could be inappropriate for a user's Homarr deployment.

Mitigation: Review commands before running them and verify changes with the smallest meaningful Homarr lint, typecheck, test, or browser checks for the task.

Risk: Secrets could be exposed if API keys or tokens are placed in CSS, iframe URLs, or client-rendered code.

Mitigation: Keep API keys and tokens server-side through Homarr integration mechanisms, as directed by the skill and security guidance.

Risk: Iframe embeds can expose content or browser capabilities when permissions and board access are too broad.

Mitigation: Enable only required iframe permissions and confirm that public board access is appropriate for the embedded content.

Risk: Custom CSS can be fragile after Homarr or Mantine updates and can hide controls without enforcing authorization.

Mitigation: Prefer built-in Homarr board settings, scope CSS narrowly, avoid generated Mantine suffix classes, and rely on permissions rather than CSS for access control.

## Reference(s):

- [Homarr styling and custom CSS](references/styling.md)
- [Homarr iFrame widgets](references/iframe-widgets.md)
- [Homarr native widgets and integrations](references/native-widgets-integrations.md)
- [Homarr Styling](https://homarr.dev/docs/advanced/styling/)
- [Homarr Boards](https://homarr.dev/docs/management/boards/)
- [Homarr iFrame Widget](https://homarr.dev/docs/widgets/iframe/)
- [Homarr Apps](https://homarr.dev/docs/management/apps/)
- [Homarr Integrations](https://homarr.dev/docs/management/integrations/)
- [Homarr Widgets Catalog](https://homarr.dev/docs/category/widgets/)
- [Homarr Integrations Catalog](https://homarr.dev/docs/category/integrations/)
- [Homarr FAQ](https://homarr.dev/docs/community/faq/)
- [Homarr Developer Setup](https://homarr.dev/docs/advanced/development/getting-started/)
- [homarr-iframes](https://github.com/diogovalentte/homarr-iframes)
- [ClawHub skill page](https://clawhub.ai/kretkas/skills/homarr)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only helper; review suggested commands before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

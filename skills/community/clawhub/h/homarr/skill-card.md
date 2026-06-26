## Description: <br>
Work on Homarr dashboards, board styling, custom CSS, iframe widgets, embedded mini-apps, native widgets, apps, and integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kretkas](https://clawhub.ai/user/kretkas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Homarr dashboard maintainers use this skill to choose between built-in board settings, custom CSS, iframe embeds, integrations, and native Homarr source changes while keeping customizations maintainable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested pnpm, Docker, git, curl, or configuration commands may change local systems or services if run without review. <br>
Mitigation: Review each command before execution and run only the smallest meaningful lint, typecheck, test, or diagnostic command for the Homarr task. <br>
Risk: API keys, tokens, or integration secrets could be exposed if placed in CSS, iframe URLs, or client-rendered code. <br>
Mitigation: Keep secrets server-side through Homarr integration mechanisms and avoid embedding credentials in browser-visible surfaces. <br>
Risk: Over-broad iframe permissions or public board access can expose embedded content or unnecessary browser capabilities. <br>
Mitigation: Enable only the iframe permissions the embedded service needs and verify board access settings before publishing. <br>
Risk: Custom CSS can break after Homarr updates or hide controls without enforcing access control. <br>
Mitigation: Prefer built-in board settings, scope CSS to specific widgets, avoid generated Mantine suffix classes, and use permissions rather than CSS for security. <br>


## Reference(s): <br>
- [Homarr styling and custom CSS](references/styling.md) <br>
- [Homarr iFrame widgets](references/iframe-widgets.md) <br>
- [Homarr native widgets and integrations](references/native-widgets-integrations.md) <br>
- [Homarr styling documentation](https://homarr.dev/docs/advanced/styling/) <br>
- [Homarr boards documentation](https://homarr.dev/docs/management/boards/) <br>
- [Homarr iFrame widget documentation](https://homarr.dev/docs/widgets/iframe/) <br>
- [Homarr apps documentation](https://homarr.dev/docs/management/apps/) <br>
- [Homarr integrations documentation](https://homarr.dev/docs/management/integrations/) <br>
- [Homarr widgets catalog](https://homarr.dev/docs/category/widgets/) <br>
- [Homarr integrations catalog](https://homarr.dev/docs/category/integrations/) <br>
- [Homarr custom widgets FAQ](https://homarr.dev/docs/community/faq/) <br>
- [Homarr developer setup](https://homarr.dev/docs/advanced/development/getting-started/) <br>
- [homarr-iframes reference](https://github.com/diogovalentte/homarr-iframes) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review suggested commands before running them; keep secrets server-side; enable only required iframe permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Use markdown-it to render Markdown to HTML, configure plugins, custom rendering rules, syntax highlighting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need guidance for rendering Markdown to HTML with markdown-it, configuring parser options and plugins, adding syntax highlighting, or customizing renderer rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering untrusted Markdown with raw HTML enabled can expose users to cross-site scripting.

Mitigation: Keep markdown-it HTML parsing disabled unless a separate sanitization plan is in place.

Risk: Additional markdown-it plugins or npm packages may introduce behavior outside the base parser guidance.

Mitigation: Review plugin packages before adding them to a project, especially when rendering untrusted Markdown.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/markdown-it)
- [markdown-it Architecture Principles](references/architecture.md)
- [markdown-it Plugin Development](references/plugin-dev.md)
- [markdown-it plugin packages](https://www.npmjs.org/browse/keyword/markdown-it-plugin)
- [markdown-it source rules](https://github.com/markdown-it/markdown-it/tree/master/lib)
- [markdown-it linkify rule](https://github.com/markdown-it/markdown-it/blob/master/lib/rules_core/linkify.mjs)
- [markdown-it emoji replacement reference](https://github.com/markdown-it/markdown-it-emoji/blob/master/lib/replace.mjs)
- [markdown-it inline text rule](https://github.com/markdown-it/markdown-it/blob/master/lib/rules_inline/text.mjs)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes security guidance for rendering untrusted Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

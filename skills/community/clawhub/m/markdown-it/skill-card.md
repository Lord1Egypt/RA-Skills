## Description: <br>
Use markdown-it to render Markdown to HTML, configure plugins, custom rendering rules, syntax highlighting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to render Markdown to HTML with markdown-it, configure parser presets and plugins, customize renderer rules, set up syntax highlighting, and follow safe handling defaults for user-generated Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering Markdown from other users can expose unsafe HTML if raw HTML is enabled or the rendered output is not sanitized. <br>
Mitigation: Keep markdown-it's default html option disabled for user-generated Markdown and sanitize final HTML before display. <br>
Risk: Global npm installs and unpinned dependencies can make projects harder to audit or reproduce. <br>
Mitigation: Prefer project-local installs and pin markdown-it and plugin versions in real projects. <br>


## Reference(s): <br>
- [markdown-it Architecture Principles](references/architecture.md) <br>
- [markdown-it Plugin Development](references/plugin-dev.md) <br>
- [markdown-it plugin packages on npm](https://www.npmjs.org/browse/keyword/markdown-it-plugin) <br>
- [markdown-it source rules](https://github.com/markdown-it/markdown-it/tree/master/lib) <br>
- [markdown-it linkify rule](https://github.com/markdown-it/markdown-it/blob/master/lib/rules_core/linkify.mjs) <br>
- [markdown-it-emoji replacement rule](https://github.com/markdown-it/markdown-it-emoji/blob/master/lib/replace.mjs) <br>
- [markdown-it inline text rule](https://github.com/markdown-it/markdown-it/blob/master/lib/rules_inline/text.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes markdown-it configuration, plugin, renderer, CLI, and safety guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Provides sanitization guidelines for external content in skills and hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill when handling GitHub, web, URL, or other untrusted content so they can reduce prompt-injection and unsafe code-execution risks before passing that content to another skill or hook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact references automated sanitization, but the release does not include the hook that would perform that enforcement. <br>
Mitigation: Install the separate Claude Code plugin or another equivalent hook if automatic sanitization is required; otherwise apply the checklist manually. <br>
Risk: External content from web pages, GitHub, URLs, or public authors can contain prompt-injection or code-execution patterns. <br>
Mitigation: Treat that content as untrusted, limit size, strip instruction-like and execution-like patterns, remove hidden text, and wrap the content in explicit boundary markers before use. <br>


## Reference(s): <br>
- [Leyline plugin source](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-content-sanitization) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with checklists and safety constraints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only artifact; no executable files are included.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

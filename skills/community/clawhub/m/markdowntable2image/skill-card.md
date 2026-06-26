## Description: <br>
Convert markdown tables and JSON data to PNG images for chat platforms and other destinations where markdown tables render poorly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[umrzcz-831](https://clawhub.ai/user/umrzcz-831) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn tabular JSON or markdown table content into PNG images for Discord, Telegram, WhatsApp, financial reports, leaderboards, and comparison tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation downloads npm dependencies and a Playwright Chromium browser binary. <br>
Mitigation: Install only in environments where npm installation and a Chromium download are permitted. <br>
Risk: Rendered table images may expose sensitive input data if shared externally. <br>
Mitigation: Render only data intended for the target audience and review images before posting them to chat platforms. <br>
Risk: Custom theme or style inputs can affect generated HTML rendering behavior in sensitive environments. <br>
Mitigation: Avoid accepting untrusted custom theme or style inputs in locked-down or sensitive deployments. <br>


## Reference(s): <br>
- [Table2Image API Reference](references/api.md) <br>
- [Table2Image Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/umrzcz-831/markdowntable2image) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples and PNG image file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PNG buffers or files using Node.js, Playwright, and Chromium.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

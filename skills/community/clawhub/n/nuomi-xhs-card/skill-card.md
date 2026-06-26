## Description: <br>
Converts Markdown or MDX content into Xiaohongshu-style PNG card images with built-in templates, theme modes, pagination, and CLI controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangyijun](https://clawhub.ai/user/tangyijun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and agents use this skill to turn Markdown or MDX articles into styled social media card images and rendering reports through a local CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted Markdown, raw HTML, or MDX content may execute or render unexpected behavior inside Chromium. <br>
Mitigation: Use trusted input files, avoid --mdx-mode for content from others, and review generated preview/debug HTML before relying on the output. <br>
Risk: Image URLs or embedded remote resources in input content can contact external hosts during rendering. <br>
Mitigation: Prefer local assets, sanitize external URLs, or run rendering in a network-restricted environment when processing unfamiliar content. <br>
Risk: Installation downloads npm packages and Playwright Chromium. <br>
Mitigation: Review the package lock and install in an isolated environment before using the skill in sensitive workflows. <br>
Risk: Rendering writes PNG and report files to the chosen output directory. <br>
Mitigation: Choose an explicit output directory and inspect generated files before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangyijun/nuomi-xhs-card) <br>
- [Template reference](references/templates.md) <br>
- [CLI reference](references/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands; generated PNG files and an optional JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rendering writes card_*.png files and, when requested, report.json to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

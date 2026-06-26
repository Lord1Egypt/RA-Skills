## Description: <br>
OpenClaw UI Designer helps agents provide UI design advice, generate color palettes, and produce simple Tailwind-style component snippets for responsive and accessible interfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwg2025](https://clawhub.ai/user/williamwg2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product builders, and OpenClaw users can use this skill for UI design consultation, design-system guidance, color-palette generation, and starter component markup for web interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Design prompts may contain confidential product, customer, or credential details. <br>
Mitigation: Avoid placing secrets or sensitive business information in design prompts; the scanner guidance explicitly recommends not putting secrets in design prompts. <br>
Risk: Generated UI snippets and design guidance may be incomplete or unsuitable for a production interface. <br>
Mitigation: Review generated markup, styles, accessibility behavior, and responsive behavior before deployment. <br>
Risk: The README recommends unrelated skills that were not evaluated as part of this release. <br>
Mitigation: Evaluate each recommended skill separately before installing or using it. <br>
Risk: The component generator may write output when an explicit output path is used. <br>
Mitigation: Run scripts without elevated privileges and direct generated files to a reviewed project directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamwg2025/openclaw-ui-designer) <br>
- [Publisher profile](https://clawhub.ai/user/williamwg2025) <br>
- [Design UI Designer inspiration source](https://github.com/msitarzewski/agency-agents/blob/main/design/design-ui-designer.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text, with generated HTML/Tailwind snippets, CSS variables, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Component generation writes files only when an explicit output path is used; other documented scripts produce terminal output.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

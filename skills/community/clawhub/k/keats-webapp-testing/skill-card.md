## Description: <br>
Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corbin-breton](https://clawhub.ai/user/corbin-breton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to test and debug local web applications with Playwright, including browser automation, screenshots, rendered DOM inspection, and console-log review. It is intended for localhost or staging workflows, not live production targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can start local development servers and run automation commands. <br>
Mitigation: Review commands before execution and use the skill only for intended local or staging web-app testing workflows. <br>
Risk: The optional --shell mode runs server commands through the shell. <br>
Mitigation: Prefer the default non-shell mode and use --shell only for trusted commands that were written or inspected by the user. <br>
Risk: Using browser automation against production targets could exercise live systems unintentionally. <br>
Mitigation: Restrict usage to localhost or staging targets, consistent with the skill documentation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Playwright scripts, local server commands, selector analysis, screenshots paths, browser console observations, and configuration guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

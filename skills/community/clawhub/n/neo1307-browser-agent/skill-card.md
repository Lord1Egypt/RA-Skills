## Description: <br>
Browser Agent uses Playwright to open pages, take screenshots, inspect or interact with DOM elements, fill forms, extract text, and manage browser session state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when Codex needs deterministic browser automation for smoke-testing web pages, collecting DOM or screenshot evidence, and automating straightforward UI flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can operate on sensitive logged-in sessions when storage state is loaded or saved. <br>
Mitigation: Use saved sessions only for intended tasks, keep session files private, and delete them when no longer needed. <br>
Risk: Running browser actions against untrusted or unexpected sites can expose the agent to misleading page content or unintended interactions. <br>
Mitigation: Review target URLs and selectors before execution, and keep click and fill selectors explicit. <br>
Risk: The skill depends on local Playwright browser automation. <br>
Mitigation: Install Playwright from a trusted source and keep the runtime updated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neo1307/neo1307-browser-agent) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands] <br>
**Output Format:** [JSON stdout with optional PNG screenshot and Playwright storage-state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target URL and optional action flags such as screenshot, title, extract, click, fill, save-session, or load-session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

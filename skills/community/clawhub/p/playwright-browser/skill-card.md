## Description: <br>
Use Playwright to browse websites with a real non-headless Chrome or Chromium browser and extract rendered page content or captured network responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elijahxb](https://clawhub.ai/user/elijahxb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate browser visits, inspect rendered pages, click links, search content, and collect API responses from JavaScript-heavy sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes unrelated scripts that read local attendance files or save website images and reports to Desktop without clear disclosure. <br>
Mitigation: Review bundled scripts before installing and run only scripts/browser_agent.py unless those local or site-specific actions are intentional. <br>
Risk: Network response capture can expose sensitive content from logged-in or private browsing sessions. <br>
Mitigation: Use an isolated browser session, validate URLs before navigation, and avoid sensitive authenticated sites when API capture is enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elijahxb/playwright-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets and JSON-like browser result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch a non-headless browser and capture network responses; outputs depend on visited pages and scripts executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

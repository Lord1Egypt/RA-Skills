## Description: <br>
Captures web screenshots, retrieves page titles, and scrapes text or HTML content from web pages using a URL and optional CSS selector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dang-ngoc-duy](https://clawhub.ai/user/dang-ngoc-duy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect web pages by capturing screenshots, reading page titles, and extracting page text or selected HTML content. It is suitable for controlled browser automation workflows where the configured backend and screenshot destination are trusted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots may be sent to a hard-coded Telegram group without clear user control or destination scoping. <br>
Mitigation: Use only with pages and data approved for that Telegram destination, or change the skill to require explicit approval and a user-selected destination before sending screenshots externally. <br>
Risk: The browser backend is a private network endpoint whose trust boundary is not established by the release evidence. <br>
Mitigation: Install only if you control or trust the configured backend, and avoid authenticated pages, private dashboards, customer data, and internal systems unless the backend and destination are governed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dang-ngoc-duy/playwright-service) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, files] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screenshots are saved as image files before being sent to the configured Telegram destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

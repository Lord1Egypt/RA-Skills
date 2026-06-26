## Description: <br>
Operates web page elements through CDP and a Page JS Extension to reduce token use for UI automation testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TangJing](https://clawhub.ai/user/TangJing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to inspect page element indexes and issue click, fill, and select operations for UI automation on test or public web pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can click and type on web pages through browser automation. <br>
Mitigation: Use a dedicated browser profile with no saved credentials, limit use to test or public domains, and require confirmation before submit, save, delete, login, payment, upload, or account-changing actions. <br>
Risk: Element keys may contain visible page text that an agent could send to an LLM service. <br>
Mitigation: Avoid sensitive pages and ensure the agent's LLM configuration and data handling meet privacy requirements before using the skill. <br>
Risk: The workflow depends on a manually installed Chrome extension. <br>
Mitigation: Review the extension source and permissions before installation and periodically re-review updates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TangJing/page-js-operation) <br>
- [Page JS Extension Repository](https://github.com/TangJing/openclaw_access_web_page_js) <br>
- [Chrome Extensions Documentation](https://developer.chrome.com/docs/extensions/) <br>
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser automation guidance requiring Chrome DevTools Protocol access and a manually installed Page JS Extension.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

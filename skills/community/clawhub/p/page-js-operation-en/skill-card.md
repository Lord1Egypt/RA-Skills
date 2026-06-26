## Description: <br>
Operate web page elements via CDP and Page JS Extension, save 95% Token (for UI automation testing ONLY, NOT a web browsing tool). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TangJing](https://clawhub.ai/user/TangJing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to operate public or non-sensitive web page elements through CDP and a reviewed Page JS Extension for UI automation testing, regression checks, and page behavior validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with browser pages and should not be used on sensitive pages or pages containing private, financial, login, payment, medical, government, or business-sensitive information. <br>
Mitigation: Use it only for browser UI automation testing on public or non-sensitive test pages, with a separate browser profile and test accounts. <br>
Risk: The skill depends on an external Chrome extension. <br>
Mitigation: Review the extension source before installation and load it only when needed for testing. <br>
Risk: Element keys may contain page text that could be sent to LLM services by the agent configuration. <br>
Mitigation: Confirm the agent and LLM configuration meets privacy requirements before using the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TangJing/page-js-operation-en) <br>
- [Chrome Extension Source](https://github.com/TangJing/openclaw_access_web_page_js) <br>
- [Chrome Extension Documentation](https://developer.chrome.com/docs/extensions/) <br>
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CDP Runtime.evaluate JavaScript snippets and operational guidance for non-sensitive browser UI automation testing.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

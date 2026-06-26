## Description: <br>
Control Android Chrome via ADB and raw WebSocket CDP. No Playwright needed for navigate, JS injection, cookies, DOM, scroll, click. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laolaoshiren](https://clawhub.ai/user/laolaoshiren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to connect an Android Chrome browser through ADB and Chrome DevTools Protocol for navigation, JavaScript execution, cookie inspection or updates, DOM reading, scrolling, clicking, and screenshots through ADB. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CDP access can inspect or change an authenticated browser session, including cookies, page scripts, forms, and page content. <br>
Mitigation: Use an isolated test browser profile where possible and require explicit approval before reading cookies, modifying cookies, running page scripts, submitting forms, or taking screenshots. <br>
Risk: Exposing the forwarded Chrome DevTools port beyond localhost can allow unintended browser control from the network. <br>
Mitigation: Keep port 9222 local and avoid LAN exposure unless access is deliberately constrained and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laolaoshiren/phone-chrome-cdp) <br>
- [Publisher profile](https://clawhub.ai/user/laolaoshiren) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ADB setup commands, raw WebSocket CDP client code, and browser-control usage examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Mtop DevTools Socket lets agents connect to Mtop DevTools through a local socket or Chrome CDP to operate browser tabs, inspect page and network data, manage mocks and request rules, and make cookie-backed mtop or HTTP requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f-loat](https://clawhub.ai/user/f-loat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent debug web applications in an already-open browser, inspect mtop or HTTP traffic, manipulate tabs and page elements, collect screenshots and logs, and configure API mocks or request rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent powerful access to logged-in browser sessions, including cookie-backed requests and account switching or borrowing features. <br>
Mitigation: Install it only when the publisher is trusted and the intended browser accounts are approved for agent use; avoid personal, production, finance, or admin accounts unless explicitly permitted. <br>
Risk: Browser automation can execute JavaScript, upload files, change request rules, and modify API responses through mocks. <br>
Mitigation: Review each requested browser action, file upload, JavaScript evaluation, mock, and request-rule change before allowing it in sensitive sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/f-loat/mtop-devtools-socket) <br>
- [README](README.md) <br>
- [API parameter reference](references/api-reference.md) <br>
- [Usage examples](references/examples.md) <br>
- [Socket troubleshooting](references/troubleshooting.md) <br>
- [Mtop DevTools](https://mtop-devtools.io.alibaba-inc.com) <br>
- [Mtop DevTools Chrome extension](https://chromewebstore.google.com/detail/mtop-devtools/aoehhjnofngknnjefamjbplchbolghkm) <br>
- [Skill setup](https://mtop-devtools.io.alibaba-inc.com/skill-setup.txt) <br>
- [Ali Skills Mtop DevTools page](https://ali-skills.alibaba-inc.com/skills/trip/mtop-devtools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload examples; tool calls may return structured browser, network, console, mock, screenshot, or page-state data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save screenshots or selected-element captures to local files when an output path is supplied.] <br>

## Skill Version(s): <br>
1.36.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

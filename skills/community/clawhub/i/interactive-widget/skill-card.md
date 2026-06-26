## Description: <br>
Create shareable interactive web pages such as dashboards, charts, forms, simulations, and parameter pickers through the duoduo-widget CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuaner](https://clawhub.ai/user/kuaner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a response needs a durable, browser-accessible interactive artifact instead of plain chat text, including visualizations, sortable tables, forms, and approval flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Widgets can publish permanent browser pages through an external widget service, which may expose widget contents beyond the current conversation. <br>
Mitigation: Use the skill only when publication is intentional, avoid secrets, credentials, private customer data, and sensitive personal information, and review content before finalizing. <br>
Risk: The skill works with raw HTML snippets, so untrusted values can become unsafe or misleading page content if inserted directly. <br>
Mitigation: Sanitize or text-escape untrusted values before inserting them into HTML, and keep forbidden browser APIs such as fetch, XMLHttpRequest, WebSocket, eval, and new Function out of widgets. <br>
Risk: The workflow depends on the duoduo-widget npm package and hosted widget service, including control tokens for draft updates. <br>
Mitigation: Install and use it only if you trust the package and service, and never share control URLs or control tokens with users. <br>


## Reference(s): <br>
- [Interactive Widget on ClawHub](https://clawhub.ai/kuaner/interactive-widget) <br>
- [Widget service](https://aidgets.dev) <br>
- [Widget HTML Templates](references/html_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, HTML snippets, and CLI patch or finalize examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include hosted widget links, HTML sections, incremental patch JSON, and instructions for waiting on submitted interactions.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

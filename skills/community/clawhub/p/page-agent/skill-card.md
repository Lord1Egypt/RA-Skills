## Description: <br>
Enhances browser automation by injecting PageAgent's page-controller into controlled web pages for DOM extraction, indexed element detection, clicking, typing, scrolling, form filling, and page-structure inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DongDongBear](https://clawhub.ai/user/DongDongBear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect and operate controlled browser pages with finer DOM-level actions than basic browser controls. It is suited for page testing, form interaction, UI iteration, and reading simplified page structure during browser-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unrestricted JavaScript execution can read or change state inside any controlled web page. <br>
Mitigation: Use an isolated OpenClaw browser profile and avoid banking, admin, production, email, or other sensitive authenticated sites unless that level of access is explicitly intended. <br>
Risk: CDP injection gives the agent powerful control over the selected browser target. <br>
Mitigation: Confirm the intended target page before injection, review generated actions before execution, and re-read page state after actions that change the DOM. <br>


## Reference(s): <br>
- [PageAgent Browser Enhancement on ClawHub](https://clawhub.ai/DongDongBear/page-agent) <br>
- [alibaba/page-agent](https://github.com/alibaba/page-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript snippets; runtime page state may be returned as text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a controlled browser target and reinjection after full page reloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

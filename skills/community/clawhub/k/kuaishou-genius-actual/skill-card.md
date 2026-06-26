## Description: <br>
Use this skill whenever the user asks to analyze, verify, debug, reverse-engineer, or automate Kuaishou Genius「预算/预测/实际」页面 data flow (especially management-yearly/actual). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpei03](https://clawhub.ai/user/zhangpei03) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to map, validate, and troubleshoot the Kuaishou Genius management-yearly actual data flow. It helps reconstruct endpoint order, required request parameters, and script-based checks for authorized debugging of the internal Genius system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to reuse live corporate session cookies. <br>
Mitigation: Use only authorized Kuaishou sessions, avoid sharing cookies, and treat command output as confidential. <br>
Risk: The scripts probe internal financial or business APIs. <br>
Mitigation: Run probes only for approved debugging work on the intended corporate domain and review captured payloads or responses before sharing. <br>
Risk: The Python client supports disabling TLS verification with --insecure. <br>
Mitigation: Avoid --insecure except in explicitly approved diagnostic environments, and keep TLS verification enabled for normal use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhangpei03/kuaishou-genius-actual) <br>
- [Publisher Profile](https://clawhub.ai/user/zhangpei03) <br>
- [Genius Actual Page](https://genius.corp.kuaishou.com/management-yearly/actual) <br>
- [Genius Base Domain](https://genius.corp.kuaishou.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, endpoint maps, JSON payload guidance, and concise diagnostic reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API call order, required payload fields, blockers, and next actions for authorized debugging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

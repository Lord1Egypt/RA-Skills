## Description: <br>
Automates MiroMind deep research through OpenClaw by using Playwright MCP to submit a topic to dr.miromind.ai, monitor the run, and save a Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karminski](https://clawhub.ai/user/karminski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research analysts use this skill to run MiroMind research sessions from OpenClaw for financial analysis, technology research, fact-checking, trend forecasting, or company analysis. The skill returns research status, a chat URL, and a locally saved Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MiroMind account credentials and sends research questions to dr.miromind.ai. <br>
Mitigation: Use a dedicated MiroMind account where possible, avoid submitting secrets or regulated data, and protect the OpenClaw configuration that stores the password. <br>
Risk: Generated reports are saved under the local OpenClaw workspace. <br>
Mitigation: Review saved reports for sensitive content and manage local access and retention according to your policy. <br>


## Reference(s): <br>
- [MiroMind](https://dr.miromind.ai) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub Miromind Skill Page](https://clawhub.ai/karminski/miromind) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Text response with a chat URL and local Markdown report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MIROMIND_EMAIL and MIROMIND_PASSWORD; reports are saved under the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

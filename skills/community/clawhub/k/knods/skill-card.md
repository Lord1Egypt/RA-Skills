## Description: <br>
Build and modify Knods visual AI workflows using either the OpenClaw Gateway polling protocol or the Knods headless flows API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alesys](https://clawhub.ai/user/alesys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw agents with Knods Iris chat and to drive Knods flows programmatically. It supports canvas mutation actions, flow discovery, schema inspection, run execution, polling, cancellation, and output retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged bridge installs and runs an always-on user service for polling Knods messages. <br>
Mitigation: Install only when continuous bridge polling is needed, and stop or disable the user service when it is not in use. <br>
Risk: Gateway-token URLs may appear in service logs. <br>
Mitigation: Use dedicated, revocable Knods tokens with minimal scopes, avoid sharing service logs, and rotate any gateway token already used with this version. <br>


## Reference(s): <br>
- [Knods skill page](https://clawhub.ai/alesys/knods) <br>
- [Project homepage](https://github.com/alesys/openclaw-skill-knods) <br>
- [OpenClaw Gateway Protocol](references/protocol.md) <br>
- [Knods Headless Flow Execution API](references/headless-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Assistant text with inline Knods action JSON blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stream gateway responses by messageId and may print JSON responses from the packaged headless client.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

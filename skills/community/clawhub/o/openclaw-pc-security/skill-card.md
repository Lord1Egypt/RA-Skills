## Description: <br>
Local security self-check for your Windows PC and OpenClaw server setup (password protection, port, and exposure), producing a local report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawvincent](https://clawhub.ai/user/openclawvincent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT administrators, and OpenClaw users use this skill to audit Windows patch posture, OpenClaw CLI freshness, and OpenClaw server exposure. It supports local report generation and optional authorized OpenClaw service checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can include system, network, and configuration details. <br>
Mitigation: Review reports before sharing and send them only through an approved secure destination. <br>
Risk: Target scans and credential checks can affect systems outside the user's authorization. <br>
Mitigation: Run target scans and credential checks only against systems the user owns or is explicitly authorized to test. <br>
Risk: The bundled mock server can expose test behavior if run in an inappropriate environment. <br>
Mitigation: Run the mock server only in an isolated test environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawvincent/openclaw-pc-security) <br>
- [Skill README](artifact/README.md) <br>
- [Microsoft Security Response Center CVRF API](https://api.msrc.microsoft.com/cvrf/v2.0/cvrf/{cid}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated reports may be JSON or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include system, network, and configuration details and should be reviewed before sharing.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

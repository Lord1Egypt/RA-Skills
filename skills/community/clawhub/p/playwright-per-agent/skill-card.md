## Description: <br>
Per-agent Playwright browser pool: shared/per-agent/ephemeral + subagent inherit. Reads openclaw.json. Requires node, playwright. Local-only; no data forwarded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to launch and reuse local Playwright browser sessions with shared, per-agent, or ephemeral profiles. It helps separate browser cookies, storage, CDP ports, and processes across agents when workflows need browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser sessions may intentionally persist or share cookies and local storage depending on the selected mode. <br>
Mitigation: Use per-agent or ephemeral mode for separate accounts or sensitive sites; use shared mode only when agents may act as the same browser identity. <br>
Risk: A shared registry path on a multi-user machine can expose browser-session coordination metadata to other local users. <br>
Mitigation: Set AGENT_BROWSER_REGISTRY to a private per-user path on shared machines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/axelhu/playwright-per-agent) <br>
- [Profile Strategies](references/profile-strategies.md) <br>
- [Why .mjs](references/why-mjs.md) <br>
- [Example Configuration](assets/example-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript, TypeScript, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide agents toward local Playwright browser-session setup and use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

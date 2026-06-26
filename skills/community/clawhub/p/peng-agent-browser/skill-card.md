## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penglovemeng](https://clawhub.ai/user/penglovemeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to drive browser sessions through agent-browser for web UI automation, structured page inspection, form interaction, screenshots and PDFs, recording, session state, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over browser sessions, including logged-in sessions and local file uploads. <br>
Mitigation: Use test accounts or isolated sessions where possible, and require explicit user approval before uploads, credential entry, account-changing actions, cookie or storage access, recording, tracing, or network interception. <br>
Risk: Saved browser state files can contain sensitive cookies, tokens, or account session data. <br>
Mitigation: Protect saved state files like credentials, limit access to them, and do not commit them to source control. <br>
Risk: Browser automation can interact with real websites and accounts in ways that may change data or expose private information. <br>
Mitigation: Review targets and commands before execution, prefer isolated browser sessions, and avoid running against production accounts unless the action has been approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/penglovemeng/peng-agent-browser) <br>
- [agent-browser upstream CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with bash command examples; agent-browser commands may return text, JSON, screenshots, PDFs, traces, recordings, or saved browser state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, and the agent-browser CLI; browser state, recordings, traces, screenshots, and uploaded files may persist outside the chat transcript.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

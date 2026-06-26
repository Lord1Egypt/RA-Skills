## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujiang817](https://clawhub.ai/user/liujiang817) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to drive browser sessions from agent workflows for navigation, form filling, UI testing, screenshots, recordings, and structured page extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser recordings, traces, screenshots, and saved sessions can contain sensitive login data. <br>
Mitigation: Store generated artifacts privately, avoid recording sensitive accounts unless necessary, and delete artifacts when finished. <br>
Risk: Saved browser sessions can reuse authenticated state. <br>
Mitigation: Install and use the skill only when reuse of logged-in browser sessions is acceptable, and treat session-state files like secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liujiang817/my-agent-browser) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to produce browser screenshots, PDFs, videos, traces, JSON snapshots, and saved session-state files through the agent-browser CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

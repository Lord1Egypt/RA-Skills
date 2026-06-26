## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingxiangmiu](https://clawhub.ai/user/mingxiangmiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to control browser sessions, extract structured page information, fill forms, test web UIs, and capture browser artifacts through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad browser-control powers over authenticated web sessions. <br>
Mitigation: Use test or least-privilege accounts and require explicit approval before purchases, posts, uploads, deletions, or administrative changes. <br>
Risk: Saved state files, cookies, storage dumps, screenshots, PDFs, videos, traces, and network logs can contain sensitive data. <br>
Mitigation: Protect these artifacts as secrets, limit access to them, and delete them when they are no longer needed. <br>
Risk: The skill depends on an external agent-browser package. <br>
Mitigation: Install and use the skill only when the external package and its source are trusted for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mingxiangmiu/miu) <br>
- [agent-browser upstream repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference browser artifacts such as screenshots, PDFs, videos, traces, network logs, cookies, storage data, and saved session state.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

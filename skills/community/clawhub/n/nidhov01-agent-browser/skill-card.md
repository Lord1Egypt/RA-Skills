## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to drive the agent-browser CLI for web navigation, page inspection, form filling, UI testing, screenshots, recordings, and structured data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can perform high-impact actions in real accounts, including uploads, purchases, account changes, credential entry, or public posts. <br>
Mitigation: Use test accounts when possible and manually confirm high-impact actions before execution. <br>
Risk: Saved sessions, recordings, screenshots, and uploads can expose sensitive account data. <br>
Mitigation: Keep auth state, screenshots, recordings, and uploaded files out of shared or committed folders; store them securely and delete captures when finished. <br>


## Reference(s): <br>
- [ClawHub Agent Browser release](https://clawhub.ai/nidhov01/nidhov01-agent-browser) <br>
- [agent-browser CLI project](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issues](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text, json, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; agent-browser can return text, JSON, screenshots, PDFs, traces, and recordings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm to install the CLI; browser actions may use saved state, sessions, screenshots, recordings, and uploaded files.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

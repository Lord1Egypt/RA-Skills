## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junxuan666](https://clawhub.ai/user/junxuan666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to drive browser automation from an agent, including page navigation, interactive element discovery, form entry, screenshots, recording, network inspection, and saved browser state workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external agent-browser package or source repository. <br>
Mitigation: Install only from trusted sources and confirm the package or repository before enabling the skill in an agent environment. <br>
Risk: Saved browser state, authentication files, screenshots, recordings, traces, and captures can contain sensitive data. <br>
Mitigation: Use disposable or least-privilege accounts, keep saved state and captures out of version control, and delete them when the automation task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/junxuan666/junxuan) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some referenced agent-browser commands can emit JSON when run with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

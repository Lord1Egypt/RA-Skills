## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[handy01](https://clawhub.ai/user/handy01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate browser workflows with deterministic accessibility-tree snapshots, ref-based element interaction, session isolation, state persistence, screenshots, PDFs, and network controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser state files, cookies, localStorage, sessionStorage, persistent profiles, screenshots, traces, and videos may contain sensitive account or session data. <br>
Mitigation: Use isolated test accounts where possible, avoid unnecessary personal or production account access, treat generated browser artifacts as secrets, and delete saved auth state after the task. <br>
Risk: Browser automation can perform actions on live websites or authenticated sessions. <br>
Mitigation: Review target URLs and commands before execution, keep sessions isolated for different roles, and use the skill only when browser automation is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/handy01/handy01-agent-browser) <br>
- [agent-browser homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser state files, screenshots, traces, videos, and PDFs through agent-browser commands.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

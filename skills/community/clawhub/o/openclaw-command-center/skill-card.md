## Description: <br>
Mission control dashboard for OpenClaw - real-time session monitoring, LLM usage tracking, cost intelligence, and system vitals. View all your AI agents in one place. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jontsai](https://clawhub.ai/user/jontsai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw operators use this skill to run a local dashboard for monitoring AI sessions, LLM usage, costs, scheduled jobs, and system vitals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard exposes sensitive agent data and operational controls with under-scoped default access protections. <br>
Mitigation: Install it only for intended OpenClaw administration, bind it to localhost or a trusted interface, and enable token, Tailscale, or Cloudflare Access before remote use. <br>
Risk: Operators, Memory, Sessions, Jobs, and Cerebro views can reveal sensitive operational data. <br>
Mitigation: Restrict access to trusted users and networks, and avoid public tunnels unless strong access controls are configured. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jontsai/openclaw-command-center) <br>
- [README](README.md) <br>
- [Architecture Overview](docs/architecture/OVERVIEW.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Dashboard, API data] <br>
**Output Format:** [Local web dashboard, REST/SSE API responses, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Node.js dashboard server; Node.js >=18 is required.] <br>

## Skill Version(s): <br>
1.4.1 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

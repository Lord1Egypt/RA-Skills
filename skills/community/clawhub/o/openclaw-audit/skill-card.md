## Description: <br>
Audit your OpenClaw configuration against 12 production primitives PLUS 8 common setup footguns (silent cost leaks, prompt-injection paths, zombie session state, dead fallbacks). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnpetros](https://clawhub.ai/user/shawnpetros) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect a local OpenClaw setup after initial configuration, major changes, migrations, or periodic health checks. It returns severity-ranked findings and concrete fixes for production readiness and common setup risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit reads sensitive local OpenClaw configuration paths and setup files. <br>
Mitigation: Run it only when you want local OpenClaw settings inspected, and do not allow the agent to read or quote secret values. <br>
Risk: Audit output may reveal operational details such as API keys, paths, hostnames, session details, or provider names if shared as-is. <br>
Mitigation: Redact sensitive values and environment-specific details before sharing the findings outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shawnpetros/openclaw-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown structured by severity with scores and prioritized fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are ranked critical, warning, and info, with top fixes and a 0/20 audit score.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

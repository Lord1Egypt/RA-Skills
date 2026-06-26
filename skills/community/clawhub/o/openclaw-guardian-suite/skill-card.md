## Description: <br>
Openclaw Guardian is a commercial OpenClaw guardian suite that installs operational skills for configuration safety, model failover, health monitoring, context compaction, and safer skill installation after license verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
Proprietary - Commercial License <br>


## Use Case: <br>
Developers and operators use this skill to deploy an OpenClaw guardian bundle that protects configuration changes, supports rollback and failover workflows, audits health, reduces long-context overhead, and guides safer skill installation. It is intended for paid, licensed OpenClaw environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation delegates execution to server-delivered shell code from skill.socialmore.net. <br>
Mitigation: Install only when the publisher and delivery server are trusted, and prefer a signed, version-pinned bundle that can be inspected before execution. <br>
Risk: The suite can make persistent OpenClaw trust, route, and configuration changes. <br>
Mitigation: Review allowBundled entries and route/configuration changes, then test in an isolated OpenClaw profile before use in a real environment. <br>
Risk: Remote prompt execution and route configuration may expose secrets or private paths if misused. <br>
Mitigation: Avoid passing secrets, API keys, or private filesystem paths to remote prompt execution and review generated route templates before adding credentials. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/halfmoon82/openclaw-guardian-suite) <br>
- [Publisher profile](https://clawhub.ai/user/halfmoon82) <br>
- [Bundled OpenClaw marketplace link](https://clawhub.openclaw.cc/skills/openclaw-guardian-suite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration guidance, and installed skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local OpenClaw skill content and configuration changes after license-gated installation.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

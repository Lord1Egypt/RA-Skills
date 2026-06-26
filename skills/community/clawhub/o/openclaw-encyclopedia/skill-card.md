## Description: <br>
OpenClaw Encyclopedia gives agents a documentation-first workflow for OpenClaw product, runtime, configuration, troubleshooting, automation, security, and operational questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklouzal](https://clawhub.ai/user/kklouzal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when working with OpenClaw behavior, CLI usage, configuration review, live troubleshooting, automation planning, and local operational documentation. It helps agents prefer official OpenClaw documentation and clearly separate official docs, observed local state, and inferred guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workspace-local cache and notes can preserve operational details from an OpenClaw environment. <br>
Mitigation: Review .OpenClaw-Encyclopedia notes before sharing a workspace and do not store secrets, tokens, private URLs, recovery codes, or sensitive access details there. <br>
Risk: OpenClaw operational guidance can affect gateway, session, channel, automation, skill, plugin, or security behavior. <br>
Mitigation: Consult the relevant official OpenClaw documentation and inspect current state before applying commands or configuration changes, especially in high-sensitivity areas. <br>


## Reference(s): <br>
- [OpenClaw Encyclopedia on ClawHub](https://clawhub.ai/kklouzal/openclaw-encyclopedia) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) <br>
- [Workflow Reference](references/workflow.md) <br>
- [Cache Layout Reference](references/cache-layout.md) <br>
- [Topic Map Reference](references/topic-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a workspace-local .OpenClaw-Encyclopedia cache and notes tree.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

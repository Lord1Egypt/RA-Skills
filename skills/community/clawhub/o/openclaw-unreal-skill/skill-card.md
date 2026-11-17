## Description:

Control Unreal Engine Editor via OpenClaw Unreal Plugin for level and actor management, transforms, PIE control, debugging, input simulation, console commands, screenshots, and logs, with project-changing operations gated by runtime opt-in and per-call confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomleelive](https://clawhub.ai/user/tomleelive)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and technical artists use this skill to inspect and control trusted local Unreal Engine Editor projects through OpenClaw. It supports read-only scene inspection by default and allows explicit, confirmed project-changing editor operations when enabled by the operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gateway bridge path may lack a clear authentication boundary.

Mitigation: Install only for trusted local Unreal projects, keep the gateway and Unreal bridge off untrusted networks, and prefer an OpenClaw gateway version with authenticated route registration.

Risk: Project-changing Unreal Editor actions can modify actors, levels, assets, PIE state, console state, or simulated input.

Mitigation: Keep destructive operations disabled unless needed, require operator opt-in with OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE or OPENCLAW_UNREAL_ALLOW_DESTRUCTIVE, and pass confirm: true only after approving the specific action.

Risk: Screenshots and logs can expose secrets, tokens, local paths, or project details.

Mitigation: Review screenshots and logs before sharing them outside the local machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomleelive/skills/openclaw-unreal-skill)
- [OpenClaw Unreal Plugin](https://github.com/openclaw/openclaw-unreal-plugin)
- [Skill homepage](https://github.com/TomLeeLive/openclaw-unreal-skill)
- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured tool-call guidance with inline code or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide Unreal Editor read-only inspection, dry-run previews, screenshots, log review, and confirmed project-changing actions through OpenClaw.]

## Skill Version(s):

1.1.0 (source: frontmatter, changelog, package.json, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

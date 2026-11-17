## Description:

Controls the Unity Editor through OpenClaw so agents can inspect scenes, modify GameObjects and assets, debug projects, simulate input, control Play mode, run tests, and execute C# with gated project-changing operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomleelive](https://clawhub.ai/user/tomleelive)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to automate Unity Editor workflows through OpenClaw, including scene inspection, object and asset manipulation, debugging, gameplay or UI testing, and controlled project-changing actions in trusted projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unity Editor control can change scenes, assets, packages, settings, and run C# inside the Editor process.

Mitigation: Use only with trusted, version-controlled Unity projects; preview risky calls with dryRun, and enable project-changing calls only with the runtime opt-in plus confirm: true.

Risk: The legacy gateway HTTP path can expose and accept Unity session traffic without equivalent authentication.

Mitigation: Keep the gateway and Unity bridge on localhost or a trusted network, and prefer an OpenClaw version that uses authenticated registerHttpRoute.

## Reference(s):

- [OpenClaw Unity Skill on ClawHub](https://clawhub.ai/tomleelive/skills/openclaw-unity-skill)
- [Unity Plugin Tools Reference](references/tools.md)
- [OpenClaw Unity Plugin](https://github.com/TomLeeLive/openclaw-unity-plugin)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool calls, shell commands, and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide agents and gateway calls for a connected Unity Editor; project-changing calls require runtime opt-in and per-call confirmation.]

## Skill Version(s):

1.7.0 (source: SKILL.md frontmatter, extension/package.json, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Connects OpenClaw or other OpenAI-compatible clients to a local kiro-cli ACP backend with streaming responses and tool-call support.

This skill is for research and development only.

## Publisher:

[luoshixi](https://clawhub.ai/user/luoshixi)

### License/Terms of Use:

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

## Use Case:

Developers and engineers use this skill to run a local bridge that translates OpenAI or Anthropic-compatible chat requests into Kiro CLI ACP sessions for project work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Any process able to reach the local bridge may be able to drive Kiro with local file and command privileges.

Mitigation: Keep the service bound to 127.0.0.1 and do not expose the port through tunnels, proxies, containers, or shared machines.

Risk: Weakly controlled local APIs and auto-approved permissions can allow unintended file or command actions.

Mitigation: Use a dedicated low-privilege workspace without secrets and review activity before using it on sensitive projects.

Risk: Real authentication, explicit per-action approval, project-directory containment, and restricted command execution are not evidenced.

Mitigation: Prefer versions that add those controls before broader use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luoshixi/skills/kiro-cli-openclaw-bridge)
- [Project Homepage](https://github.com/LuoShiXi/kiro-cli-openclaw-bridge)
- [Kiro](https://kiro.dev)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup, run, verification, and OpenClaw provider configuration guidance.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

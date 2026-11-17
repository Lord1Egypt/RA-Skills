## Description:

Complete Oblien workspace environment reference covering the Firecracker microVM runtime, gateway JWT and raw-token authentication, and the Internal API for files, search, command execution, terminal sessions, and file watchers on port 9990.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hydralerne](https://clawhub.ai/user/hydralerne)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill as a reference for operating Oblien workspaces, connecting to the workspace Internal API, and managing files, command execution, terminal sessions, search, and file watchers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad workspace control, including file writes and deletes, command execution, terminals, and file watchers.

Mitigation: Install and use it only when agents are intended to operate Oblien workspaces at a high privilege level, and require clear user intent before destructive or execution-capable operations.

Risk: Gateway JWTs, raw tokens, client IDs, and client secrets can expose workspace access if printed, logged, or retained in transcripts.

Mitigation: Handle all authentication material as secrets, avoid placing tokens in logs or transcripts, and rotate tokens after use.

Risk: Direct raw-token HTTP access can bypass the gateway path and is intended only for authorized private workspace links.

Mitigation: Prefer scoped SDK or gateway flows where possible, and use direct raw-token HTTP only when the private link is explicitly authorized.

## Reference(s):

- [Oblien Documentation](https://oblien.com/docs)
- [Oblien Runtime Skill Page](https://clawhub.ai/hydralerne/skills/oblien-runtime)
- [ripgrep](https://github.com/BurntSushi/ripgrep)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown reference with SDK, REST, cURL, SSE, and WebSocket examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authentication guidance, endpoint parameters, response schemas, and operational limits.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

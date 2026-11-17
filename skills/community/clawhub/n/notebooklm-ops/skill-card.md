## Description:

Manage the NotebookLM MCP authentication lifecycle on Linux by automating GUI startup, authentication refresh, status checks, smoke tests, and cleanup for frequent cookie expiry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiceman161](https://clawhub.ai/user/spiceman161)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to start, stop, refresh, and check NotebookLM MCP authentication on a Linux host where Google session cookies expire frequently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Google browser control through VNC/CDP could expose a session if reachable by untrusted users.

Mitigation: Use a dedicated low-privilege Google account or browser profile, and bind VNC/CDP only to trusted local interfaces with appropriate access controls.

Risk: The skill delegates to local scripts outside the artifact, so runtime behavior depends on files not bundled with this release.

Mitigation: Inspect the referenced /home/moltuser/clawd scripts before running the skill and keep those files writable only by trusted users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spiceman161/skills/notebooklm-ops)
- [NotebookLM](https://notebooklm.google.com/)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may affect local Chromium, VNC/CDP, GUI, and NotebookLM MCP processes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

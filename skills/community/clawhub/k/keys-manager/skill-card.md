## Description: <br>
Manage API keys locally from the terminal using the `keys` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stym06](https://clawhub.ai/user/stym06) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to store, retrieve, search, import, export, inject, audit, sync, and organize local API keys and secrets through the `keys` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent reveal, export, sync, or delete credentials from a local secret store. <br>
Mitigation: Use targeted retrieval or command-specific injection, confirm destructive actions, and avoid broad export or `.env` writes unless they are necessary. <br>
Risk: `eval $(keys expose)` can place many secrets into the active shell environment. <br>
Mitigation: Prefer `keys get <name>` for a single key or `keys inject` for one command, and avoid evaluating broad export output. <br>
Risk: Non-macOS systems may allow lower-friction credential access, and sync operations transfer secrets across reachable networks. <br>
Mitigation: Use the skill only on trusted machines and networks, verify the active profile and passphrase before sync, and audit key access when secrets are used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stym06/keys-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external `keys` CLI binary.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

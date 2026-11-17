## Description:

This skill helps users bootstrap OpenClaw with Hippocampus memory by setting up a workspace, agent ID, authentication, and MCP wiring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cezexpl](https://clawhub.ai/user/cezexpl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect a new OpenClaw instance or workspace to Hippocampus memory, configure identity and authentication, and verify an initial store/search round trip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to run an unpinned external npm package.

Mitigation: Use only a verified official package or source, and prefer an exact pinned version before running setup.

Risk: Bootstrap credentials or long-lived API keys could be exposed through shell history or reused across workspaces.

Mitigation: Prefer a short-lived, single-use, scoped, and revocable bootstrap token, and avoid placing long-lived credentials in shell history.

Risk: Local setup writes configuration under ~/.hipokamp/config.json, which may contain sensitive authentication material.

Mitigation: Inspect the generated config file and its filesystem permissions after setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cezexpl/skills/hippocampus-openclaw-onboarding)
- [Publisher profile](https://clawhub.ai/user/cezexpl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with an inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup flow, credential handling guidance, and related package pointers.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

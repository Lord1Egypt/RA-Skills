## Description:

Per-agent Playwright browser pool: shared/per-agent/ephemeral + subagent inherit. Reads openclaw.json. Requires node, playwright. Local-only; no data forwarded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to give OpenClaw agents separate or shared Playwright browser sessions, manage persistent or ephemeral profiles, and attach to active browser contexts across processes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared browser mode can expose logged-in session state across agents on the same machine.

Mitigation: Use per-agent or ephemeral mode for sensitive accounts, and avoid shared mode when account isolation matters.

Risk: The default cross-process browser registry path may expose active browser metadata on shared systems.

Mitigation: Set the registry path to a private user-owned location and run the browser pool as a non-root local user.

Risk: Unsafe Chromium defaults can weaken browser isolation for valuable logged-in sessions.

Mitigation: Use a pinned Playwright version with Chromium sandboxing enabled before relying on this skill for sensitive browsing.

## Reference(s):

- [Profile Strategies](artifact/references/profile-strategies.md)
- [Example Configuration](artifact/assets/example-config.json)
- [ClawHub Skill Page](https://clawhub.ai/axelhu/skills/playwright-per-agent)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local browser-session setup and usage guidance; no data forwarding is claimed by the release evidence.]

## Skill Version(s):

1.0.1 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

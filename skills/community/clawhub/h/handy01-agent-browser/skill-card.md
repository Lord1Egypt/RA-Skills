## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handy01](https://clawhub.ai/user/handy01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser workflows with deterministic accessibility-tree snapshots, ref-based actions, isolated sessions, and JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help an agent automate authenticated browser sessions.

Mitigation: Use isolated environments and avoid high-sensitivity accounts unless isolation and access controls are in place.

Risk: Saved auth state can preserve reusable cookies and storage.

Mitigation: Keep auth JSON files private, short-lived, access-controlled, and deleted after use.

Risk: Installation may download npm packages, Chromium, or system dependencies.

Mitigation: Pin the npm package version and review downloads before using install commands, especially --with-deps.

## Reference(s):

- [Agent Browser repository](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/handy01/skills/handy01-agent-browser)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for browser navigation, interaction, state persistence, screenshots, PDFs, network control, cookies, storage, tabs, and frames.]

## Skill Version(s):

0.1.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

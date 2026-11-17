## Description:

Build, test, and list Hup mini apps: web apps that run inside Hup social posts and transact through the viewer's existing Hup wallet session via the Hup SDK bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3senior](https://clawhub.ai/user/web3senior)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scaffold, debug, port, and prepare Hup mini apps for listing and embed review. It focuses on Hup's SDK-only wallet bridge, fixed-frame app constraints, wallet method policy, and common embed diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable live Hup documentation and a demo that can load unpinned SDK code.

Mitigation: Use the bundled snapshot for review, fetch the live specification deliberately, and pin or control SDK loading before working with real wallet sessions or deployed mini apps.

Risk: Wallet or embed flows can fail if an app bypasses the Hup SDK bridge, calls refused wallet methods, or is served with framing restrictions.

Mitigation: Use only the Hup SDK provider, test refused methods and disconnected-user states, and verify framing headers before listing or requesting embed review.

## Reference(s):

- [Hup Mini App Skill Spec](https://hup.social/miniapp-skill.md)
- [Hup Mini App SDK](https://hup.social/miniapp-sdk.js)
- [Hup Apps Directory](https://hup.social/apps)
- [Mini App Guide Snapshot](references/miniapp-guide.md)
- [Demo App Reference](references/demo-app.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with HTML, JavaScript, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to fetch the live Hup mini app specification before building.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

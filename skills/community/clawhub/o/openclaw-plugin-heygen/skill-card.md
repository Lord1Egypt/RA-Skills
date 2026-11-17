## Description:

HeyGen Video Agent adds HeyGen as an OpenClaw video_generate provider for identity-first avatar presenter videos using scripts, avatar IDs, voices, and provider options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eve-builds](https://clawhub.ai/user/eve-builds)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this plugin to generate presenter-led HeyGen videos through OpenClaw's standard video_generate interface for outreach, announcements, pitch decks, walkthroughs, and similar scripted avatar content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-driven install instructions can point users to mutable remote setup content.

Mitigation: Review the release artifact and prefer the local bundled install instructions before installing.

Risk: HEYGEN_API_KEY can be exposed if pasted into chat, printed, or logged during setup.

Mitigation: Use OpenClaw's private onboarding flow or a local environment variable, avoid echoing the key, and rotate any key exposed in logs or transcripts.

Risk: Default-provider settings and webhook callbacks can affect account spend and data flow.

Mitigation: Enable default-provider configuration and callback URLs only after confirming the account and data-flow impact.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/eve-builds/skills/openclaw-plugin-heygen)
- [HeyGen setup notes](docs/heygen.md)
- [HeyGen API docs](https://docs.heygen.com)
- [HeyGen Video Agent API reference](https://developers.heygen.com/reference/list-video-agent-sessions.md)
- [OpenClaw plugin docs](https://docs.openclaw.com/plugins)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registers the heygen video-generation provider, requires HEYGEN_API_KEY, and returns guidance for configuring avatar, voice, style, aspect ratio, polling, and webhook options.]

## Skill Version(s):

0.1.2 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

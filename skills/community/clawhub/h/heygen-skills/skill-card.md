## Description:

Create HeyGen avatar videos through the v3 Video Agent pipeline, with avatar resolution, aspect ratio correction, prompt engineering, and voice selection guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eve-builds](https://clawhub.ai/user/eve-builds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill with coding agents to set up HeyGen access, create reusable avatars or digital twins, and generate personalized avatar videos for updates, outreach, announcements, and explainers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad agent-led install instructions can give an agent too much authority over cloning, setup, authentication, and verification.

Mitigation: Review each install command before execution and prefer manual or stepwise installation for production environments.

Risk: API keys may be exposed if stored in global shell profiles, committed project files, or shared agent sessions.

Mitigation: Prefer MCP OAuth when possible, keep HEYGEN_API_KEY scoped to the session or a protected secret store, and never commit local environment files.

Risk: One-line remote installers and plugins can introduce supply-chain risk.

Mitigation: Verify the installer and plugin source, pin versions where supported, and review plugin permissions before enabling video generation.

Risk: User photos, identity files, PDFs, and other media may be uploaded to HeyGen during avatar or video creation.

Mitigation: Require explicit approval for each raw file or photo upload and use only assets the user intentionally provides for generation.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/eve-builds/skills/heygen-skills)
- [HeyGen API Quick Start](https://developers.heygen.com/docs/quick-start)
- [HeyGen CLI](https://developers.heygen.com/cli)
- [HeyGen MCP Remote Docs](https://developers.heygen.com/docs/mcp-remote)
- [OpenClaw HeyGen Plugin](https://github.com/heygen-com/openclaw-plugin-heygen)
- [Avatar Discovery](artifact/references/avatar-discovery.md)
- [Prompt Craft](artifact/references/prompt-craft.md)
- [Frame Check](artifact/references/frame-check.md)
- [Asset Routing](artifact/references/asset-routing.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and local state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create AVATAR-<NAME>.md and heygen-video-log.jsonl files and may upload user-approved media to HeyGen through MCP, CLI, or an OpenClaw plugin.]

## Skill Version(s):

2.2.1 (source: server release metadata, SKILL.md frontmatter, changelog released 2026-04-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

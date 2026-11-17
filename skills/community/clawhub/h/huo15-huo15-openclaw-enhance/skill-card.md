## Description:

Huo15 Openclaw Enhance is a third-party OpenClaw plugin that adds agent-harness features such as memory helpers, task and chapter tools, status reporting, model routing, file sharing, upload handoff flows, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this plugin to add non-invasive workflow, memory, diagnostics, routing, and file handoff utilities to OpenClaw agent deployments. The plugin is broad and default-on, so teams should review enabled features before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin is broad and default-on, and server security evidence says it should be trusted with local OpenClaw sessions, memory, logs, and file-sharing paths.

Mitigation: Review configuration before installation and disable transcript bridging, bot share/upload, model routing, context watchdog, LaunchAgent-related, or other features that are not needed.

Risk: File sharing and upload handoff features can expose sensitive local files or directories if used carelessly.

Mitigation: Avoid sharing symlinked files, sensitive directories, credentials, or private data; set narrow share roots and expiration windows, and revoke links when done.

Risk: Generated LaunchAgent commands can create persistent cleanup behavior with a deletion policy.

Mitigation: Inspect the generated commands and uninstall path before running them, and only enable persistence after accepting the cleanup policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-huo15-openclaw-enhance)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)
- [Project homepage](https://cnb.cool/huo15/ai/huo15-openclaw-enhance)
- [npm package](https://www.npmjs.com/package/@huo15/openclaw-enhance)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)
- [Self-iteration SOP](docs/SELF_ITERATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON-like tool results, inline shell commands, local file paths, and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reference local OpenClaw sessions, memory, logs, share paths, upload tokens, and generated setup commands depending on enabled features.]

## Skill Version(s):

6.7.13 (source: server release evidence, SKILL.md frontmatter, package.json, CHANGELOG; CHANGELOG date 2026-05-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

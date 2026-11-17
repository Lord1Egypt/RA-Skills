## Description:

HotTrender Basic Crawler helps agents use a bundled local crawler runtime for four-region daily trend collection and custom keyword hotspot discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[7487](https://clawhub.ai/user/7487)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they need an agent to install, configure, run, or extend a small local HotTrender crawler for jp/us/tw/kr daily trends or custom keyword hotspot reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional TikTok live mode handles TikTok session material and logs part of an acquired msToken.

Mitigation: Avoid optional TikTok mode until token-prefix logging is removed; use a disposable TikTok session token for testing and keep logs private.

Risk: Live crawler mode contacts external platforms and may fail or return incomplete results when providers block or do not support a region.

Mitigation: Run offline mode first for deterministic validation, then keep explicit provider errors in reports instead of replacing failures with fabricated data.

Risk: Runtime dependencies are version-ranged and may change behavior across installs.

Mitigation: Install in an isolated virtual environment or container and prefer pinned or hash-locked dependencies before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/7487/skills/hottrender-dingtalk-bot)
- [Setup And Portability](references/setup.md)
- [Command Reference](references/commands.md)
- [Basic Crawler Capability Map](references/capabilities.md)
- [Extension Policy](references/extension-policy.md)
- [HotTrender Basic Crawler Runtime](assets/hottrender-runtime/README_RUNTIME.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands; the bundled runtime can write Markdown and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live mode contacts external platforms; optional TikTok mode requires extra dependencies and session setup.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

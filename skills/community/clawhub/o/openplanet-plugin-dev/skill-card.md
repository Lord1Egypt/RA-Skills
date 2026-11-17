## Description:

Create, debug, structure, and run Openplanet AngelScript plugins for Trackmania 2020 (TMNEXT) and ManiaPlanet 4 (TM2/MP4).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomekdot](https://clawhub.ai/user/tomekdot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, debug, review, and launch Openplanet AngelScript plugins for Trackmania 2020 and ManiaPlanet 4. It supports API verification, plugin structure decisions, launch and log checks, MP4 compatibility fixes, and performance-aware UI patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes advanced game-modding guidance such as Dev memory writes, hooks, patches, unsigned plugins, registry files, and SmartScreen bypass steps.

Mitigation: Verify sources, prefer read-only checks first, keep backups, and use per-build validation before writing to game memory.

Risk: Process-kill, archive, or log-clearing recipes can interrupt active game or editor work or remove useful diagnostic material.

Mitigation: Save active work and preserve backups or copied logs before following those recipes.

Risk: Build-specific offsets or unsafe memory writes can crash the game or invalidate plugin behavior.

Mitigation: Validate offsets on the current build, start with read-only telemetry, and fall back to read-only behavior when validation fails.

## Reference(s):

- [Openplanet Plugin Dev release page](https://clawhub.ai/tomekdot/skills/openplanet-plugin-dev)
- [Openplanet API documentation](https://openplanet.dev/docs/api)
- [MP4 verified API reference](references/mp4-api-verified.md)
- [MP4 runtime and Dev memory guidance](references/mp4-runtime-and-dev-memory.md)
- [Cross-game TMNEXT and MP4 guidance](references/crossgame-tmnext-mp4.md)
- [Launch and verification workflow](references/launch-and-verify.md)
- [Static verification workflow](references/static-verify-workflow.md)
- [AngelScript API quirks and pitfalls](references/api-quirks-and-pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with AngelScript code examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include static verification steps and risk-aware game-modding guidance.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

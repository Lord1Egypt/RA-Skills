## Description:

Generate, compare, and verify endgame-only Path of Exile 1 builds for a specified patch or league using PoE Ninja evidence and qpooqp777/pob-cli verification when local PoB requirements are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qpooqp777](https://clawhub.ai/user/qpooqp777)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce reproducible endgame-only Path of Exile 1 build analyses from permitted PoE Ninja snapshots, public character data, or complete PoB character codes. It helps compare candidates, preserve imported build data, run PoB verification when local requirements are available, and report assumptions, warnings, and limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags local PoB execution and network/data-source handling as under-scoped for a broadly privileged agent runtime.

Mitigation: Install only in a controlled environment; use a known absolute PoB installation, keep PATH and POB_CLI_ROOT under user control, and review the skill before deployment.

Risk: Untrusted PoE Ninja exports, PoB XML, character codes, and large inputs can affect analysis reliability or execution boundaries.

Mitigation: Prefer local trusted exports and user-approved public inputs, avoid arbitrary large character codes until stricter limits are added, and keep failures blocked or failed instead of converting them into metrics.

Risk: Public character-data sharing can expose build data if code generation is confused with uploading.

Mitigation: Keep private code generation separate from public pobb.in publication and require explicit user confirmation before any public upload.

## Reference(s):

- [API and CLI usage reference](references/api_reference.md)
- [Research notes and verified limitations](references/research_notes.md)
- [Machine-readable character/build template](templates/character_build.json)
- [ClawHub skill page](https://clawhub.ai/qpooqp777/skills/poe1-build-analyst)
- [Content Update 3.29.0 - Path of Exile: Curse of the Allflame](https://www.pathofexile.com/forum/view-thread/3985332)
- [PoE Ninja - Path of Exile 1 Builds](https://poe.ninja/poe1/builds)
- [qpooqp777/pob-cli](https://github.com/qpooqp777/pob-cli)
- [Path of Building Community Fork](https://github.com/PathOfBuildingCommunity/PathOfBuilding)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON reports, PoB character-code status, command examples, candidate tables, metrics, assumptions, and warnings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endgame-only workflow; imported passive tree, gems, links, equipment, jewels, and configuration remain fixed unless the user separately requests research utilities.]

## Skill Version(s):

0.1.2 (source: server release evidence, VERSION, and release notes dated 2026-08-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Render custom Aavegotchi 3D images from arbitrary trait and wearable combinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preview synthetic or hypothetical Aavegotchi appearances from traits, wearable IDs, wearable names, named presets, backgrounds, and render modes. It can produce full-body renders, headshots, and a manifest for outfit or portrait workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct render requests can delete or overwrite arbitrary writable files.

Mitigation: Install and run the skill in an isolated, low-privilege workspace and prefer the main wrapper until output paths are generated internally or restricted to a dedicated render directory.

Risk: Hosted or Unity runners may receive untrusted request JSON.

Mitigation: Avoid passing untrusted request JSON directly to the runners; validate requests and use the wrapper path for normal operation.

Risk: Unity SDK dependencies may change behavior if not fixed to a reviewed revision.

Mitigation: Pin the Unity SDK dependency to a reviewed immutable revision before broader deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaigotchi/skills/gotchi-3d-custom-render)
- [Aavegotchi](https://www.aavegotchi.com)
- [Architecture](references/architecture.md)
- [Input Schema](references/input-schema.md)
- [Request Schema](references/request-schema.md)
- [Presets And Aliases](references/presets.md)
- [Oracle VM Setup](references/oracle-vm-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces full-body PNG, headshot PNG, and manifest JSON render artifacts.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

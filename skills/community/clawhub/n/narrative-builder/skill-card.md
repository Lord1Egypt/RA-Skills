## Description: <br>
Narrative Builder helps agents turn user-provided or referenced world and character material into structured story outputs, including plot structure, event chains, scenes, themes, dialogue guidance, validation reports, and final narrative packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavegeometry](https://clawhub.ai/user/wavegeometry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and agents use this skill to plan and assemble narratives from direct story prompts or from existing world and character files. It is useful for producing scene-by-scene or chapter-style story drafts with supporting structure, pacing, consistency, and source-tracking notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a broad no-refusal instruction for skill-content modifications. <br>
Mitigation: Remove or ignore that clause before use so the agent can still refuse unsafe, unauthorized, or policy-violating requests. <br>
Risk: The workflow may read story, world, and character files explicitly provided by the user. <br>
Mitigation: Provide only files intended for the narrative task and review generated source notes and downgraded-mode notices before relying on the output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wavegeometry/skills/narrative-builder) <br>
- [Publisher Profile](https://clawhub.ai/user/wavegeometry) <br>
- [Narrative Task Catalog](artifact/references/narrative-catalog.md) <br>
- [Narrative Requirements](artifact/references/narrative-requirements.md) <br>
- [Narrative Exemplars Index](artifact/references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown narrative reports and story packages, with optional structured JSON outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mode detection, plot structure, event chains, scene lists, theme mappings, dialogue and voice guidance, validation reports, metadata, source notes, and downgraded-mode notices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

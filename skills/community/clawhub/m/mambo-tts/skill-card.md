## Description:

Mambo TTS provides quick Chinese text-to-speech presets based on Microsoft Edge TTS, including a lively zh-CN-XiaoyiNeural preset with pitch +8%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate Chinese MP3 speech from text with preconfigured Edge TTS voices for lively, fast-paced, general, or narration-style output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text passed to the skill may be processed by Microsoft Edge TTS.

Mitigation: Avoid sending secrets, private personal data, or regulated content unless that processing is acceptable for the deployment.

Risk: The artifact documentation references shell convenience scripts that are not included in this release.

Mitigation: Use the included Node.js scripts or confirm any shell wrappers exist before documenting them as supported entry points.

## Reference(s):

- [Mambo TTS ClawHub Release](https://clawhub.ai/systiger/skills/mambo-tts)
- [Edge TTS Skill](../edge-tts/SKILL.md)
- [node-edge-tts Guide](../edge-tts/references/node_edge_tts_guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [MP3 audio files with command-line invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Microsoft Edge TTS voice, pitch, and rate presets; default output location is the workspace output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

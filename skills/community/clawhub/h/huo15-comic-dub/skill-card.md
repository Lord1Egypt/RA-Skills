## Description:

Reads script.json dialogue, assigns a voice per character, and uses Volcengine Ark Seed-TTS to generate one WAV file per line of dialogue named {sceneId}_{charId}_{idx}.wav.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and production engineers use this skill to turn comic or short-drama dialogue scripts into per-character WAV voice tracks and a manifest for downstream media assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dialogue text is sent to Volcengine Ark for synthesis.

Mitigation: Use the skill only with dialogue that is approved for that external service and configure ARK_API_KEY in a controlled environment.

Risk: The skill creates local output and sidecar files in the selected project directory.

Mitigation: Run it with trusted script.json inputs and keep output directories isolated from sensitive or unrelated files.

Risk: Bundled shared helpers include additional image, video, and download API capabilities beyond the main dubbing path.

Mitigation: Avoid invoking those helper capabilities unless they have been separately reviewed and constrained for the deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-comic-dub)
- [Volcengine TTS Documentation](https://www.volcengine.com/docs/6561/97465)
- [Volcengine Seedance Documentation](https://www.volcengine.com/docs/82379/1520757)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, audio files, JSON]

**Output Format:** [Markdown instructions with CLI examples; runtime output is WAV files plus manifest.json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY and writes local audio, manifest, checkpoint, and cost sidecar files under the selected project output path.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

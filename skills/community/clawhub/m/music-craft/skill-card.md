## Description: <br>
Generate music through a disciplined OpenClaw-native workflow for songs, instrumentals, and lyrics-driven tracks with structured prompts, quality checks, and backend-aware routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luischarro](https://clawhub.ai/user/luischarro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn music requests, lyrics, poems, or briefs into structured generation prompts, select an appropriate local or cloud backend, run the generation workflow, and verify delivered audio quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud music backends may receive prompts, lyrics, reference URLs, and generation instructions. <br>
Mitigation: Use cloud backends only when the user is comfortable sending that material, and avoid private lyrics or proprietary content unless the user explicitly intends that upload. <br>
Risk: Local backends may download large models and write generated audio, cache, or temporary files. <br>
Mitigation: Ask for explicit approval before installs, model downloads, uploads, or overwriting user-visible outputs. <br>
Risk: Generated audio can miss duration, lyrics alignment, loudness, or completeness targets. <br>
Mitigation: Verify duration, loudness, file size, audible completeness, lyrics alignment, and structure before delivery, then revise the prompt rather than retrying the same failing payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luischarro/music-craft) <br>
- [Publisher profile](https://clawhub.ai/user/luischarro) <br>
- [Homepage from skill metadata](https://github.com/LuisCharro/skills/tree/main/publish/music-craft) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [references/changelog.md](references/changelog.md) <br>
- [references/setup-and-preflight.md](references/setup-and-preflight.md) <br>
- [references/acestep-generation.md](references/acestep-generation.md) <br>
- [references/other-backends.md](references/other-backends.md) <br>
- [references/examples.md](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with prompts, checklists, shell commands, and file-delivery notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or route generation of local audio files through approved local or cloud backends.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter, release evidence, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

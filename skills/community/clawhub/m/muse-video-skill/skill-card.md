## Description: <br>
Helps agents plan video projects by producing creative packages with scripts, storyboards, art direction, prompts, and exportable planning assets, without performing final video rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luojiangyong](https://clawhub.ai/user/luojiangyong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, filmmakers, and developers use this skill to turn a video idea into a pre-production package with narrative structure, shot planning, art direction, sound direction, storyboard prompts, and export formats for downstream production tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may steer an agent toward image-generation tools and downstream production configurations even though its stated scope is planning. <br>
Mitigation: Keep generation tools disabled unless explicitly needed, and review generated ComfyUI, HyperFrames, Kling, and Runway payloads before use. <br>
Risk: Generated production configs or repository changes may have effects beyond pre-production planning. <br>
Mitigation: Require separate explicit approval before allowing repository writes, git push, or execution of downstream production configurations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luojiangyong/muse-video-skill) <br>
- [Case library index](references/cases/INDEX.md) <br>
- [Default production pipeline](references/pipelines/default.md) <br>
- [Fast-track production pipeline](references/pipelines/fast-track.md) <br>
- [Downstream tool matrix](references/media/tool-matrix.md) <br>
- [Image generation guide](references/media/image-gen-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration, HTML or Excel export files, and shell commands for local export scripts when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Creative Package JSON, storyboard tables, image prompts, and downstream ComfyUI, HyperFrames, Kling, or Runway configuration drafts.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

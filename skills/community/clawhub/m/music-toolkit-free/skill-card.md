## Description: <br>
Music Toolkit Free helps agents generate MIDI ideas, process audio files, recommend chord progressions, and provide basic music theory guidance for personal music creation and learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Music hobbyists, learners, independent developers, and video creators use this skill to prototype melodies, chord progressions, rhythm ideas, and basic audio edits through an agent-assisted local workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run local commands and write MIDI, audio, and configuration files. <br>
Mitigation: Use a dedicated project or output folder, review generated filenames and paths before execution, and scan resulting files before sharing them. <br>
Risk: The artifact says audio processing is local, but prompts may still be processed by the agent's configured LLM service. <br>
Mitigation: Avoid including sensitive unreleased lyrics, stems, client work, or private project details in prompts unless the configured agent service is approved for that data. <br>
Risk: The free-edition artifact describes personal-use limits and excludes copyrighted media processing and commercial authorization. <br>
Mitigation: Confirm license terms and rights before processing protected media or using generated assets in commercial projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/music-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown with Python, bash, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local MIDI, audio, and configuration files when the agent executes the provided examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

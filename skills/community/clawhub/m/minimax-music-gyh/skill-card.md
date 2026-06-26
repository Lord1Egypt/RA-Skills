## Description: <br>
A MiniMax music-generation skill that uses text prompts, optional lyrics, and a MiniMax API key to create music with Music-2.5, Music-2.5+, or Music-02 models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skydream9527-ctrl](https://clawhub.ai/user/skydream9527-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to generate music from natural-language prompts and optional lyrics through the MiniMax API, saving the resulting audio file locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music prompts, optional lyrics, and request metadata are sent to MiniMax. <br>
Mitigation: Avoid sensitive or confidential prompt text and use a dedicated MiniMax API key where possible. <br>
Risk: The skill writes the generated audio to a caller-selected local path. <br>
Mitigation: Choose an output path that is safe to create or overwrite before running the command. <br>
Risk: The helper script depends on the Python requests package. <br>
Mitigation: Install requests from a trusted Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skydream9527-ctrl/minimax-music-gyh) <br>
- [MiniMax API host](https://api.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, Configuration instructions] <br>
**Output Format:** [CLI command output with a generated audio file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, the requests package, and MINIMAX_API_KEY; saves audio to the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

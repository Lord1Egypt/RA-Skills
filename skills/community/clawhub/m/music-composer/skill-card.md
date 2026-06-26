## Description: <br>
Music Composer helps agents plan MiniMax mmx-cli music generation prompts and commands for instrumental tracks, lyric songs, and cover-style music from user requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuhouxinliang](https://clawhub.ai/user/yuhouxinliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn music ideas into structured genre, tempo, arrangement, vocal, lyric, and mmx command guidance for generated music assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lyrics or source audio selected by the user may be sent to the external MiniMax mmx service. <br>
Mitigation: Only provide lyrics or audio files that are appropriate to send to MiniMax, and confirm service use before generation. <br>
Risk: Running an untrusted or unexpected mmx binary could execute the wrong music-generation tool. <br>
Mitigation: Install mmx only from a trusted source and run the documented existence and version checks before any generation command. <br>
Risk: Generation commands may consume account quota and write output files. <br>
Mitigation: Confirm quota, output filename, and destination before running generation commands. <br>


## Reference(s): <br>
- [Music Genre & Production Parameters Reference](references/music-genres.md) <br>
- [Lyrics Structure Templates](references/lyrics-structures.md) <br>
- [MiniMax](https://www.minimax.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and structured prompt guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mmx command examples, output filename guidance, lyrics structures, and music-generation prompt parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

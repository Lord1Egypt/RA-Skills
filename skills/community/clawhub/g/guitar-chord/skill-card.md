## Description: <br>
Guitar Chord is a guitar chord toolkit for chord identification, chord diagrams, inversions, drop2 voicings, scale lookup, and capo transposition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeAntiWang](https://clawhub.ai/user/DeAntiWang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Musicians, guitar students, and developers can use this skill to answer practical guitar theory questions, including chord note lookup, reverse chord identification, voicing exploration, scale lookup, and capo transposition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The diagram feature can run an undeclared Cargo project from ~/workspace/ascii_chord. <br>
Mitigation: Use ordinary chord, scale, inversion, and drop2 features without diagram mode unless the Cargo dependency is documented, pinned, bundled, or replaced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DeAntiWang/guitar-chord) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style text with command examples and optional ASCII chord or scale diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Diagram mode may depend on a local Cargo project at ~/workspace/ascii_chord; ordinary chord, scale, inversion, and drop2 results are local text outputs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

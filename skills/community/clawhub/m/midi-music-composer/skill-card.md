## Description: <br>
Use when the user asks to write, compose, make, or generate a song as an actual MIDI/instrumental artifact rather than lyrics or a Suno prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lostviolinist](https://clawhub.ai/user/lostviolinist) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate short original instrumental MIDI compositions, manifests, composition plans, and optional audition sets from titles or music prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local MIDI and JSON artifacts that may need review before use in a project. <br>
Mitigation: Review generated song files, manifests, and critic output before publishing or relying on the composition. <br>
Risk: Feedback notes and ratings can be saved locally for future personalization. <br>
Mitigation: Avoid entering sensitive information in feedback, and delete ~/.hermes/music-composer-preferences.json to reset saved preferences. <br>


## Reference(s): <br>
- [Music Composer Skill Homepage](https://github.com/lostviolinist/music-composer-skill) <br>
- [Composer Protocol](references/composer-protocol.md) <br>
- [Song Recipes](references/song-recipes.json) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown response with generated MIDI, JSON manifest, and composition-plan file paths plus optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .mid files, manifest JSON, composition JSON, optional rendered audio, audition records, and local preference memory.] <br>

## Skill Version(s): <br>
1.7.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

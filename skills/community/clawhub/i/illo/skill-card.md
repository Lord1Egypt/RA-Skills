## Description: <br>
Illo creates original editorial illustrations, mini-comics, explainer diagrams, and transparent mascot cutouts from a concept, article, or URL using bundled character, palette, and visual-style guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, writers, and content teams use Illo to turn concepts or articles into original mascot-led editorial images, mini-comics, explainer diagrams, or transparent cutouts for posts, blogs, decks, and social channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image generation can consume the user's Codex CLI quota or OpenRouter account balance. <br>
Mitigation: Confirm the selected backend and model before generation, and make cost or quota implications clear when choosing OpenRouter or generating multiple images. <br>
Risk: Reusable character packs saved under ~/.config/illo can influence future outputs. <br>
Mitigation: Review community packs before installing them and use update/install options that preserve local edits when needed. <br>
Risk: Generated image paths may overwrite existing files if chosen carelessly. <br>
Mitigation: Choose explicit output paths that are safe to overwrite or use distinct filenames for each run. <br>


## Reference(s): <br>
- [Illo homepage](https://illo-skill.com) <br>
- [README](README.md) <br>
- [Backend guide](references/backends.md) <br>
- [Composition guide](references/composition.md) <br>
- [Character builder](references/character-builder.md) <br>
- [Cutout guide](references/cutout.md) <br>
- [Model guide](references/models.md) <br>
- [Quality bar](references/quality-bar.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create reusable character packs under ~/.config/illo and generated image assets at user-selected output paths.] <br>

## Skill Version(s): <br>
0.28.1 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

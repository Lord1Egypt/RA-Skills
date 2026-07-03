## Description: <br>
Turns concepts, articles, and posts into original editorial illustrations, explainer diagrams, mini-comics, or transparent mascot cutouts using a recurring character and bundled visual styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, creators, and developers use Illo to plan and generate article art, social images, brand-matched mascot illustrations, explainer diagrams, and character cutouts through an agent-driven workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call OpenRouter or the user's logged-in Codex CLI to generate images. <br>
Mitigation: Run the documented doctor and backend setup flow, and confirm expected backend, quota, and cost behavior before generation. <br>
Risk: Illo stores user-scoped settings under ~/.config/illo, including an OpenRouter key when that backend is used. <br>
Mitigation: Enter API keys only through the documented local init flow and avoid pasting secrets into chat, command-line flags, or shared files. <br>
Risk: Community character packs are installed from a GitHub-based catalog into user-scoped configuration directories. <br>
Mitigation: Review pack sources before installing or updating them, and use trusted pack repositories for shared or company use. <br>


## Reference(s): <br>
- [Illo homepage](https://illo-skill.com) <br>
- [ClawHub skill listing](https://clawhub.ai/tmchow/skills/illo) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Backends - dual image engine](references/backends.md) <br>
- [Composition](references/composition.md) <br>
- [Character builder](references/character-builder.md) <br>
- [Character cutout register](references/cutout.md) <br>
- [Community character packs](references/pack-sharing.md) <br>
- [Models - friendly names, ids, traits](references/models.md) <br>
- [Prompt recipe](references/prompt-recipe.md) <br>
- [Quality bar](references/quality-bar.md) <br>
- [Visual style](references/visual-style.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, local configuration instructions, generated image files, JSON line records, and optional HTML galleries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Image generation uses either the user's Codex CLI session or an OpenRouter API key stored in the local Illo config; character packs and palettes are user-scoped.] <br>

## Skill Version(s): <br>
0.28.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Use when the user wants to generate or edit images with Google's Nanobanana/Gemini image models using the official Gemini API shape, or when they need publication-style scientific figures rendered exactly from data with the bundled Python plotting tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Grenzlinie](https://clawhub.ai/user/Grenzlinie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical authors use this skill to create materials-science schematics, graphical abstracts, device architecture figures, and publication-style plots. It supports prompt-built Gemini-compatible image workflows and deterministic local plotting from numeric data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image generation mode sends prompts, API credentials, and selected input images to the configured Gemini-compatible endpoint. <br>
Mitigation: Prefer the official Google endpoint, use an API key file where possible, and enable third-party endpoints only after explicitly trusting the provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Grenzlinie/materials-science-figure-skill) <br>
- [Project homepage](https://github.com/siyuliu/materials-science-figure-skill) <br>
- [API Reference](references/api-reference.md) <br>
- [Materials Science Figure Template](references/materials-science-figure-template.md) <br>
- [Publication Plot API](references/publication-plot-api.md) <br>
- [Natural Language Plot Workflow](references/natural-language-plot-workflow.md) <br>
- [Publication Figure Design](references/publication-figure-design.md) <br>
- [Publication Chart Patterns](references/publication-chart-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON plotting specifications, and generated figure files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Image mode may produce generated or edited image files through a Gemini-compatible endpoint; plot mode can produce exact PNG, PDF, or SVG figures from numeric data.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

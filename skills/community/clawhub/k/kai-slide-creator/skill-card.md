## Description: <br>
Generates zero-dependency HTML presentations with 22 style presets, playback, presenter mode, and inline editing for pitches, launches, technical talks, and proposal decks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and presentation authors use this skill to turn prompts, source content, or structured briefs into browser-native HTML slide decks with selected visual presets and validation gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated decks are active HTML and may load remote fonts or run browser-side presentation and editing scripts. <br>
Mitigation: Review generated HTML before sharing or hosting it, and treat decks as executable web content rather than static documents. <br>
Risk: The inline save workflow may send edited deck content back to the page URL before downloading a copy. <br>
Mitigation: Avoid hosting generated decks on origins that accept unauthenticated PUT or other unintended write methods. <br>
Risk: The release includes an unrelated privileged desktop preload file. <br>
Mitigation: Remove or ignore preload.cjs unless the desktop host behavior is understood and the file is intentionally loaded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaisersong/kai-slide-creator) <br>
- [Publisher profile](https://clawhub.ai/user/kaisersong) <br>
- [Homepage](https://github.com/kaisersong/slide-creator) <br>
- [Live demo](https://kaisersong.github.io/slide-creator/demos/blue-sky-en.html) <br>
- [Style index](references/style-index.md) <br>
- [Workflow reference](references/workflow.md) <br>
- [HTML template reference](references/html-template.md) <br>
- [Generation brief schema](schemas/generation-brief.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON brief files, HTML deck code, validation commands, and optional evaluation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated decks are browser-native HTML and may include presenter mode, inline editing, speaker notes, style-specific CSS, and validation artifacts.] <br>

## Skill Version(s): <br>
2.27.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

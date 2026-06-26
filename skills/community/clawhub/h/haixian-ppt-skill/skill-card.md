## Description: <br>
Generates single-file horizontal HTML slide decks with WebGL-backed visual systems, structured layouts, image slots, social covers, and validation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haixiandaxia-jpg](https://clawhub.ai/user/haixiandaxia-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, presenters, and content teams use this skill to turn articles, outlines, screenshots, or product material into polished browser-based decks and related cover images. It is best suited for talks, product launches, analysis decks, salons, and visually structured shareable presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains an author-specific local reference path that may not exist or may expose unintended local context if followed blindly. <br>
Mitigation: Ignore the hardcoded local path unless the user explicitly provides that file and asks to use it; rely on bundled templates and references by default. <br>
Risk: Generated decks may load external fonts, icons, animation libraries, or optional map tiles when opened in a browser. <br>
Mitigation: Review generated HTML before sharing, use bundled fallbacks where available, and confirm network-loading behavior is acceptable for the presentation environment. <br>
Risk: Slide generation can create misleading or poorly fitted visual content if source material, audience, image handling, or constraints are underspecified. <br>
Mitigation: Clarify style, audience, source material, image requirements, and hard constraints before generation, then run the included checklist and Swiss validator when applicable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/haixiandaxia-jpg/haixian-ppt-skill) <br>
- [Homepage from release metadata](https://github.com/op7418/guizang-ppt-skill) <br>
- [README.en.md](artifact/README.en.md) <br>
- [README.md](artifact/README.md) <br>
- [Skill workflow](artifact/SKILL.md) <br>
- [Layout references](artifact/references/layouts.md) <br>
- [Swiss layout references](artifact/references/layouts-swiss.md) <br>
- [Quality checklist](artifact/references/checklist.md) <br>
- [Screenshot framing rules](artifact/references/screenshot-framing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically produces or edits single-file HTML decks and associated image assets; generated decks may use bundled assets and browser-loaded resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

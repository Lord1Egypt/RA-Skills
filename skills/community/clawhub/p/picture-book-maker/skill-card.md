## Description: <br>
Creates illustrated picture books through theme planning, story writing, character design, storyboard layout, page image generation, and HTML packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lishuailibertine](https://clawhub.ai/user/lishuailibertine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, parents, writers, and agents use this skill to plan and assemble children's picture books, including story structure, character cards, storyboard prompts, metadata, page assets, and a browsable HTML book. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaging script can fetch arbitrary image URLs from metadata. <br>
Mitigation: Use trusted image sources, prefer local images under the intended pages directory, and avoid untrusted URLs unless network access is explicitly intended. <br>
Risk: The packaging script can read local paths referenced by book metadata. <br>
Mitigation: Run it only on trusted book folders and review metadata.json before packaging. <br>


## Reference(s): <br>
- [Story Creation Template](references/story-template.md) <br>
- [Picture Book Page Design Guide](references/page-guide.md) <br>
- [Packaging Script](scripts/pack-book.py) <br>
- [ClawHub Skill Page](https://clawhub.ai/lishuailibertine/picture-book-maker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON metadata, image assets, and packaged HTML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create ./picture-book-output/<book-name>/ with metadata.json, pages/, and book.html.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

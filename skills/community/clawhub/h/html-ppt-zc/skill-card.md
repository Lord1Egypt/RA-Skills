## Description: <br>
Generates PowerPoint presentations from a title and body text, with optional HTML slide deck export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to turn plain text into simple .pptx presentations or browser-viewable HTML slide decks for personal, internal, or general presentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML may contact third-party font or CDN providers when opened. <br>
Mitigation: Use the skill only when remote asset loading is acceptable, or prefer an offline/local-assets mode when available. <br>
Risk: Choosing an existing output path may overwrite an important presentation or HTML file. <br>
Mitigation: Use a fresh output filename or back up important files before generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/html-ppt-zc) <br>
- [jsDelivr SRI guidance](https://www.jsdelivr.com/using-sri-with-dynamic-files) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Presentation, HTML, Shell commands] <br>
**Output Format:** [.pptx or HTML files generated from command-line arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and python-pptx; jinja2 is documented as optional for HTML export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

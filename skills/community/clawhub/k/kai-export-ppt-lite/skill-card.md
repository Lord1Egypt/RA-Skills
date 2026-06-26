## Description: <br>
Export HTML presentations to editable PPTX slides using pure Python without browser dependencies, ideal for sandbox environments and limited runtimes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert HTML slide decks into editable PowerPoint files when browser-based rendering with Playwright, Chrome, or Node.js is unavailable. It is intended for sandboxed or limited runtimes that can run Python and install or provide the listed Python packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The exporter can install Python packages at runtime. <br>
Mitigation: Preinstall beautifulsoup4, lxml, python-pptx, and Pillow in a controlled environment, or disable automatic installation before use. <br>
Risk: HTML image references can trigger network requests or include local image files in the generated PPTX. <br>
Mitigation: Use trusted HTML inputs and review external or local image references before conversion. <br>
Risk: Bundled demo HTML may include save or presenter-mode JavaScript. <br>
Mitigation: Review demo HTML before hosting it or using it as an editable shared presentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaisersong/kai-export-ppt-lite) <br>
- [README](artifact/README.md) <br>
- [Release notes](artifact/RELEASE.md) <br>
- [Skill entrypoint](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Configuration] <br>
**Output Format:** [Editable PPTX files generated from HTML input, with Markdown usage guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 with beautifulsoup4, lxml, python-pptx, and Pillow; optional width, height, and chrome flags control export behavior.] <br>

## Skill Version(s): <br>
1.6.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

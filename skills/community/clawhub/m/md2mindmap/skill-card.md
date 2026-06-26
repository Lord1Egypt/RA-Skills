## Description: <br>
Md2mindmap converts Markdown documents into interactive mind maps with HTML output and optional PDF export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sukimgit](https://clawhub.ai/user/sukimgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, learners, trainers, and knowledge workers use this skill to turn Markdown notes, course outlines, and project plans into visual mind maps for review, presentation, and sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML loads JavaScript and CSS from unpkg, so viewing or exporting may depend on third-party CDN availability and policy. <br>
Mitigation: Use the skill only where CDN loading is acceptable, or vendor and review the assets locally before using sensitive Markdown. <br>
Risk: PDF export uses Playwright/Chromium and writes local output files. <br>
Mitigation: Run the converter in a controlled workspace and review input and output paths before execution. <br>


## Reference(s): <br>
- [Md2mindmap ClawHub page](https://clawhub.ai/sukimgit/md2mindmap) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Test report](artifact/TEST_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated HTML/PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Markdown input from a file or command-line argument; writes an interactive HTML mind map and can optionally export PDF via Playwright/Chromium.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release, SKILL.md frontmatter, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

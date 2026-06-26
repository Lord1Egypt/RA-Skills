## Description: <br>
Convert a PDF, such as a research paper, technical report, or project document, into a single-page academic or project website with a structured outline JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zai-org](https://clawhub.ai/user/zai-org) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to turn a local PDF or downloaded PDF into a project-style webpage. The workflow extracts page images, plans website sections, crops relevant figures, and saves an outline JSON plus a single-page HTML site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the full PDF contents and converts pages into local images. <br>
Mitigation: Use local PDFs for confidential material and review generated page images, crops, and outline data before sharing them. <br>
Risk: When given a URL, the workflow downloads the PDF with curl. <br>
Mitigation: Avoid untrusted, oversized, or internal-network URLs, and prefer known public PDF sources when remote download is needed. <br>
Risk: The workflow creates output files under the workspace. <br>
Mitigation: Run it in an appropriate workspace and inspect the generated web output directory before publishing or deploying the site. <br>


## Reference(s): <br>
- [OpenClaw homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-pdf-to-web) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JSON schemas, shell commands, Python snippets, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces outline.json, cropped PNG assets, and index.html under a workspace web output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

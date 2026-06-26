## Description: <br>
Use when a task needs a local Markdown file path or pasted Markdown text converted into a faithful mobile-friendly PNG/JPG long image for phone-readable articles, guides, notes, or reports, with HTML kept beside the image for inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LINSUISHENG034](https://clawhub.ai/user/LINSUISHENG034) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and operators use this skill to convert local or pasted Markdown into phone-readable PNG or JPG long images while retaining an HTML sidecar for inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python packages and Playwright Chromium during normal use. <br>
Mitigation: Run it in an isolated virtual environment or container, or preinstall reviewed dependencies before use. <br>
Risk: Markdown text, generated HTML sidecars, and .source.md files may remain on disk. <br>
Mitigation: Avoid sensitive Markdown unless the output directory is controlled, and delete retained source and HTML files after export when needed. <br>
Risk: Remote images in Markdown may fail to load because of broken URLs, network restrictions, or host rate limiting. <br>
Mitigation: Inspect the generated HTML and image output before distribution, and verify external image sources when completeness matters. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/LINSUISHENG034/markdown-mobile-export) <br>
- [Publisher Profile](https://clawhub.ai/user/LINSUISHENG034) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, Code, Configuration] <br>
**Output Format:** [JSON status output plus generated PNG/JPG image and HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a normalized Markdown source file for pasted text, an HTML sidecar, and a full-page mobile long-image capture.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

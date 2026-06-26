## Description: <br>
Deep-read research papers into authoritative, reproducible teaching reports, then turn them into source-grounded multi-image cartoon-comic storyboard workflows with camera/style/logic continuity and final image-PDF assembly guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, educators, and paper-reading agents use this skill to convert user-provided research papers into rigorous deep-reading reports, teaching explanations, staged storyboard prompts, and final 16:9 PDF assembly guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided or unpublished papers may contain confidential content that appears in reports, prompts, handoff bundles, or storyboard planning. <br>
Mitigation: Use a clean project workspace, include only intended paper artifacts, and avoid external image-generation APIs for confidential papers unless the user explicitly approves sending paper-derived content. <br>
Risk: External image-generation tools may receive paper-derived prompts or visual details during storyboard creation. <br>
Mitigation: Keep image generation as a separate user-approved phase and use only the already summarized report content and approved visual plan. <br>
Risk: Zipped handoff bundles or final PDF assembly may accidentally include unintended local files. <br>
Mitigation: Prepare bundles from a clean workspace and verify file lists before packaging or sharing outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/c-narcissus/paper-deepread-comic-studio) <br>
- [Publisher Profile](https://clawhub.ai/user/c-narcissus) <br>
- [README](artifact/README.md) <br>
- [Security and Privacy Notes](artifact/SECURITY_PRIVACY.md) <br>
- [Publishing Page Information](artifact/PUBLISH_PAGE_INFO_CN.md) <br>
- [Workflow: Request Sources](artifact/workflow/01_request_sources.md) <br>
- [Workflow: Staged Cartoon Visual Storyboard](artifact/workflow/08_staged_cartoon_visual_storyboard.md) <br>
- [Workflow: Storyboard PDF Assembly](artifact/workflow/09_storyboard_pdf_assembly.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured prompts, JSON-compatible planning artifacts, Python helper commands, and PDF assembly guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-first workflow separates deep-reading reports from later image generation and final local PDF assembly.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter, _meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

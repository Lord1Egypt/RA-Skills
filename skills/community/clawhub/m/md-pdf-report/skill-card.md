## Description: <br>
Convert Markdown research reports, fact-checks, and scheme proposals into styled PDFs with native CJK font support while keeping Markdown as the single source of truth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn long-form Markdown analysis, research reports, fact-checks, and proposals into styled PDF deliverables while also returning the editable Markdown source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown and PDF reports may contain confidential or regulated content that is then delivered through a chat platform. <br>
Mitigation: Use this skill only when sending both the Markdown and PDF through the active chat platform is acceptable. <br>
Risk: Broad report-generation prompts may trigger file generation when the user did not intend a PDF deliverable. <br>
Mitigation: Use explicit PDF requests when a PDF is required, and avoid invoking the skill for short messages or Markdown-only outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xcjl/md-pdf-report) <br>
- [macOS CJK Fonts Reference](artifact/references/macos-cjk-fonts.md) <br>
- [PDF Engine Comparison](artifact/references/pdf-engine-comparison.md) <br>
- [WeasyPrint Bootstrap Reference](artifact/references/weasyprint-bootstrap.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown source plus generated PDF file, usually delivered as chat attachments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Markdown as the source document and generates a matching styled PDF; may include MEDIA attachment paths for delivery.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Compares revised outline or script PDFs against older DOCX, PDF, TXT, or Markdown baselines and produces a structural-change report plus visible annotated PDF markup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hshgogogo](https://clawhub.ai/user/hshgogogo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and agents use this skill to compare revised story outlines, scripts, treatments, beat sheets, season maps, or character bios against older versions. It focuses review on structural additions and rewrites, then helps produce a report, DOCX, annotated PDF, and normalized manifest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports, extracted text, and annotated PDFs may contain sensitive draft content. <br>
Mitigation: Use the skill in a dedicated project folder, review generated files before sharing, and avoid running it on content that should not be written into comparison outputs. <br>
Risk: The automatic follow-up workflow can create extra comparison files after an agent edits a draft. <br>
Mitigation: Opt out of the auto-follow workflow or avoid it when additional comparison artifacts are not wanted. <br>
Risk: Structural-change judgments can be incomplete or misclassified because the agent decides which edits matter. <br>
Mitigation: Review the markdown report, annotation manifest, and annotated PDF before relying on the comparison. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hshgogogo/outline-revision-annotator) <br>
- [macOS workflow](references/macos.md) <br>
- [Windows workflow](references/windows.md) <br>
- [Manifest schema](references/manifest-schema.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated deliverables include PDF, DOCX, Markdown, and JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent chooses structural changes and annotation text; the bundled script deterministically extracts sources and renders outputs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

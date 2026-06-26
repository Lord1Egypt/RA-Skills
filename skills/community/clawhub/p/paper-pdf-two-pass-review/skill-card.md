## Description: <br>
Analyze uploaded CVPR paper PDFs with a strict two-pass workflow: first extracting verifiable facts with page, section, figure, and table evidence, then producing a grounded Chinese research critique. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GPIOX](https://clawhub.ai/user/GPIOX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, and developers use this skill to review uploaded CVPR-style paper PDFs, extract evidence-tagged facts, and generate technical critique and reproducibility notes grounded only in the paper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded papers may contain unpublished or private research. <br>
Mitigation: Use the skill only with PDFs that are appropriate to share with the agent environment. <br>
Risk: The second pass defaults to Chinese output and may not fit every review workflow. <br>
Mitigation: Confirm the desired output language before relying on the generated critique. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/GPIOX/paper-pdf-two-pass-review) <br>
- [Round 1 Fact Extraction Prompt](artifact/references/round1.md) <br>
- [Round 2 Research Critique Prompt](artifact/references/round2.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown fact sheet followed by a Chinese markdown research critique with evidence tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an uploaded PDF as input; major claims must include evidence tags and missing information must be stated explicitly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

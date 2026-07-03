## Description: <br>
学术论文润色修改全流程SOP，支持从审稿意见解析、论文诊断、可视化批注、分级改写到终审自检的完整论文修订流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, authors, editors, and academic writing assistants use this skill to turn reviewer comments and manuscript diagnostics into revision plans, rewrite guidance, HTML review reports, revised drafts, and final quality check reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local manuscript files and writes derivative report or draft files. <br>
Mitigation: Use it only with manuscripts you are comfortable processing locally, choose a private output folder, and review generated files before sharing them. <br>
Risk: Generated HTML reports may load a remote Chart.js script. <br>
Mitigation: For confidential or unpublished work, remove the remote script or bundle Chart.js locally before opening or distributing the HTML report. <br>
Risk: Some rewrite examples or journal-fit advice may be generic or hard-coded rather than fully manuscript-specific. <br>
Mitigation: Manually verify revision examples, recommendations, and journal-fit checks against the manuscript and target journal requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuwenqi123123/paper-revision-sop) <br>
- [AI writing pattern reference](references/ai-flavor-patterns.md) <br>
- [Final quality checklist](references/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands, JSON diagnostics, HTML reports, and revised document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local manuscript files and write derivative reports or revised drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Converts policy-style documents, notices, contest rules, submission requirements, and bid requirements into actionable checklists and timelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users handling submissions, applications, contests, policy compliance, or bid responses use this skill to turn copied requirements into a checklist, material list, deadline summary, and high-risk omission notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and print the entire system clipboard when invoked. <br>
Mitigation: Use it only after copying the exact document to process; avoid invoking it while secrets or unrelated private content may be on the clipboard. <br>
Risk: Broad activation prompts may trigger clipboard processing without a clear consent step. <br>
Mitigation: Confirm the intended clipboard content before running the clipboard reader, and prefer explicit clipboard-processing requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/policy-to-checklist) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown checklist and timeline; clipboard reader emits plain text between boundary markers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and pbpaste; reads the current system clipboard when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

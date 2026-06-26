## Description: <br>
Read policies, application requirements, and forms, then turn them into a completeness checklist, risk list, and submission plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert policy text, application requirements, forms, deadlines, applicant details, attachments, and blockers into a practical submission checklist and plan. It is intended to surface missing evidence, ambiguous requirements, and readiness risks before a submission is finalized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Policy documents, application requirements, forms, and applicant profiles may contain sensitive personal or business information. <br>
Mitigation: Treat input materials as sensitive and provide only the files or excerpts needed for the checklist task. <br>
Risk: The helper script can write a local checklist file and may overwrite a default output file in the working directory. <br>
Mitigation: Run the helper only on explicitly selected input files and pass an explicit output path instead of relying on the default checklist.md. <br>
Risk: The skill structures requirements and flags readiness issues but does not prove legal, financial, or submission compliance. <br>
Mitigation: Keep assumptions explicit, mark uncertain fields for confirmation, and have responsible reviewers verify requirements before final submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/policy-application-checker) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README](README.md) <br>
- [Example prompt](examples/example-prompt.md) <br>
- [Checklist template](resources/checklist_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown checklists, risk lists, timelines, evidence trackers, and optional local checklist files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local Python helper to write a checklist file from explicitly provided JSON requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG; SKILL.md frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

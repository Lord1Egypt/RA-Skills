## Description: <br>
Reviews GitHub and cnb.cool pull requests across design, implementation, testing, security, and maintainability, then produces a paste-ready Markdown review comment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review pull requests or merge requests and generate structured feedback before a human submits the review. It focuses on code-change assessment, inline review suggestions, and an overall approve/request-changes/block recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nested review may run with broad filesystem and approval-bypass authority by default. <br>
Mitigation: Use the documented --no-yolo or AUTOREVIEW_YOLO=0 option unless broad local authority is intentional. <br>
Risk: Pull request diffs can contain private code, credentials, or sensitive business context. <br>
Mitigation: Avoid fallback reviewers for sensitive diffs and review the generated comments before sharing them outside the repository. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with inline file references and suggested shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces five-dimension scores, inline comment suggestions, a summary recommendation, and paste-ready PR comment text; it should not approve, merge, or comment on a PR unless explicitly instructed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

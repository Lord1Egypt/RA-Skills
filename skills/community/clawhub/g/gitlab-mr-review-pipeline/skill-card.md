## Description: <br>
Automates GitLab Merge Request review by retrieving open MRs, sending diffs through an AI code-review workflow, generating reports, and emailing results to MR authors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[20181112523](https://clawhub.ai/user/20181112523) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitLab merge requests, produce Markdown and PDF review reports, track processed MRs, and notify contributors by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read repository diffs and email AI-generated reports using stored credentials. <br>
Mitigation: Use a dedicated least-privilege GitLab token, verify configured repositories and MRs, inspect reports for sensitive code or secrets, and require manual approval before sending email. <br>
Risk: Configuration stores GitLab and email credentials on disk. <br>
Mitigation: Keep the generated configuration file owner-readable only, avoid committing tokens, and rotate credentials regularly. <br>


## Reference(s): <br>
- [Review Report Template](references/review-report-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/20181112523/gitlab-mr-review-pipeline) <br>
- [Publisher Profile](https://clawhub.ai/user/20181112523) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, PDF report files, JSON records, email notifications, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads GitLab repository diffs and uses configured credentials for GitLab and email workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

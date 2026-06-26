## Description: <br>
自动化管理GitHub仓库、PR、Issue、CI/CD。无需API Key，安装即用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers can use this skill for GitHub repository, pull request, issue, and CI/CD automation workflows. The artifact is sparse, so install and run it only after confirming the intended repository scope and account permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises broad GitHub repository, pull request, issue, and CI/CD automation without explaining scope or user controls. <br>
Mitigation: Use it first in a controlled repository or test account, require human review before changes, and avoid granting access to production repositories until behavior is verified. <br>
Risk: The release is tagged as requiring sensitive credentials while the artifact claims no API key is needed. <br>
Mitigation: Confirm the authentication path and requested GitHub permissions before use; prefer least-privilege tokens or accounts and do not expose credentials in prompts, logs, or generated output. <br>
Risk: The artifact contains no executable code and limited operational detail, so the claimed automation behavior may be incomplete or unclear. <br>
Mitigation: Review the installed skill text and any agent actions step by step before relying on it for repository management. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/github-auto) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yezhaowang888-stack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable files are bundled; behavior is described in Markdown.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

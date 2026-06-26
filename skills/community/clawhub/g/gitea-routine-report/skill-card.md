## Description: <br>
Generates Gitea repository activity reports, asks an agent to summarize progress, and prepares HTML email reports for repository administrators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhcolin0313](https://clawhub.ai/user/zhcolin0313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to collect Gitea commit activity over a selected time window, summarize team progress, identify inactive contributors or vague commits, and send routine progress reports to repository administrators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect broad Gitea repository activity and email reports without a mandatory send confirmation step. <br>
Mitigation: Use a read-only, least-privilege Gitea token, scope runs to intended repositories, preview report content, and confirm recipients before sending. <br>
Risk: HTML email reports can include repository and commit content that may be sensitive or malformed. <br>
Mitigation: Review generated HTML before delivery and add escaping or sanitization for untrusted repository data. <br>
Risk: Runtime setup depends on temporary files and unpinned Python package ranges. <br>
Mitigation: Clean up temporary report files after use and pin dependency versions for controlled deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhcolin0313/gitea-routine-report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, HTML, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text guidance with shell commands, structured JSON report data, and HTML email content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITEA_URL and a Gitea personal access token; may process all visible repositories unless scoped to a repository.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

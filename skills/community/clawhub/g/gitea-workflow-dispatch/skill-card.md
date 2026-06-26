## Description: <br>
Trigger Gitea/Forgejo workflow_dispatch via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Qizhou-Guo](https://clawhub.ai/user/Qizhou-Guo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to trigger a selected Gitea or Forgejo workflow_dispatch action for a repository, with optional ref, workflow inputs, and dry-run checking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger workflows that run code, consume runner resources, use workflow secrets, or deploy changes depending on repository configuration. <br>
Mitigation: Use a dedicated least-privilege Gitea or Forgejo token limited to the intended repositories and actions, and use dryRun when unsure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Qizhou-Guo/gitea-workflow-dispatch) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Qizhou-Guo) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON] <br>
**Output Format:** [JavaScript object containing dispatch status, response, and request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a dry-run request preview without sending the API call.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Trigger workflows, list runs, and get status for Gitea/Forgejo Actions workflows using repository and workflow details through the configured API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Qizhou-Guo](https://clawhub.ai/user/Qizhou-Guo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to trigger Gitea or Forgejo Actions workflows, inspect workflow runs, and check the status of a specific run from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real Gitea or Forgejo automation with an API token, and workflows may deploy code, modify repositories, use secrets, or call external systems. <br>
Mitigation: Install only for intended Gitea or Forgejo instances, use HTTPS, and provide a short-lived least-privilege token limited to the required repositories and workflows. <br>
Risk: A workflow dispatch request can start automation without enough warning or confirmation guidance. <br>
Mitigation: Review each dispatch request, including owner, repository, workflow file, and ref, before allowing the action to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Qizhou-Guo/gitea-actions) <br>
- [Publisher profile](https://clawhub.ai/user/Qizhou-Guo) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JavaScript object or parsed JSON data describing workflow dispatch, workflow runs, or a single run status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITEA_URL and GITEA_TOKEN environment variables and repository owner, repository name, and action-specific workflow or run identifiers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

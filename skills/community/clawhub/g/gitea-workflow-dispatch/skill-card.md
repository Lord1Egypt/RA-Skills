## Description:

Trigger Gitea or Forgejo Actions workflow_dispatch events through the API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhou-guo](https://clawhub.ai/user/qizhou-guo)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to trigger Gitea or Forgejo workflow_dispatch runs for a repository, optionally passing a ref and workflow inputs or using dry-run mode to inspect the request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Gitea API token can be sent to a configured endpoint while triggering remote workflows.

Mitigation: Use a narrowly scoped token, set GITEA_URL to HTTPS, and avoid plaintext HTTP except in isolated local testing.

Risk: The skill can trigger remote automation that may deploy, publish, or access private repositories depending on token permissions.

Mitigation: Review token permissions and target workflow behavior before installing or running the skill in sensitive repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qizhou-guo/skills/gitea-workflow-dispatch)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON object with dispatch status, response, and request details; Markdown guidance may include shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, GITEA_URL, and GITEA_TOKEN; supports owner, repo, workflow, ref, inputs, and dryRun inputs.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

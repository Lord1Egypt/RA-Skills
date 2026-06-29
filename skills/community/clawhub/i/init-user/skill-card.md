## Description: <br>
Initializes paper-kb users by checking Feishu registration, guiding Gitea signup, and creating a private Gitea knowledge-base repository plus a Feishu Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of paper-kb use this skill to onboard Feishu users, bind them to a Gitea account and research direction, create required Gitea state, and set up Feishu Bitable tracking for later ingest and query workflows. <br>

### Deployment Geography for Use: <br>
Global, subject to the operator's Gitea and Feishu deployment. <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a site-admin Gitea token to create private repositories and persist user mappings for supplied Gitea usernames. <br>
Mitigation: Install only against a controlled Gitea instance, verify the configured server addresses, protect and rotate the token, and replace the admin token with the least-privilege account possible. <br>
Risk: A Feishu user can claim a Gitea username without evidence that they control that Gitea account. <br>
Mitigation: Add an account-control proof before binding, such as a one-time code committed to the target Gitea account or confirmed through an authenticated Gitea session. <br>
Risk: The workflow handles Feishu identifiers, table IDs, repository URLs, and sensitive credentials. <br>
Mitigation: Avoid logging Feishu identifiers or credentials unnecessarily, keep environment files out of shared storage, and restrict access to generated user records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/init-user) <br>
- [Configured Gitea registration endpoint](http://43.134.182.170:3000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash-style script invocations and single-line JSON responses from Python scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Feishu user open_id, Gitea server configuration, a Gitea admin token, and optional Feishu Bitable tool access.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

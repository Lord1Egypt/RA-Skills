## Description: <br>
Operates Google Cloud STS through an OOMOL-connected `gcloud_sts` connector to exchange an OOMOL OIDC token for a Google Cloud access token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need an agent to invoke OOMOL's Google Cloud STS connector and retrieve a federated Google Cloud access token for a requested task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector can mint and return Google Cloud access tokens. <br>
Mitigation: Confirm the user's intent before minting a token, minimize token exposure, and avoid placing returned tokens in logs or chat unless necessary for the task. <br>
Risk: The artifact presents the token exchange as an untagged safe/read-like action. <br>
Mitigation: Treat `get_federated_access_token` as credential-sensitive despite the read-like labeling and require explicit user confirmation for token issuance. <br>
Risk: First-time setup may involve remote installer commands for the oo CLI. <br>
Mitigation: Review the installer source before execution and run installation only when the CLI is missing and the user approves setup. <br>


## Reference(s): <br>
- [Google Cloud Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Google Cloud STS on ClawHub](https://clawhub.ai/oomol/oo-gcloud-sts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Google Cloud access tokens that must be treated as secrets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

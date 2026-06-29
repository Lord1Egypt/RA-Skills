## Description: <br>
Manage Gumroad and batch-publish digital products with the official CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and store administrators use this skill to administer Gumroad stores, plan product changes, and batch-publish local digital products through the official Gumroad CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help run commands that read and write local files and perform live Gumroad account actions. <br>
Mitigation: Install only for live Gumroad publishing workflows, verify the target account, files, manifest path, and exact command before account-changing steps, and keep backups of local state files. <br>
Risk: Batch publishing or product mutation can create, publish, replace, or otherwise change products in an external commerce system. <br>
Mitigation: Use dry-run and planning commands first, run one product before continuing a batch, and require explicit confirmation before creation, publication, deletion, file replacement, refunds, license changes, webhook mutation, or other bulk changes. <br>
Risk: The workflow requires Gumroad credentials or an authenticated CLI session. <br>
Mitigation: Keep credentials in the environment or the official CLI login flow, and do not store access tokens, secrets, generated manifests, or account-specific state in the skill package. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline command examples and JSON-oriented CLI outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local batch manifests and verification state when the included helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Deploys a decentralized three-agent CI/CD pipeline where build, test, and deploy stages run on separate Pilot agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to configure three Pilot agents for decentralized build, test, and deploy workflows, including role manifests, peer handshakes, artifact transfer, and deployment receipts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup establishes trust between CI/CD agents and exchanges build artifacts across Pilot peers. <br>
Mitigation: Confirm each peer before handshakes, review dependent Pilot skills, and verify trust state before sending artifacts. <br>
Risk: The deployer role may publish deployment receipts and trigger post-deploy webhooks for production workflows. <br>
Mitigation: Use staging first, least-privilege deployment credentials, validated webhook destinations, manual production approval, and rollback procedures. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Listing](https://clawhub.ai/teoslayer/pilot-ci-cd-pipeline-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash commands and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup steps for a three-agent CI/CD pipeline.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

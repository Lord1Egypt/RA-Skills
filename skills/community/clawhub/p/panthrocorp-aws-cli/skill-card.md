## Description: <br>
AWS CLI v2 for OpenClaw agents, repackaged from the official AWS binary distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panthrocorp](https://clawhub.ai/user/panthrocorp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and invoke AWS CLI v2 inside OpenClaw gateway or container agents for AWS operations such as S3 access and STS identity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may run AWS commands with credentials resolved from the environment or an attached EC2/ECS role. <br>
Mitigation: Install only where AWS access is intended, verify the active identity with `aws sts get-caller-identity`, and use least-privilege IAM permissions. <br>
Risk: Containerized deployments may automatically pick up instance metadata credentials when IMDS is reachable. <br>
Mitigation: Review EC2/ECS credential exposure deliberately and ensure the IMDS hop limit and role attachment match the intended access model. <br>
Risk: The packaging workflow downloads the AWS CLI binary distribution during release packaging. <br>
Mitigation: Prefer pinned releases and verified checksums when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panthrocorp/panthrocorp-aws-cli) <br>
- [Publisher profile](https://clawhub.ai/user/panthrocorp) <br>
- [Project homepage](https://github.com/PanthroCorp-Limited/openclaw-skills) <br>
- [AWS CLI v2 Linux binary distribution](https://awscli.amazonaws.com/awscli-exe-linux-${AWS_ARCH}.zip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, authentication, and AWS CLI command guidance for Linux arm64 and amd64 environments.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata, version.txt, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

AWS CLI v2 for OpenClaw agents, repackaged from the official AWS binary distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panthrocorp](https://clawhub.ai/user/panthrocorp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to make AWS CLI v2 available inside OpenClaw gateway containers for S3, STS, and other AWS command-line workflows. It supports containerized AWS access using configured credentials or the AWS default credential provider chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unverified executable package.

Mitigation: Install only from a trusted, pinned release channel and prefer releases with published checksums or signatures.

Risk: The AWS CLI can automatically use EC2 or ECS metadata credentials inside a container.

Mitigation: Run the skill with a least-privileged AWS identity and confirm the intended credential source before use.

Risk: AWS commands can access or modify cloud resources according to the active credentials.

Mitigation: Review commands before execution and test with restricted IAM permissions for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panthrocorp/skills/panthrocorp-aws-cli)
- [OpenClaw skills repository](https://github.com/PanthroCorp-Limited/openclaw-skills)
- [AWS CLI v2 Linux installer source](https://awscli.amazonaws.com/awscli-exe-linux-${AWS_ARCH}.zip)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command behavior depends on AWS credentials, IAM permissions, network access, and target AWS services.]

## Skill Version(s):

0.2.1 (source: release evidence, CHANGELOG, version.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

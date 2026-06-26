## Description: <br>
Self-contained AWS S3 SDK bundle for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panthrocorp](https://clawhub.ai/user/panthrocorp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to give OpenClaw agents access to the AWS S3 SDK inside gateway containers, including environments where dependencies must already be bundled for offline installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this bundle can receive broad live S3 access from the AWS credentials already available in the gateway container. <br>
Mitigation: Install only with tightly scoped IAM roles or AWS profiles, limited to the required buckets, prefixes, and S3 actions. <br>
Risk: S3 write or delete commands can modify or remove data if exposed to agents without review. <br>
Mitigation: Require explicit user approval before agents run S3 write or delete operations. <br>
Risk: A release tarball could be replaced or corrupted before installation. <br>
Mitigation: Verify the release tarball checksum before installing it into the gateway container. <br>


## Reference(s): <br>
- [ClawHub Aws S3 skill page](https://clawhub.ai/panthrocorp/panthrocorp-aws-s3) <br>
- [OpenClaw skills repository](https://github.com/PanthroCorp-Limited/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for installing and using the bundled @openclaw/aws-s3 package; live S3 behavior depends on the AWS credentials available to the runtime environment.] <br>

## Skill Version(s): <br>
0.2.1 (source: SKILL.md frontmatter, package.json, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

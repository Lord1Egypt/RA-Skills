## Description: <br>
AWS S3 helps an agent operate Amazon S3 through an OOMOL-connected account, including listing buckets and objects, reading metadata, uploading objects, generating pre-signed URLs, and deleting objects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation users use this skill to let an agent inspect and manage AWS S3 resources through their connected OOMOL account. It is suited for bucket and object discovery, object metadata checks, uploads, pre-signed URL workflows, and carefully approved deletion tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a connected AWS S3 account, including write, pre-signed URL, and delete workflows. <br>
Mitigation: Review every write, pre-signed URL, and delete payload before approval, and confirm the target bucket, key, action, and expected effect. <br>
Risk: Deleting an object removes data from the connected AWS S3 account. <br>
Mitigation: Require explicit approval for destructive actions and verify the exact object target before running the command. <br>
Risk: Pre-signed URLs can grant time-limited access to read, upload, or delete an object. <br>
Mitigation: Generate pre-signed URLs only for intended recipients, actions, buckets, and keys, and avoid sharing them beyond the required workflow. <br>
Risk: First-time setup may run an installer for the oo CLI. <br>
Mitigation: Use the fallback install path only when the CLI is missing, and verify the installer from OOMOL's official source before running it. <br>


## Reference(s): <br>
- [AWS S3 homepage](https://aws.amazon.com/s3/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-aws-s3) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include action payloads, connector schema inspection commands, command outputs, setup guidance, or approval prompts for write and destructive actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

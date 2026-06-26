## Description: <br>
Operates Alibaba Cloud OSS through an OOMOL-connected account using the oo CLI to list buckets and objects, fetch metadata, generate pre-signed URLs, upload objects, and delete objects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Alibaba Cloud OSS resources and perform controlled object operations through a connected OOMOL account. It supports object listing, metadata checks, pre-signed URL generation, uploads, and deletions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploads and deletes can change or remove Alibaba Cloud OSS objects. <br>
Mitigation: Confirm the exact bucket, object key, payload, and expected effect before approving upload or delete actions. <br>
Risk: Pre-signed URLs can grant read, upload, or delete access to a specific object. <br>
Mitigation: Generate pre-signed URLs only for the intended object and operation, and review the requested access before sharing or using them. <br>
Risk: The skill depends on the oo CLI and an OOMOL-connected Alibaba Cloud OSS credential. <br>
Mitigation: Install and authenticate the oo CLI only when needed, and use the connected account intended for the target bucket. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-aliyun-oss) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Alibaba Cloud OSS](https://www.alibabacloud.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return structured JSON from oo connector executions when the agent runs Alibaba Cloud OSS actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

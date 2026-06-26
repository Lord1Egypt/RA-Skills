## Description: <br>
Cloudflare R2 (cloudflare.com). Use this skill for ANY Cloudflare R2 request: reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Cloudflare R2 accounts, buckets, bucket details, and bucket-level CORS policies through an OOMOL-connected Cloudflare R2 account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-capable Cloudflare R2 actions can create or modify buckets and CORS policies. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running actions tagged as write. <br>
Risk: Destructive Cloudflare R2 actions can delete buckets or bucket CORS policies. <br>
Mitigation: Confirm the target resource and obtain explicit user approval before running actions tagged as destructive. <br>
Risk: Connector payload assumptions can be wrong if the live Cloudflare R2 action schema changes. <br>
Mitigation: Inspect the live connector schema for the selected action before constructing or running a payload. <br>
Risk: Security confidence is limited by the available scanner evidence. <br>
Mitigation: Review the skill instructions and metadata for requested tools, credentials, network access, file access, and write-capable behavior before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-cloudflare-r2) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Cloudflare R2 homepage](https://www.cloudflare.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing Cloudflare R2 action payloads.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

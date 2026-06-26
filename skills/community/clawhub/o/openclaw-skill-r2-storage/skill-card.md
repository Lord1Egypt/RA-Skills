## Description: <br>
Manage Cloudflare R2 object storage operations, including upload, download, list, delete, and pre-signed URL generation, through a boto3 S3-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrnsmh](https://clawhub.ai/user/mrnsmh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to manage Cloudflare R2 buckets and objects from agent workflows, including file transfer, object listing, deletion, and temporary sharing links. It is intended for environments where users provide credentials they are authorized to use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports hardcoded Cloudflare R2 credentials and a specific account endpoint, which could expose or operate on an account the user does not control. <br>
Mitigation: Remove the embedded credentials and endpoint, rotate exposed keys, and require users to provide authorized R2 credentials through environment variables. <br>
Risk: Delete and pre-signed URL operations can remove objects or share access when run with valid credentials. <br>
Mitigation: Review target bucket and key values before execution, and add explicit confirmation or warnings around deletion and sharing-link commands. <br>


## Reference(s): <br>
- [Cloudflare R2 API Reference](references/r2-api.md) <br>
- [Cloudflare R2 Docs](https://developers.cloudflare.com/r2/) <br>
- [Cloudflare R2 S3 API Compatibility](https://developers.cloudflare.com/r2/api/s3/api/) <br>
- [boto3 S3 Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce R2 operation summaries, object listings, and pre-signed URL text when executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

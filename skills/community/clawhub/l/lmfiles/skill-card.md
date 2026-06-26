## Description: <br>
Upload files to lmfiles.com and return public download links via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[setdemos](https://clawhub.ai/user/setdemos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use LMFiles to register an lmfiles.com account, upload files, retrieve public download links, inspect file metadata, list account files, and delete owned uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files become publicly shareable through returned download links. <br>
Mitigation: Upload only files intended for public sharing and confirm with the user before uploading uncertain content. <br>
Risk: LMFILES_API_KEY and LMFILES_BOOTSTRAP_TOKEN are credentials that could grant account access if exposed. <br>
Mitigation: Keep credentials out of chat logs and shared transcripts, avoid logging them, and rotate the bootstrap token if it is exposed. <br>
Risk: Deleting a file by ID is an owner-only destructive operation. <br>
Mitigation: Verify the target file ID before issuing delete requests. <br>


## Reference(s): <br>
- [LMFiles service documentation](https://lmfiles.com/docs) <br>
- [LMFiles OpenAPI schema](https://lmfiles.com/openapi.json) <br>
- [LMFiles API host](https://lmfiles.com) <br>
- [LMFiles on ClawHub](https://clawhub.ai/setdemos/lmfiles) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads are limited to 100 MB, executable file types are rejected, and returned download URLs are public.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

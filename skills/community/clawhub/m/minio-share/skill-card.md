## Description: <br>
Uploads selected files to a configured MinIO bucket and returns shareable presigned links with optional JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinute](https://clawhub.ai/user/sinute) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to upload user-selected local files to a configured MinIO object storage bucket and return a download link or JSON metadata for sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill uploads selected files to external MinIO object storage and creates shareable links. <br>
Mitigation: Confirm the exact file and intended destination before upload, and use the skill only with a bucket approved for the data being shared. <br>
Risk: MinIO credentials can grant broader storage access than the sharing task requires. <br>
Mitigation: Configure a least-privilege MinIO key scoped to the intended bucket and keep access keys in environment variables or the user's normal secret-management system. <br>
Risk: Uploaded objects may remain in the bucket after a presigned link expires, and disabling TLS verification weakens transport security. <br>
Mitigation: Apply bucket lifecycle or cleanup policies for uploaded objects and avoid the insecure SSL option except in controlled test environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sinute/minio-share) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime script output is a presigned URL or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MinIO endpoint, console URL, access key, secret key, and bucket environment variables. Uploads create objects in the configured bucket and presigned links expire after the selected interval.] <br>

## Skill Version(s): <br>
0.1.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

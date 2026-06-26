## Description: <br>
Upload files to Aliyun OSS or Tencent COS and return public access URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhean2021](https://clawhub.ai/user/liuhean2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload local files or URL-fetched files to Aliyun OSS or Tencent COS and return a public HTTPS link for browser access or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud storage credentials can be mishandled during setup or troubleshooting. <br>
Mitigation: Use a dedicated least-privilege OSS or COS key scoped to one bucket and path, configure it through platform secrets or local setup, and avoid sharing credential values in chat or logs. <br>
Risk: Uploaded local or fetched content may become publicly accessible on the internet. <br>
Mitigation: Upload only content intended for public access, review files before upload, and treat every returned link as public. <br>
Risk: URL uploads can fetch and publish content from sensitive internal or private locations. <br>
Mitigation: Avoid URL uploads for internal or sensitive addresses unless network-scope protections are added and reviewed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown with shell command examples and returned URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads one file under 100 MB, verifies object existence and public link accessibility, and returns a public HTTPS URL only after validation.] <br>

## Skill Version(s): <br>
1.7.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

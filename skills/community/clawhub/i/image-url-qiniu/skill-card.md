## Description: <br>
Download an image from a user-supplied HTTP(S) URL and upload it to Qiniu cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lubin1127](https://clawhub.ai/user/lubin1127) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to mirror a user-provided public image URL into a configured Qiniu bucket and return a stable public media URL for delivery, CDN use, or backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime needs Qiniu upload credentials. <br>
Mitigation: Use a dedicated bucket or restricted key and prefix, and keep credentials out of chat, logs, and user profile data. <br>
Risk: Uploaded objects are served through a public-read bucket or public base URL. <br>
Mitigation: Only mirror images the user is authorized to use and confirm that public-read delivery is intentional for the deployment. <br>
Risk: The optional --no-verify-ssl flag disables TLS certificate verification for downloads. <br>
Mitigation: Avoid --no-verify-ssl except for a clearly understood debugging case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lubin1127/image-url-qiniu) <br>
- [Qiniu homepage](https://www.qiniu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text MEDIA_URL line with optional troubleshooting guidance on failure.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Qiniu credentials and bucket configuration in environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Upload a local image to img.scdn.io and return a permanent public link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nujgnoix](https://clawhub.ai/user/nujgnoix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload a selected local image file to a public image host and get a shareable URL for posts or other public sharing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are uploaded to a third-party public host and may become publicly accessible. <br>
Mitigation: Use only with images intended for public sharing; do not upload private, personal, confidential, or regulated content. <br>
Risk: The response parser embeds server-controlled response text into a Python command string. <br>
Mitigation: Review the script before installation and prefer parsing the response through stdin or a temporary file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nujgnoix/image-upload-imgcdn) <br>
- [Publisher profile](https://clawhub.ai/user/nujgnoix) <br>
- [img.scdn.io upload endpoint](https://img.scdn.io/api/v1.php) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text URL with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads the selected file to a third-party public image host before returning the URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

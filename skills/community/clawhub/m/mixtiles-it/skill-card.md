## Description: <br>
Send a photo or image URL to Mixtiles for ordering wall tiles by uploading it and returning a ready-to-order cart link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SaharCarmel](https://clawhub.ai/user/SaharCarmel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill when they want to turn one or more local photos or image URLs into Mixtiles cart links for customization and ordering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected photos or image URLs are uploaded to Cloudinary and used in a Mixtiles cart link. <br>
Mitigation: Use the skill only with photos the user intends to send to Mixtiles, and confirm the exact file or URL before running it. <br>
Risk: Batch mode can upload multiple selected photos in one run. <br>
Mitigation: Confirm the full batch input list before execution. <br>
Risk: Optional fallback upload settings can send image URLs to a custom endpoint. <br>
Mitigation: Set the fallback upload URL and key only for an endpoint the user trusts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SaharCarmel/mixtiles-it) <br>
- [Publisher profile](https://clawhub.ai/user/SaharCarmel) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text cart URL with brief user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce one cart link containing one or more photos.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
img-upload uploads a local image to img.scdn.io and returns public sharing and deletion links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[big-dust](https://clawhub.ai/user/big-dust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and external users use this skill when a local, generated, or screenshot image needs to become a shareable public URL for documents, messages, web pages, or tickets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images uploaded with this skill become publicly accessible through the returned URL. <br>
Mitigation: Use the skill only for images intended for public sharing; avoid confidential screenshots, documents, IDs, receipts, medical images, and internal tickets. <br>
Risk: The returned delete_url can control deletion of the hosted image. <br>
Mitigation: Treat delete_url as sensitive control information and share it only with users or systems authorized to delete the image. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/big-dust/img-upload) <br>
- [Publisher profile](https://clawhub.ai/user/big-dust) <br>
- [img.scdn.io upload API endpoint](https://img.scdn.io/api/v1.php) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Console text containing public image URL and delete URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces public links; delete_url should be treated as sensitive control information.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Meta Business Suite automates Facebook Page and Instagram publishing, scheduling, analytics, comments, media uploads, and deletions through the Meta Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nachx639](https://clawhub.ai/user/Nachx639) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and social media operators use this skill to generate Meta Graph API commands for publishing, scheduling, reviewing analytics, managing comments, uploading media, and deleting Facebook Page or Instagram content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Meta business account using sensitive Page access tokens. <br>
Mitigation: Use least-privilege tokens, prefer explicit META_PAGE_ACCESS_TOKEN and META_PAGE_ID environment variables, and avoid relying on token cache values unless they have been verified. <br>
Risk: Generated commands can publish, comment, upload, schedule, or delete Facebook and Instagram content. <br>
Mitigation: Require manual approval and verify the target Page, Instagram account, post, media, schedule time, and local file path before running account-changing commands. <br>


## Reference(s): <br>
- [Meta Graph API documentation](https://developers.facebook.com/docs/graph-api) <br>
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/) <br>
- [ClawHub skill page](https://clawhub.ai/Nachx639/meta-business-suite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require Meta Page access credentials and should be reviewed before account-changing actions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

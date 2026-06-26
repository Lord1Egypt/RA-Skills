## Description: <br>
Manages Halo CMS blogs through API workflows for posts, categories, tags, comments, media uploads, and blog statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siyrs](https://clawhub.ai/user/siyrs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External blog operators and developers use this skill to administer a Halo CMS site through authenticated API requests, including creating and editing posts, managing taxonomy, moderating comments, and uploading media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Halo login credentials and session cookies on disk. <br>
Mitigation: Use a Halo account with only the permissions needed, avoid shared machines, and protect or delete ~/halo-manager/config.json and ~/halo-manager/session.json after use. <br>
Risk: The skill can publish, delete, upload, and moderate content on a Halo site. <br>
Mitigation: Manually confirm publish, delete, upload, and comment-moderation actions before execution. <br>


## Reference(s): <br>
- [Halo API Reference](artifact/references/api-reference.md) <br>
- [Halo Manager Examples](artifact/references/examples.md) <br>
- [Halo Blog Manager ClawHub Release](https://clawhub.ai/siyrs/halo-blog-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with API request summaries, JSON payload examples, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration and session files under ~/halo-manager when setup or login workflows are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

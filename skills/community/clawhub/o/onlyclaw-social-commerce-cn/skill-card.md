## Description: <br>
Automates Onlyclaw social commerce workflows for posting product content, reading and searching posts, uploading cover or video media, and liking or commenting on posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azhangwq-bit](https://clawhub.ai/user/azhangwq-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to automate Onlyclaw social commerce operations, including creating posts, finding related resources, uploading media before posting, reading and searching posts, and performing public interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize an agent to post, upload media, like, and comment publicly on Onlyclaw. <br>
Mitigation: Require explicit human approval before public posts, uploads, likes, or comments. <br>
Risk: Uploaded media can produce public URLs and may expose sensitive content. <br>
Mitigation: Avoid sensitive media uploads and review files before upload. <br>
Risk: Broad API credentials can allow unexpected or excessive social-commerce actions. <br>
Mitigation: Use a dedicated least-privilege LSK key, avoid USK unless necessary, monitor activity, and revoke the key if behavior is unexpected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/azhangwq-bit/onlyclaw-social-commerce-cn) <br>
- [Onlyclaw Platform](https://onlyclaw.online) <br>
- [Onlyclaw API Base URL](https://lvtdkzocwjkzllpywdru.supabase.co/functions/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline HTTP and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ONLYCLAW_LSK_API_KEY for primary posting and interaction workflows; ONLYCLAW_USK_API_KEY is optional for supported read or broader account-key operations.] <br>

## Skill Version(s): <br>
1.5.7 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Manages Halo CMS blog posts, categories, tags, and comments through the Halo REST API for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThomasOscar](https://clawhub.ai/user/ThomasOscar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to list, draft, publish, and manage Halo CMS blog content and comment replies from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live changes to Halo CMS posts, tags, and comments. <br>
Mitigation: Require explicit user confirmation before publishing, replying, creating tags, or recycling posts and comments; create drafts by default when publishing is not requested. <br>
Risk: Credentials and configuration may be loaded from environment variables or .env.halo files in parent directories. <br>
Mitigation: Use a least-privilege Halo account and keep .env.halo scoped to the intended workspace. <br>
Risk: A misconfigured HALO_URL can send authenticated requests to the wrong service. <br>
Mitigation: Set HALO_URL only to a trusted Halo instance before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ThomasOscar/openclaw-halo-cms) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and plain-text API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted Halo instance and Halo authentication credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

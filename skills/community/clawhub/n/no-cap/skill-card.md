## Description: <br>
Automatically ingest X/Twitter bookmarks, filter noise, and extract actionable signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zephyr2800](https://clawhub.ai/user/zephyr2800) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use No Cap to process their X/Twitter bookmarks into structured signal notes, action items, project-relevant insights, and optional email digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks the agent to extract and store raw X session cookies locally. <br>
Mitigation: Use a dedicated or lower-risk X account where possible, keep ~/.no-cap/config.json private with owner-only permissions, and rotate cookies if exposed. <br>
Risk: The workflow runs local CLI code from the configured repoPath. <br>
Mitigation: Review the CLI source before setup and run it only from a trusted installation path. <br>
Risk: Optional email digests can send bookmark-derived content through Resend. <br>
Mitigation: Enable email only if digest content can be shared with Resend and keep the Resend API key out of shared chats and logs. <br>


## Reference(s): <br>
- [No Cap on ClawHub](https://clawhub.ai/zephyr2800/no-cap) <br>
- [X](https://x.com) <br>
- [Resend](https://resend.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, HTML email digest content, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local configuration, session summaries, a master signal file, and optional email digest files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

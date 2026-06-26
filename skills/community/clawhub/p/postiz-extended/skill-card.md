## Description: <br>
Schedule and manage social media posts through the Postiz API, including multi-platform scheduling, deduplication, media upload, thread creation, and post state management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolmanns](https://clawhub.ai/user/coolmanns) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, social media managers, and automation-focused users use this skill to create, schedule, validate, query, update, and delete Postiz-managed social posts across connected channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or delete posts on connected social channels. <br>
Mitigation: Review target platform, content, post IDs, and scheduling mode before running commands, and prefer drafts or scheduled posts for first runs. <br>
Risk: Reusable Postiz login cookies may be written to a predictable temporary file. <br>
Mitigation: Protect or remove /tmp/postiz-cookies.txt after use, especially on shared machines. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Postiz credentials and integration IDs in environment variables.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

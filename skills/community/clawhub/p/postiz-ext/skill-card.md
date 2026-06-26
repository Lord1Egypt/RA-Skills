## Description: <br>
Schedule and manage social media posts through the Postiz API, including multi-platform posting, scheduling, media upload, duplicate checks, and thread creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolmanns](https://clawhub.ai/user/coolmanns) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and automation developers use this skill to plan, validate, schedule, publish, update, delete, and de-duplicate social posts across Postiz-connected channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships a fixed Postiz account password that can be used to publish, upload, list, update, and delete posts. <br>
Mitigation: Rotate the exposed password before use, remove hardcoded credentials, and use per-user or environment-provided authentication with the minimum required permissions. <br>
Risk: The helper scripts persist authenticated session cookies on disk. <br>
Mitigation: Store session material securely or avoid persistent cookies; restrict local file permissions and remove session files after use. <br>
Risk: Actions performed through the configured Postiz instance can affect connected social channels. <br>
Mitigation: Use the skill only with Postiz instances and social channels you control, and review scheduled or draft posts before publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/coolmanns/postiz-ext) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads; helper scripts may print plain-text status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create, schedule, list, update, delete, and validate social posts through an authenticated Postiz session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

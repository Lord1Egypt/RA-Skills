## Description: <br>
Job board for agents. Submit jobs, report bad listings. Humans use agents to browse and apply. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuqi-or-yuki](https://clawhub.ai/user/yuqi-or-yuki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents acting for human users use this skill to browse Humaboam jobs, submit real job listings, report bad listings, and check their Humaboam agent profile with a user-provided token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided Humaboam agent token for authenticated requests. <br>
Mitigation: Confirm the agent has permission to use the token, avoid exposing it in logs or unrelated chats, and rotate or revoke it if it is exposed. <br>
Risk: Submitting jobs or reporting listings can change Humaboam content. <br>
Mitigation: Ask for confirmation before submitting jobs or reporting listings, verify job URLs first, and do not submit staffing, fake, or otherwise unsuitable sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuqi-or-yuki/humaboam-final) <br>
- [Humaboam homepage](https://humaboam.fyi) <br>
- [Humaboam skill metadata](https://humaboam.fyi/skill.json) <br>
- [Jobhuntr Agent API documentation](https://humaboam.fyi/doc/jobhuntr-agent-api-documentation) <br>
- [API detail reference](https://humaboam.fyi/doc/api-detail-reference) <br>
- [Authentication, scope, and rate limits](https://humaboam.fyi/doc/authentication-scope-and-rate-limits) <br>
- [Job descriptions agent-token documentation](https://humaboam.fyi/doc/job-descriptions-agent-token-only) <br>
- [Token management documentation](https://humaboam.fyi/doc/token-management-user-jwt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with endpoint tables, bash examples, and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Humaboam agent token for authenticated endpoints.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

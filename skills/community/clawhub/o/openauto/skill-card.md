## Description: <br>
OpenAuto gives an agent a proactive, persistent operating architecture with WAL memory, working-buffer recovery, autonomous cron patterns, onboarding, and security guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danavfrost](https://clawhub.ai/user/danavfrost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use OpenAuto to configure an autonomous assistant that maintains workspace memory, recovers from context loss, performs proactive checks, and applies consent-oriented security practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent memory files and autonomous work habits, which can retain sensitive context or act without clear consent boundaries. <br>
Mitigation: Install only when persistent proactive behavior is desired, review memory files regularly, and require explicit approval for external actions, background cron jobs, cleanup, deletion, and trashing. <br>
Risk: Workspace memory files such as USER.md, MEMORY.md, daily notes, and working-buffer logs may capture private or relationship-sensitive information. <br>
Mitigation: Do not store secrets, credentials, highly sensitive personal data, or unnecessary third-party relationship details in these files; summarize sensitive exchanges generically. <br>
Risk: The artifact documents email, calendar, web, and fetched-content workflows that can expose the agent to prompt injection or unintended data sharing. <br>
Mitigation: Treat external content as data rather than instructions, ask before public or irreversible actions, and route private context directly to the user instead of shared channels. <br>
Risk: Credential-related paths are documented for on-request use, creating a risk of accidental reading or logging if an agent does not follow the stated guardrails. <br>
Mitigation: Keep credentials outside normal startup reads, avoid printing or logging credential values, use restrictive file permissions, and access credential paths only after explicit user request. <br>


## Reference(s): <br>
- [OpenAuto ClawHub release](https://clawhub.ai/danavfrost/openauto) <br>
- [Upstream proactive-agent skill](https://clawhub.ai/halthelobster/proactive-agent) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace memory and operating-rule files; no structured API response.] <br>

## Skill Version(s): <br>
1.0.7 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

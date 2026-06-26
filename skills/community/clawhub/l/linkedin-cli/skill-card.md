## Description: <br>
A bird-like LinkedIn CLI for searching profiles, checking messages, and summarizing your feed using session cookies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arun-8687](https://clawhub.ai/user/arun-8687) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run LinkedIn profile lookup, people search, feed summary, and message-checking workflows from a terminal-backed agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires live LinkedIn session cookie values that can provide account access if exposed. <br>
Mitigation: Treat LINKEDIN_LI_AT and LINKEDIN_JSESSIONID like passwords, avoid storing them in shell history or shared logs, and log out of LinkedIn to invalidate them when they are no longer needed or may have been exposed. <br>
Risk: The skill can display private LinkedIn profile, feed, and conversation data in terminal output. <br>
Mitigation: Run it only on trusted machines and avoid sharing terminal output or logs that may contain personal or account data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arun-8687/linkedin-cli) <br>
- [Skill homepage](https://github.com/clawdbot/linkedin-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the linkedin-api Python package, and LINKEDIN_LI_AT and LINKEDIN_JSESSIONID environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

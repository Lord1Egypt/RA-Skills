## Description: <br>
Use Kagi Search API and FastGPT for web research when you want higher-quality results than Brave or Google, or when Brave Search is rate-limited. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelasper](https://clawhub.ai/user/michaelasper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run Kagi Search queries and FastGPT prompts for web research, ranked result retrieval, and summarized answers with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and FastGPT prompts are sent to Kagi and may include sensitive information if entered by the user. <br>
Mitigation: Avoid putting secrets, personal data, or regulated information in queries or prompts. <br>
Risk: The skill reads a Kagi API token from the environment and API calls may consume account quota. <br>
Mitigation: Provide the token through normal secret-handling practices and expect Kagi API usage to count against available quota. <br>


## Reference(s): <br>
- [Kagi API quick reference](references/kagi-api.md) <br>
- [Kagi API documentation](https://help.kagi.com/kagi/api/) <br>
- [Kagi API token settings](https://kagi.com/settings/api) <br>
- [ClawHub skill page](https://clawhub.ai/michaelasper/kagi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Kagi API token supplied through the environment; API use may consume Kagi quota.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Lynse Cli lets agents call the lynse.ai backend API to inspect account information and manage files, transcripts, summaries, devices, AI models, teams, and messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johneyzhao-lynse](https://clawhub.ai/user/johneyzhao-lynse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Lynse APIs for account lookup, file and transcript workflows, AI model and device administration, team collaboration, and outbound messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a powerful Lynse API key and can perform account-changing actions. <br>
Mitigation: Use a dedicated least-privilege API key and require manual confirmation before deleting resources, changing users, teams, models, or devices, or sending messages. <br>
Risk: The submitted package references install and runtime shell scripts that were not present for review. <br>
Mitigation: Install only after reviewing or obtaining the referenced scripts from a trusted source. <br>
Risk: Misconfigured LYNSE_API_HOST could send credentials or requests to an unintended backend. <br>
Mitigation: Set LYNSE_API_HOST only to the intended Lynse backend and verify it before using LYNSE_API_KEY. <br>
Risk: Token caching may expose access tokens if local permissions are weak. <br>
Mitigation: Store token cache files with owner-only permissions such as mode 600 and protect the host account. <br>


## Reference(s): <br>
- [Lynse homepage](https://www.lynse.ai) <br>
- [ClawHub skill page](https://clawhub.ai/johneyzhao-lynse/lynse-cli) <br>
- [CLI compatibility matrix](artifact/compatibility.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LYNSE_API_HOST and LYNSE_API_KEY; may use local token caching with owner-only file permissions.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata; artifact frontmatter says 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

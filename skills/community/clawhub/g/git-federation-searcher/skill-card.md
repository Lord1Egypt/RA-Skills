## Description: <br>
Search across multiple self-hosted Git instances including Gitea, Forgejo, GitLab, and Codeberg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DJSwiss](https://clawhub.ai/user/DJSwiss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to search repositories across federated and self-hosted Git platforms, aggregate results, and manage configured search instances from a command line or Telegram interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search text can reach a shell command through the web-search fallback. <br>
Mitigation: Review or patch the shell fallback before use in any shared or remotely triggered environment. <br>
Risk: Custom Git instances and API tokens are weakly controlled in this version. <br>
Mitigation: Only add trusted HTTPS Git instances and avoid sensitive API tokens until the skill is reviewed or patched. <br>
Risk: The Telegram bot interface can expose search and instance-management actions to remote users. <br>
Mitigation: Do not expose the bot to untrusted users; restrict access before enabling it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown and terminal text with repository result links, instance status, and configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured Git instance APIs and a SearXNG fallback; results are sorted by repository star count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

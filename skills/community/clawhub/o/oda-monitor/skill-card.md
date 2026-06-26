## Description: <br>
Monitors websites, APIs, servers, and scheduled tasks through Watch.dog, including status checks, uptime history, resource management, and public status page updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robinson0594](https://clawhub.ai/user/Robinson0594) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Watch.dog so they can check monitor and watchdog status, review uptime history, create monitoring resources, pause or resume monitors, delete resources after confirmation, and configure public tracker pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the Watch.dog API key in a local .env file in the skill directory. <br>
Mitigation: Use a revocable, least-privilege API key if available and restrict access to the local skill directory. <br>
Risk: Changing credentials triggers an immediate account monitor listing to test the connection. <br>
Mitigation: Install only when this automatic account query is acceptable for the target Watch.dog account. <br>
Risk: The skill can create, pause, resume, delete, and publish monitoring resources through the Watch.dog API. <br>
Mitigation: Review account-changing actions before approval, and require explicit confirmation before deletion operations. <br>
Risk: A custom WATCHDOG_API_URL could send credentials and tool requests to a non-official server. <br>
Mitigation: Keep the API URL set to the official Watch.dog endpoint unless you intentionally trust another server. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Robinson0594/oda-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/Robinson0594) <br>
- [Watch.dog](https://watch.dog) <br>
- [Watch.dog MCP API endpoint](https://api.watch.dog/api/mcp_server.php) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, tool results, setup instructions, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Watch.dog account data returned by remote API calls; some actions can create, pause, resume, delete, or publish monitoring resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

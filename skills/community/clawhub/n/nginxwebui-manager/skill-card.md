## Description: <br>
Manage NginxWebUI reverse proxy rules via its REST API, including servers, locations, nginx reloads, and upstreams through docker exec into the nginxwebui container. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaixi](https://clawhub.ai/user/zaixi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage a live NginxWebUI instance from an agent workflow, including reverse proxy servers, location rules, upstream listings, nginx validation, and reloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer live NginxWebUI routing, delete rules, and reload nginx. <br>
Mitigation: Use limited credentials and manually verify every delete or reload command before allowing it to run. <br>
Risk: The skill can persist an admin token in a workspace .env file. <br>
Mitigation: Keep the workspace .env file private and out of source control, and rotate or remove stored tokens when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zaixi/nginxwebui-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and operational text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist an NginxWebUI token in a workspace .env file and may change live nginx routing when commands are executed.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

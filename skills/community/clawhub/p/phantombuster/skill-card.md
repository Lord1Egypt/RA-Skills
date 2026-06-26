## Description: <br>
Control PhantomBuster automation agents via API to list agents, launch automations, get output and results, check status, and abort running agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capt-marbles](https://clawhub.ai/user/capt-marbles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and go-to-market teams use this skill to operate their PhantomBuster workspace from an agent, including launching automations, checking runs, and retrieving output or CSV result data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a PhantomBuster workspace, including launching and aborting automation agents. <br>
Mitigation: Keep the PhantomBuster API key in a trusted environment and double-check agent IDs before launch or abort. <br>
Risk: Fetched CSV and output data may contain sensitive scraped, lead, or workspace data. <br>
Mitigation: Treat fetched results as sensitive data and avoid exposing them outside approved workflows. <br>
Risk: An exposed PhantomBuster API key can allow unauthorized workspace actions. <br>
Mitigation: Rotate the API key if it is exposed and avoid committing or sharing it in prompts, logs, or files. <br>


## Reference(s): <br>
- [PhantomBuster](https://phantombuster.com) <br>
- [PhantomBuster Workspace Settings](https://phantombuster.com/workspace-settings) <br>
- [PhantomBuster API v2](https://api.phantombuster.com/api/v2) <br>
- [ClawHub Skill Page](https://clawhub.ai/capt-marbles/phantombuster) <br>
- [Publisher Profile](https://clawhub.ai/user/capt-marbles) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text, JSON, and CSV data fetched from PhantomBuster runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PHANTOMBUSTER_API_KEY and a PhantomBuster agent ID or name for most commands.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

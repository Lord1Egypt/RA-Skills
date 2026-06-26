## Description: <br>
Guided SOP for setting up and using InfoDashboard from OpenClaw to clone the repo, configure database and LLM keys, start the service, and generate a Streamlit dashboard from a natural-language requirement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyxapple98](https://clawhub.ai/user/zyxapple98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up InfoDashboard, configure local provider and database settings, start the service, and generate Streamlit dashboards from natural-language requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup gives the agent access to database credentials, external LLM processing, a private-network tunnel, and generated Docker dashboards. <br>
Mitigation: Install only from a trusted checkout, pin or inspect the repository first, use isolated runtime environments, use read-only least-privilege database credentials, and avoid secrets or PII in prompts. <br>
Risk: The service may expose local dashboard or API endpoints if bound or networked too broadly. <br>
Mitigation: Bind or firewall the service appropriately and stop tunnels and containers when the work is complete. <br>
Risk: Generated dashboard code may be incorrect or unsafe for the target environment. <br>
Mitigation: Review generated code and security scan results before relying on the dashboard output. <br>


## Reference(s): <br>
- [InfoDashboard ClawHub Release](https://clawhub.ai/zyxapple98/infodashboard) <br>
- [Publisher Profile](https://clawhub.ai/user/zyxapple98) <br>
- [Clone Or Reuse Existing Repo](references/clone.md) <br>
- [Configure Environment](references/config.md) <br>
- [Start And Verify](references/startup.md) <br>
- [Generate Flow](references/generate-flow.md) <br>
- [InfoDashboard Repository](https://github.com/AInsteinAsia/InfoDashboard.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, API request details, and dashboard URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns raw dashboard URLs on their own line when generation succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

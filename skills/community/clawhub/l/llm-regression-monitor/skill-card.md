## Description: <br>
Monitors LLM behavior over time by capturing baselines, running behavioral tests, detecting output drift, and sending alerts when regressions are found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swanand33](https://clawhub.ai/user/swanand33) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up scheduled behavioral regression tests for LLM applications, capture expected-output baselines, and receive alerts when prompts or models drift unexpectedly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, prompts, LLM outputs, reports, and alerts may contain sensitive information. <br>
Mitigation: Use least-privilege provider keys, keep .env private and out of version control, avoid unapproved sensitive prompts, and send alerts only to private Slack or WhatsApp destinations. <br>
Risk: Generated baseline, report, and alert log files can expose model behavior or user data if committed. <br>
Mitigation: Add .llm_behave_baselines/, monitor_report.json, and monitor_alerts.log to .gitignore before running the monitoring scripts. <br>
Risk: Monitoring scripts call configured LLM providers and may send prompt content to third-party or custom endpoints. <br>
Mitigation: Confirm the selected provider is approved for the data being tested and prefer a trusted project environment or virtual environment for installation and execution. <br>


## Reference(s): <br>
- [Providers setup guide](references/providers.md) <br>
- [Test suite format](references/test-suite-format.md) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration examples, shell commands, and JSON monitoring reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate baseline files, monitor_report.json, and monitor_alerts.log when its helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

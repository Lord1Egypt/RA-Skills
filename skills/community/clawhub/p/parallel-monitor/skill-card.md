## Description: <br>
Continuously track the web for changes via the Parallel Monitor API. Creates a recurring research task that runs on a cadence and emits events on change, with optional webhook delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[normallygaussian](https://clawhub.ai/user/normallygaussian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create and manage recurring Parallel monitors for web changes such as pricing updates, filings, launches, posts, or other watch-and-alert workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent monitors can continue running on a cadence after creation. <br>
Mitigation: Confirm the objective and cadence before creating a monitor, and keep the monitor_id so recurring jobs can be updated or deleted later. <br>
Risk: Webhook delivery can send monitor events to an external URL. <br>
Mitigation: Use only trusted webhook URLs and confirm whether webhook delivery is needed before enabling it. <br>
Risk: Monitor commands require an installed and authenticated parallel-cli. <br>
Mitigation: Check parallel-cli availability and authentication before running monitor commands; stop on authentication errors. <br>


## Reference(s): <br>
- [Parallel Homepage](https://parallel.ai) <br>
- [Parallel API Docs](https://docs.parallel.ai) <br>
- [Monitor API Reference](https://docs.parallel.ai/api-reference/monitor) <br>
- [Parallel CLI Integration Docs](https://docs.parallel.ai/integrations/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve monitor identifiers and summarize recurring event trends when reporting monitor results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

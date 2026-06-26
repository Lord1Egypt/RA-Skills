## Description: <br>
Monitor website prices, inventory, and content changes using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinanping-CPU](https://clawhub.ai/user/yinanping-CPU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and business analysts use this skill to monitor product prices, stock status, and page content changes across specified websites, then log history and surface alerts for meaningful changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill browses user-provided URLs and may store product lists or monitoring history that reveal personal purchases or business research. <br>
Mitigation: Use trusted browser automation tooling, review product lists before running, and keep generated history files private. <br>
Risk: Optional email or Discord alerting could share monitoring data with third-party services. <br>
Mitigation: Enable external alerts only after confirming the destination and avoiding sensitive products, URLs, or pricing research in alert payloads. <br>
Risk: Frequent automated checks can trigger site blocking or collect stale data when selectors change. <br>
Mitigation: Use conservative check intervals, maintain stable selectors, and re-check pages manually when extraction errors or unexpected prices appear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinanping-CPU/price-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown guidance with bash snippets, Python script usage, CSV configuration, and CSV or JSON monitoring outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included script writes local price-history data and console alerts based on user-provided product URLs, selectors, and threshold settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Query CPU and GPU temperatures on Windows PCs using LibreHardwareMonitor, generate a colored HTML report opened in browser, and output a text summary with timestamp. Use when the user asks about PC temperature, CPU temperature, GPU temperature, hardware temperature monitoring, or thermal status on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waynehrh](https://clawhub.ai/user/waynehrh)

### License/Terms of Use:

MIT-0

## Use Case:

Windows PC users and support technicians use this skill to inspect CPU and GPU temperatures and review timestamped readings in a text summary and color-coded HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The temperature query uses administrator privileges and loads LibreHardwareMonitor from a temporary folder.

Mitigation: Run only after an explicit temperature-check request, and verify the library and its location before loading it as administrator.

Risk: Temporary temperature result and report files are replaced on subsequent runs.

Mitigation: Save any report or readings that need to be retained before running the skill again.

## Reference(s):

- [PC Temperature Monitor on ClawHub](https://clawhub.ai/waynehrh/skills/pc-temp-monitor)
- [LibreHardwareMonitor releases](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML]

**Output Format:** [Timestamped Markdown summary and color-coded HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The HTML report opens in the default browser and replaces the previous temporary report; some status text is in Chinese.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

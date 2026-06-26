## Description: <br>
Opik observability reporter - fetches traces, analyzes usage, costs, and errors, then sends reports to Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate Opik observability summaries for usage, cost, tool-call, and error reporting and deliver those summaries to Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release advertises live Opik reporting, but the security evidence says v1.0.0 appears to generate hard-coded sample metrics. <br>
Mitigation: Review the code before installation and avoid relying on reports until they are based on real telemetry or clearly labeled as synthetic. <br>
Risk: The security evidence identifies an API-key-like value, user-specific paths, and a fixed Discord destination. <br>
Mitigation: Replace the API-key-like value, configure an owned Discord destination, and remove user-specific paths before running the skill. <br>
Risk: Scheduled use could repeatedly send misleading or misdirected reports. <br>
Mitigation: Avoid scheduled execution until the report data source and delivery target have been reviewed and configured for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/opik-reporter) <br>
- [Opik](https://www.comet.com/opik/) <br>
- [Opik API endpoint](https://www.comet.com/opik/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown report text with Discord delivery via OpenClaw command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Discord delivery is truncated to 1900 characters; status is persisted to a JSON file when the script runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

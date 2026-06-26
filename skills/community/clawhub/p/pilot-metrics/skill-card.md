## Description: <br>
Collect and aggregate agent metrics from connections, peers, and custom events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Pilot Protocol agent health, connection state, peers, latency, throughput, and fleet metrics for monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the local pilotctl binary and a running Pilot Protocol daemon. <br>
Mitigation: Install only in environments that already use Pilot Protocol monitoring and trust the pilotctl binary on PATH. <br>
Risk: Exported fleet metrics can include operational details such as hostnames, peer information, latency, and throughput. <br>
Mitigation: Write metrics to private directories or use restrictive file permissions when operational data is sensitive. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-metrics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local pilotctl and jq commands that read operational metrics and can write JSON metrics files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Run speed tests to multiple endpoints, log results, and detect ISP throttling patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network administrators, and internet users use this skill to run repeatable bandwidth tests, keep local speed history, and generate evidence reports for ISP support, throttling complaints, or service-plan decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs active upload and download bandwidth tests that can consume network data and affect current connection performance. <br>
Mitigation: Run tests at an appropriate cadence, keep the configured byte and timeout limits, and avoid testing on metered or sensitive networks unless that traffic is acceptable. <br>
Risk: The skill keeps persistent local speed-test logs and may run recurring background tests if the user configures scheduling. <br>
Mitigation: Store logs in an approved local path, review scheduled jobs before enabling them, and remove the scheduler when ongoing monitoring is no longer needed. <br>
Risk: Custom test endpoints could send traffic to private, workplace, or untrusted hosts. <br>
Mitigation: Use reputable public endpoints for measurement and do not configure private, workplace, or untrusted hosts as speed-test targets. <br>


## Reference(s): <br>
- [Setup Guide](artifact/references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON configuration, JSON analysis output, and markdown evidence reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local JSONL speed logs and optional markdown reports; analysis can also be emitted as machine-readable JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

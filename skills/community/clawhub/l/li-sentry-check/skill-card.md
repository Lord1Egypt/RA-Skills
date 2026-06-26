## Description: <br>
Li Sentry Check inspects remote Linux servers over SSH with key-based authentication, runs predefined read-only health checks, and generates Markdown or JSON reports with anomaly highlighting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and site reliability engineers use this skill to inspect authorized Linux servers, gather system and service health data, and produce structured inspection reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to remote systems over SSH and can expose operational data in reports. <br>
Mitigation: Run it only against systems you are authorized to inspect and handle generated reports as sensitive operational records. <br>
Risk: SSH credentials used for inspection could grant broader access than necessary. <br>
Mitigation: Use a dedicated low-privilege SSH key or account and verify host keys for production systems. <br>
Risk: Changing target or check definitions could introduce commands outside the intended read-only posture. <br>
Mitigation: Review targets.yaml and checks.yaml before running and avoid adding state-changing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-sentry-check) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [checks.yaml](artifact/references/checks.yaml) <br>
- [targets.yaml](artifact/references/targets.yaml) <br>
- [design.md](artifact/design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or JSON reports, with shell commands and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be written to stdout or to a user-specified output file.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Deploys a four-agent PR workflow with reviewer, test-runner, documentation writer, and coordinator roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up coordinated agents that review PRs, run tests, generate documentation, and summarize results. It is intended for multi-agent PR automation rather than one-off review or test runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trusting the wrong peer agent could route PR data or generated results to an unintended host. <br>
Mitigation: Before exchanging handshakes, verify each hostname, deployment prefix, and agent owner. <br>
Risk: Downstream Pilot skills may require GitHub or Slack tokens, PR-comment permissions, file sharing, or network access. <br>
Mitigation: Review the installed downstream skills and grant only the permissions needed for the intended PR workflow. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-dev-team-assistants-setup) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup guidance, hostnames, manifests, handshakes, and sample Pilot commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

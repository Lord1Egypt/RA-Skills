## Description: <br>
Implement MQTT messaging avoiding security, QoS, and connection management pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a concise MQTT implementation reference for secure broker setup, QoS choices, topic design, retained messages, connection handling, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MQTT broker examples may be unsafe if applied without production controls. <br>
Mitigation: Use authentication, TLS, topic ACLs, and careful listener binding before applying broker configuration to real deployments. <br>
Risk: Broad MQTT subscriptions or retained messages can expose data or preserve stale state. <br>
Mitigation: Avoid production use of catch-all subscriptions, restrict topic access, and explicitly clear retained messages when correcting stale data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/mqtt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or data access is indicated by the release security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

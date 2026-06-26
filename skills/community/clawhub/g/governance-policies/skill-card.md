## Description: <br>
AxonFlow plugin setup for OpenClaw: install, connect, and explore starter governance policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axonflow](https://clawhub.ai/user/axonflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and governance or security teams use this skill to install and configure AxonFlow's OpenClaw plugin, review starter governance policies, and connect OpenClaw to AxonFlow for policy enforcement, approvals, PII handling, explainability, and audit history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external AxonFlow plugin and service may process agent events, prompts, PII, approvals, and audit history. <br>
Mitigation: Review the @axonflow/openclaw plugin and AxonFlow service before installation, and keep client credentials in a secret manager rather than source control. <br>
Risk: The setup requires OpenClaw 2026.5.22+ and @axonflow/openclaw 2.6.4+. <br>
Mitigation: Verify OpenClaw and plugin versions before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/axonflow/governance-policies) <br>
- [Artifact homepage](https://github.com/getaxonflow/axonflow-openclaw-plugin/tree/main/policies) <br>
- [AxonFlow docs](https://docs.getaxonflow.com/) <br>
- [OpenClaw plugin reference](https://docs.getaxonflow.com/docs/integration/openclaw/) <br>
- [Policy overview](https://docs.getaxonflow.com/docs/policies/overview/) <br>
- [Self-hosted deployment](https://docs.getaxonflow.com/docs/deployment/self-hosted/) <br>
- [Plugin GitHub](https://github.com/getaxonflow/axonflow-openclaw-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw 2026.5.22+ and @axonflow/openclaw 2.6.4+ requirements.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

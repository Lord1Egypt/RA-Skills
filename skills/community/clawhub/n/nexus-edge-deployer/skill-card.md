## Description: <br>
Deploy 1-bit quantized AI models on VPS for Agent-as-a-Service with 98% margins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuwanito](https://clawhub.ai/user/shuwanito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure teams use this skill to plan edge deployments for 1-bit quantized model serving on low-cost VPS fleets, including provisioning, serving configuration, monitoring, scaling, and unit-economics reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide creation or scaling of billable cloud infrastructure without enough cost limits or cleanup guidance. <br>
Mitigation: Use a dedicated low-privilege Hetzner project, require confirmation before provisioning or scaling, set budget and instance limits, and define teardown steps before execution. <br>
Risk: Endpoint security and GDPR/HIPAA or local-only claims may be over-trusted for sensitive deployments. <br>
Mitigation: Verify inference endpoint authentication and complete a separate compliance review before relying on the skill for regulated data or privacy-sensitive workloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuwanito/nexus-edge-deployer) <br>
- [Metadata homepage](https://github.com/Shuwanito/SkillsMP/tree/main/.claude/skills/nexus-edge-deployer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown deployment guidance with configuration and command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provisioning and scaling guidance for billable VPS infrastructure.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

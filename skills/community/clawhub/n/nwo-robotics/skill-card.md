## Description:

Control robots and IoT devices through natural language using the NWO Robotics API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redciprianpater](https://clawhub.ai/user/redciprianpater)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send natural-language commands to connected robots, query IoT sensors, run vision tasks, and submit task-planning requests through the NWO Robotics API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Natural-language commands may trigger broad robot or IoT actions with physical impact.

Mitigation: Use only in controlled environments with authorized accounts, command scoping, human confirmation, and physical safety interlocks.

Risk: API credentials grant access to robot and IoT operations.

Mitigation: Use restricted API keys, rotate credentials, and avoid sharing accounts across deployments.

Risk: A changed or misconfigured NWO_API_URL could route commands to an unintended service.

Mitigation: Pin NWO_API_URL to the intended HTTPS endpoint and review configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redciprianpater/skills/nwo-robotics)
- [NWO Robotics homepage](https://nworobotics.cloud)
- [NWO Robotics API credentials and docs](https://nwo.capital/webapp/api-key.php)
- [NWO Robotics API demo repository](https://huggingface.co/spaces/PUBLICAE/nwo-robotics-api-demo)
- [OpenClaw Skills Guide](https://docs.openclaw.ai/skills)

## Skill Output:

**Output Type(s):** [text, API calls, shell commands, configuration]

**Output Format:** [Plain text or Markdown responses with environment-variable configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided NWO_API_KEY and NWO_USER_ID, with optional NWO_API_URL.]

## Skill Version(s):

1.0.2 (source: skill.yaml, CHANGELOG, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

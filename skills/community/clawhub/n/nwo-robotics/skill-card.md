## Description: <br>
Control robots and IoT devices via natural language using the NWO Robotics API for robot commands, sensor queries, vision tasks, and task planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RedCiprianPater](https://clawhub.ai/user/RedCiprianPater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics operators use this skill to let OpenClaw agents query connected robots and sensors, run vision tasks, and submit natural-language robotics commands through the NWO Robotics API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send broad real-world robot, IoT, movement, patrol, emergency stop, manipulation, and task execution commands through an API key. <br>
Mitigation: Use only authorized NWO Robotics accounts with scoped or test credentials, and require separate human approval and safety controls before any physical action is executed. <br>
Risk: Robot commands, identifiers, and sensor queries are sent to the configured NWO_API_URL endpoint. <br>
Mitigation: Keep NWO_API_URL pointed at a trusted endpoint and avoid sending sensitive location, device, or operational details unless the deployment is approved for that data flow. <br>
Risk: The server security verdict is suspicious because the skill can issue physical-world action commands without clearly documented limits or confirmation steps. <br>
Mitigation: Review before installing, monitor usage, and deploy only in environments where external safety controls can constrain robot motion and task execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RedCiprianPater/nwo-robotics) <br>
- [NWO Robotics homepage](https://nworobotics.cloud) <br>
- [NWO Robotics API credentials and docs](https://nwo.capital/webapp/api-key.php) <br>
- [NWO Robotics API demo repository](https://huggingface.co/spaces/PUBLICAE/nwo-robotics-api-demo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls] <br>
**Output Format:** [Plain text status messages and command results, with authenticated JSON POST requests to NWO Robotics API endpoints.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NWO_API_KEY and NWO_USER_ID; NWO_API_URL is optional and controls the API endpoint used for robot, sensor, vision, safety, and task requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version, skill.yaml, changelog released 2025-03-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

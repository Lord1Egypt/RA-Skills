## Description: <br>
Connect to NIU smart electric vehicles to retrieve real-time status - battery level, charging status, remaining charge time, location, and total mileage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qdsang](https://clawhub.ai/user/qdsang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query NIU smart electric vehicle status, including battery level, charging state, remaining charge time, location, and total mileage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a NIU API key to retrieve live scooter status, including location. <br>
Mitigation: Use a revocable API key, keep the key private, and limit access to agents and users trusted to view vehicle location. <br>
Risk: Setup may rely on jq for config-file key resolution even though only curl is declared. <br>
Mitigation: Ensure jq is installed when using the documented config-file command, or provide NIU_API_KEY directly as an environment variable. <br>


## Reference(s): <br>
- [NIU](https://www.niu.com/) <br>
- [NIU Scooter Status API endpoint](https://ai-mcp.niu.com/claw/scooter_info?key=$NIU_API_KEY) <br>
- [ClawHub skill page](https://clawhub.ai/qdsang/niu-vehicle) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and NIU_API_KEY; setup instructions also reference jq for config-file key resolution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

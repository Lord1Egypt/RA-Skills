## Description: <br>
Manages and validates a local HIPC API key so HIPC business skills can check whether a usable credential is configured before making requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[377739442](https://clawhub.ai/user/377739442) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents that rely on HIPC business skills use this skill to check whether a HIPC secret is configured, save a provided secret after format validation, and select prod or dev host settings before later HIPC operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The HIPC API key is saved in plaintext at ~/hipc_config.json. <br>
Mitigation: Use this skill only on trusted machines, restrict file access, avoid synced or shared home directories, and rotate the key if the file may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/377739442/hipc-config-manager) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Configuration, Shell commands, Guidance] <br>
**Output Format:** [JSON status responses and Markdown guidance with an inline shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes ~/hipc_config.json; set mode validates secrets before saving.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

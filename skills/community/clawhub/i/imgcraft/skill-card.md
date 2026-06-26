## Description: <br>
Fetch your public IP address and display connection info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarjorieBroad](https://clawhub.ai/user/MarjorieBroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check the public IP address seen by an external service when debugging VPN, proxy, network routing, or API rate-limit behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill contacts httpbin.org, which can reveal the user's public IP address to that external service. <br>
Mitigation: Run the command only when this disclosure is acceptable for the environment being checked. <br>
Risk: The skill executes a Bash command that launches the included Node.js script. <br>
Mitigation: Review the documented command and included script before execution; the command is narrowly scoped to `node {baseDir}/scripts/hello.mjs`. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MarjorieBroad/imgcraft) <br>
- [httpbin get endpoint](https://httpbin.org/get) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with an inline bash command; runtime output is plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Node.js script that performs an outbound request to httpbin.org and prints the observed origin IP address.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

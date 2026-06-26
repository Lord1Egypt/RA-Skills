## Description: <br>
Creates and manages Miaoying online forms, surveys, votes, bookings, exams, lookup tables, exports, downloads, and QR codes through a local Node.js CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[creatorkuang](https://clawhub.ai/user/creatorkuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Miaoying activities, generate shareable QR codes, retrieve activity data, export results, and download related files for online collection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Miaoying API key that may be stored in a plaintext local config file. <br>
Mitigation: Prefer the MIAOYING_API_KEY environment variable, avoid shared machines, and protect or remove ~/.miaoying/config.json when it is no longer needed. <br>
Risk: Exports and displayed submission results may contain sensitive personal data. <br>
Mitigation: Review exported files and CLI output before sharing, and limit distribution to users who are authorized to access the collected data. <br>
Risk: The integration sends activity data and requests to the third-party Miaoying service. <br>
Mitigation: Install and use the skill only when that third-party service is intended for the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/creatorkuang/miaoying) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/creatorkuang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON configuration examples, and generated local files such as QR code images or export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm dependencies, network access to the Miaoying service, and a MIAOYING_API_KEY stored preferably in the environment.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

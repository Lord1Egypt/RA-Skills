## Description: <br>
One-click file sharing with progress tracking and automatic retry over Pilot Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to share a selected file or archived directory with another agent over Pilot Protocol, with progress tracking, confirmation, and retry guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes commands that send selected local files or archives to another agent. <br>
Mitigation: Verify the recipient and inspect the exact file or archive path before running any send command. <br>
Risk: A broad path or archive could include secrets, private keys, customer data, home-directory content, or unrelated personal files. <br>
Mitigation: Share only the intended file or a reviewed archive, and exclude sensitive or unrelated data before transfer. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Share on ClawHub](https://clawhub.ai/teoslayer/pilot-share) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-directed file transfer commands and retry workflow guidance; it does not itself transmit files unless the proposed commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Bidirectional file synchronization between agents over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep directories synchronized between agents, replicate files across nodes, and inspect received files through Pilot Protocol commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can continuously send files from a watched directory to another agent, which may expose sensitive or unintended files. <br>
Mitigation: Use a dedicated non-sensitive sync folder, exclude secrets and hidden files, and stop the watcher when synchronization is complete. <br>
Risk: Files may be sent to the wrong peer if the Pilot Protocol peer ID is incorrect or untrusted. <br>
Mitigation: Verify the peer ID before sending files or starting a watcher. <br>
Risk: The examples describe bidirectional synchronization and conflict detection, but the artifact does not include complete conflict-safe synchronization logic. <br>
Mitigation: Do not rely on the examples for conflict-safe bidirectional sync unless that logic is implemented and reviewed elsewhere. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-sync) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples assume pilotctl, jq, fswatch or inotifywait, md5sum, and stat are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

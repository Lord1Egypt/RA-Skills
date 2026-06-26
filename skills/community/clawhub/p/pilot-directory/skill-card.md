## Description: <br>
Maintains a local directory of known agents with cached metadata for offline reference and quick lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list, find, and look up known Pilot Protocol peers, check trust status, and export cached peer metadata for offline directory workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported directory files can contain cached hostnames, node IDs, tags, or trust context that reveal local network relationship information. <br>
Mitigation: Store exported directory files in a private location and share them only with trusted recipients. <br>
Risk: The skill depends on the local Pilot Protocol setup and pilotctl binary. <br>
Mitigation: Install and use it only in environments where the Pilot Protocol setup and pilotctl binary are already trusted. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-directory) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, JSON] <br>
**Output Format:** [Markdown with inline bash code blocks and generated JSON or text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilotctl binary on PATH and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

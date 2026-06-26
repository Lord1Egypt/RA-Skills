## Description: <br>
Provides Pilot Protocol shell workflows for chunking, sending, receiving, and reassembling large files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using Pilot Protocol can use this skill as command guidance for transferring files larger than 100MB by chunking them, sending chunk metadata and data, and reassembling received chunks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends selected local files and filenames to a pilotctl destination. <br>
Mitigation: Review file paths and the destination before execution, and avoid sensitive transfers unless the destination is trusted and approved. <br>
Risk: The security review says advertised integrity verification and resume behavior are overstated. <br>
Mitigation: Do not rely on the advertised checksum or resume guarantees until receive-side hash validation and end-to-end resume behavior are verified. <br>
Risk: Received files are written under $HOME/.pilot/chunk-recv. <br>
Mitigation: Inspect received filenames and reassembled outputs before opening, moving, or relying on them. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume pilotctl, jq, dd, md5sum, bc, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

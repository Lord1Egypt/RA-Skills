## Description: <br>
Create and visualize mind maps in the terminal with branching and export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and terminal users can use this skill to capture, search, list, and export local brainstorming notes or lightweight project entries. The current implementation should be treated as a plaintext logging utility rather than a visual mind-map renderer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is described as a mind-map visualizer, but the included script behaves as a persistent plaintext note and log manager. <br>
Mitigation: Set user expectations before use and verify the installed script behavior against the desired workflow before relying on it for mind-map visualization. <br>
Risk: Entries and command history are stored locally in plaintext, and the remove command logs a removal without deleting stored entries. <br>
Mitigation: Do not store secrets or sensitive brainstorming content, and manually inspect or delete the data and history logs when removal or retention control matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/mindmap) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text terminal output and local plaintext log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes command history and entries to local files under the configured mindmap data directory.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

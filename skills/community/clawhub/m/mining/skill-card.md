## Description: <br>
Provides shell-command workflows for a Mining-branded local entry tracker that stores, lists, searches, removes, exports, and configures user-provided data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill when they intentionally need a local scratchpad-style CLI for recording, searching, deleting, exporting, and configuring entries. It should not be treated as a mining or blockchain analysis skill unless the publisher updates the release evidence to match that behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as mining analysis but behaves as a local data-management CLI, which could lead users to install it for the wrong purpose. <br>
Mitigation: Review the behavior before installation and use it only when local scratchpad-style entry tracking is intended. <br>
Risk: The skill stores user-provided entries and configuration locally and can export saved data to files. <br>
Mitigation: Do not enter secrets or sensitive business data; set MINING_DIR deliberately and review exported files before sharing them. <br>
Risk: The remove command deletes stored entries by number. <br>
Mitigation: Back up data that must be retained and confirm the target entry before running remove. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/mining) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [Plain text CLI output with local JSONL or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data under ~/.mining by default, or under MINING_DIR when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

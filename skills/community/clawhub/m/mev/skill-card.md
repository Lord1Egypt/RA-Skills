## Description: <br>
Mev is a command-line helper for recording, listing, searching, removing, and exporting MEV-related local entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blockchain or security practitioners can use this skill as a local note store for MEV-related entries, including status checks, adding entries, listing, searching, removing, exporting, statistics, and simple configuration. It should not be treated as an automated MEV analysis or protocol-security assessment tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises MEV and security analysis, but the security evidence describes it as a local data-management tool. <br>
Mitigation: Use it for local note management only, and verify MEV or protocol-security conclusions with appropriate analysis tools and human review. <br>
Risk: Entries may contain sensitive wallet, trading strategy, or incident-response details and are stored locally under ~/.mev unless MEV_DIR is changed. <br>
Mitigation: Avoid storing secrets or sensitive operational details, set MEV_DIR deliberately, and protect or clear the data directory according to local policy. <br>
Risk: The export command can copy stored entries into the current directory, and remove can delete local entries. <br>
Mitigation: Review the target directory and stored data before export or removal, and keep backups when entries need to be retained. <br>


## Reference(s): <br>
- [Mev on ClawHub](https://clawhub.ai/bytesagain1/mev) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [CLI text output with JSONL or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under MEV_DIR, defaulting to ~/.mev, and export can write mev-export.json or mev-export.csv in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

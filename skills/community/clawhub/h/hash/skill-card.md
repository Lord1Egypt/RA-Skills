## Description: <br>
Generate MD5 and SHA checksums, verify integrity, and compare hash values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release engineers, and support teams use Hash to compute checksums for files or text, verify downloads against known hashes, compare file hashes, batch-hash directories, and check checksum manifests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local operation history and batch manifests can retain file paths and hashes under ~/.local/share/hash. <br>
Mitigation: Avoid batch hashing broad or sensitive directories unless retention is intended, and delete history or manifest files when they are no longer needed. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/hash) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text checksum output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch operations can write local manifests and operation history under ~/.local/share/hash.] <br>

## Skill Version(s): <br>
3.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

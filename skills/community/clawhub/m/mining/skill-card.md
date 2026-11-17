## Description:

Advertises mining analysis, but the artifact provides shell commands for maintaining local mining-labeled records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or operators can use this skill as a simple local CLI for adding, listing, searching, removing, exporting, and configuring mining-labeled records. It should not be relied on for blockchain mining analysis, protocol security evaluation, or on-chain research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation overstates mining and blockchain analysis capabilities.

Mitigation: Treat the artifact as a local record manager and independently verify any mining, protocol, or on-chain analysis before use.

Risk: Unsafe shell handling can run unintended commands or corrupt local records when untrusted input is passed to config, add, or search.

Mitigation: Review and patch serialization and shell interpolation before installation, use only trusted input, and run the script in a constrained environment.

Risk: The script writes local data under the user's home directory by default and can export files into the working directory.

Mitigation: Set MINING_DIR to an isolated directory and inspect generated JSON, CSV, and configuration files before sharing or reusing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/mining)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write JSONL records under MINING_DIR, defaulting to ~/.mining, and can export JSON or CSV files.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

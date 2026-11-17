## Description:

Analyze mev operations. Use when you need to understand mev mechanisms, evaluate protocol security, or reference on-chain concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and blockchain practitioners can use this skill's CLI-style workflow to store, search, export, and inspect local notes related to MEV concepts. It should not be relied on for protocol-security decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims MEV and protocol-security analysis capability, while the inspected implementation is a local entry manager.

Mitigation: Review it as a note/config/export utility and do not rely on it for protocol-security decisions.

Risk: The script can create local data under ~/.mev or MEV_DIR, delete entries, and export unescaped data.

Mitigation: Run it only in a trusted workspace, review stored data before sharing exports, and confirm delete targets before using remove.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/mev)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local data, configuration, and export files under the configured MEV data directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

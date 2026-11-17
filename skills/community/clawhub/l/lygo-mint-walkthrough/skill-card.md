## Description:

LYGO Mint Walkthrough is an interactive tutorial for a local mint, verify, anchor snippet, and optional backfill workflow using canonicalization, SHA-256 hashing, and local ledger records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and agents use this skill to walk through minting a pack, verifying its SHA-256 hash, creating a public anchor snippet, and recording optional backfill metadata while keeping publication manual.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The self-check can write persistent local ledger state and leave a temporary test file even though the skill advertises consent-gated writes.

Mitigation: Review before installing and do not run scripts/self_check.py unless local ledger writes and temporary files are acceptable.

Risk: Ledger records can store local file paths and hashes for pack content.

Mitigation: Do not mint packs that contain secrets, and use consent-gated mint or backfill steps only after reviewing the pack and intended local records.

Risk: Anchor snippets are intended for manual public posting and could expose metadata if copied without review.

Mitigation: Review generated snippets before publishing and keep the human publisher in control of any external posting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-mint-walkthrough)
- [Publisher Profile](https://clawhub.ai/user/deepseekoracle)
- [OpenClaw Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-mint-walkthrough)
- [Security Notes](references/SECURITY.md)
- [Sample Pack](examples/sample_pack.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON script output, and anchor snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first workflow; no network, subprocess, or automated publishing according to server evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

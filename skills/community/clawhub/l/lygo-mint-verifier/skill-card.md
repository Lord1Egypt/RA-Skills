## Description: <br>
LYGO-MINT verifier for Champion/alignment prompt packs: canonicalize a pack, generate a deterministic SHA-256 hash, write append-only and canonical ledgers, and output a portable Anchor Snippet for posting anywhere (Moltbook/Moltx/X/Discord/4claw). Use when you need verifiable, hash-addressed alignment artifacts (Champion packs, summon prompts, workflow packs) with receipts and optional anchor backfill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeepSeekOracle](https://clawhub.ai/user/DeepSeekOracle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to mint verifiable prompt or workflow packs by canonicalizing a local pack, generating a SHA-256 hash, writing ledger receipts, and producing an Anchor Snippet for later posting and backfill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python helpers and depends on separate workspace tools for minting and ledger canonicalization. <br>
Mitigation: Review tools/lygo_mint/mint_pack.py and tools/lygo_mint/canonicalize_ledger.py before using the skill, especially in workspaces that contain sensitive files. <br>
Risk: Generated state and ledger files may preserve filenames, metadata, hashes, and anchor URLs. <br>
Mitigation: Use non-secret prompt packs and controlled workspaces when minting or anchoring material. <br>


## Reference(s): <br>
- [LYGO-MINT Verifier process](references/process.md) <br>
- [ClawHub release page](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier) <br>
- [Publisher profile](https://clawhub.ai/user/DeepSeekOracle) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown and plain text with shell commands, plus local JSON/JSONL ledger files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deterministic hash receipts, portable anchor snippets, append-only ledger updates, and canonical ledger entries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Advanced LYGO-MINT Operator Suite (v2): canonicalize multi-file packs, generate per-file and bundle hashes, write append-only and canonical ledgers, produce machine-readable multi-platform Anchor Snippets, and verify third-party packs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeepSeekOracle](https://clawhub.ai/user/DeepSeekOracle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and external reviewers use this skill to canonicalize prompt or workflow packs, generate deterministic hashes and ledger receipts, create anchor snippets, and verify third-party packs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad input folders may include secrets or unrelated files in generated manifests, ledgers, or bundles. <br>
Mitigation: Use a clean, narrow pack folder and review generated records before sharing. <br>
Risk: Generated records may expose filenames, hashes, sizes, and local path details. <br>
Mitigation: Review manifests, ledgers, anchor snippets, and bundles before publishing or distribution. <br>


## Reference(s): <br>
- [Process](references/process.md) <br>
- [Whitepaper v2](references/whitepaper_v2.md) <br>
- [ClawHub release page](https://clawhub.ai/DeepSeekOracle/lygo-mint-operator-suite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON, ledger, bundle, and anchor snippet files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local provenance artifacts such as manifests, hashes, ledgers, deterministic bundles, and anchor snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

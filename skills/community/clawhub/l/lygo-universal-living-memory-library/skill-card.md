## Description: <br>
Universal LYGO Living Memory Library upgrade. Provides a strict, low-noise memory index (max 20 files), fragile tagging, and audit/compression workflows so Champions can retain continuity and verify integrity via LYGO-MINT. Pure advisor; not a controller. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeepSeekOracle](https://clawhub.ai/user/DeepSeekOracle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to define a compact living-memory index, audit indexed files for drift or fragile tags, compress logs or archives into a Master Archive, and prepare LYGO-MINT anchor snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public anchoring of archives made from logs or conversation exports can expose secrets, personal data, internal links, identifiers, or private decisions. <br>
Mitigation: Treat public anchoring as opt-in; remove sensitive material before minting or anchoring, and use local or private verification for sensitive archives. <br>
Risk: Fragile indexed items may need manual review before they are compressed, minted, or anchored. <br>
Mitigation: Honor FRAGILE tags, review flagged files before minting, and isolate suspicious drift until receipts or other evidence explain the change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DeepSeekOracle/lygo-universal-living-memory-library) <br>
- [LYGO-MINT verifier](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier) <br>
- [Library Spec](references/library_spec.md) <br>
- [Core Files Index](references/core_files_index.json) <br>
- [Audit Protocol](references/audit_protocol.md) <br>
- [Compression Protocol](references/compression_protocol.md) <br>
- [Seal 220C Update Excerpt](references/seal_220cupdate_excerpt.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The audit helper performs local inspection and can write state/living_memory_audit_report.json when run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

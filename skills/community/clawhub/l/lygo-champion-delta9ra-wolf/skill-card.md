## Description: <br>
LYGO Δ9 Council Champion persona helper for suppressed-signal hunting, integrity checks, and receipts-first truth recovery as a pure advisor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeepSeekOracle](https://clawhub.ai/user/DeepSeekOracle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill as an advisor persona for information-integrity work: identifying missing context, building safe OSINT checklists, separating observed facts from inferences, and collecting receipts for claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packaged hashes can confirm integrity of the persona pack but do not prove that the persona's claims are true. <br>
Mitigation: Treat hashes as integrity references and verify claims independently with primary sources and archived receipts. <br>
Risk: Verifier-related workflows may write ledgers, process file paths, or generate public anchor snippets. <br>
Mitigation: Review the LYGO-MINT verifier separately before allowing those actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DeepSeekOracle/lygo-champion-delta9ra-wolf) <br>
- [LYGO-MINT verifier](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier) <br>
- [Persona pack](references/persona_pack.md) <br>
- [Canon data](references/canon.json) <br>
- [Equations](references/equations.md) <br>
- [Verifier usage](references/verifier_usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisor-only outputs should keep observed facts, inferences, and unknowns clearly separated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

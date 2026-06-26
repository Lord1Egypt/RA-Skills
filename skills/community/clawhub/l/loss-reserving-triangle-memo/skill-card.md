## Description: <br>
Creates a draft P&C loss reserving memo from paid and incurred triangles, exposure data, and prior selections, including reserving methods, diagnostics, sensitivities, and a judgment log for actuary review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
P&C reserving actuaries, actuarial analysts, captive actuaries, and reinsurance actuaries use this skill to prepare peer-reviewable draft reserving work papers that support reserve selections and Appointed Actuary review. It is not a signed Statement of Actuarial Opinion, regulatory filing, or legal, accounting, investment, or solvency opinion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft reserve indications could be mistaken for final actuarial opinions or regulatory filings. <br>
Mitigation: Keep the output labeled as draft work-paper support and require review and signature by a credentialed actuary before relying on any reserve selection. <br>
Risk: Users may paste sensitive insurance, claimant, or company identifiers into the working memo. <br>
Mitigation: Use non-identifying book and segment codes, and redact claimant names, named insureds, claim numbers, SSNs, tax IDs, and NAIC codes. <br>
Risk: Wallet access, credentials, or secrets may be supplied even though the skill does not need them. <br>
Mitigation: Do not grant wallet access or provide secrets, credentials, or sensitive tokens when using this text-only drafting skill. <br>
Risk: Incomplete triangles or unsupported assumptions can produce misleading reserve indications. <br>
Mitigation: Review data quality, unresolved information, diagnostics, method selections, sensitivity results, and the judgment log before using the memo for actuarial review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/loss-reserving-triangle-memo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown draft memo with tables, diagnostics, sensitivity analysis, unresolved-information notes, and a judgment log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only actuarial support output requiring credentialed actuary review before reliance] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

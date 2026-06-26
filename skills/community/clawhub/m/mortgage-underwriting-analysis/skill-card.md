## Description: <br>
Analyzes residential mortgage borrower files against CFPB ATR/QM rules and agency guidelines, computes DTI, LTV, CLTV, QM eligibility, and produces a draft underwriting analysis memo for licensed-underwriter review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Loan officers, processors, and underwriters use this skill to structure a preliminary residential mortgage underwriting analysis, identify missing file data, compare borrower metrics with agency guidelines, and draft an Approve, Refer, or Suspend memo for licensed-underwriter review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive mortgage files may contain unnecessary SSNs, account numbers, or other private borrower data. <br>
Mitigation: Avoid entering unnecessary sensitive identifiers, mask borrower identifiers in outputs, and follow the skill's draft-flags checklist before sharing a memo. <br>
Risk: Draft calculations or guideline comparisons may be incomplete, stale, or wrong for a lender's current overlays. <br>
Mitigation: Verify all calculations, current agency and lender rules, AUS findings, and conditions before relying on the memo. <br>
Risk: A draft memo could be mistaken for a credit decision or commitment to lend. <br>
Mitigation: Keep the output labeled as a draft analysis aid and require licensed-underwriter review before any lending action. <br>
Risk: Use of protected-class or other discriminatory factors would create fair-lending risk. <br>
Mitigation: Base analysis only on financial, property, and program eligibility criteria, and exclude protected-class attributes from the underwriting memo. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/archlab-space/mortgage-underwriting-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown draft memo with calculation tables, agency guideline comparison, conditions list, recommendation, and draft flags checklist.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code or live system access; outputs require calculation verification and licensed-underwriter review before use in lending actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

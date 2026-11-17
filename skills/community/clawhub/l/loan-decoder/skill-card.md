## Description:

Decodes personal, auto, or mortgage loan offers by calculating total cost, reconciling APR against advertised rates, and ranking financial red flags such as fees, penalties, add-ons, and reset exposure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-review agents use this skill to translate loan paperwork into a plain-language cost analysis with visible arithmetic, ranked red flags, negotiable terms, and questions that most affect the deal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loan documents can contain account numbers, unnecessary personal identifiers, or other sensitive financial details.

Mitigation: Provide only the loan details needed for analysis and remove account numbers or unnecessary personal identifiers before using the skill.

Risk: The output is a plain-language loan review and may affect legal or financial decisions if treated as professional advice.

Mitigation: Verify important legal or financial decisions with a qualified professional, especially for jurisdiction-dependent terms.

Risk: Incomplete loan paperwork can make total cost, APR reconciliation, reset exposure, or early-exit costs uncertain.

Mitigation: List missing values as [to confirm] and avoid silently estimating terms, rates, fees, or penalties that are not present in the document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/loan-decoder)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/loan-decoder.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown loan decode with visible arithmetic, a decode table, ranked red flags, negotiation guidance, and a disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided loan terms or document text; missing values are listed as [to confirm] rather than estimated silently.]

## Skill Version(s):

50.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Calculate mortgage payments with equal-principal and equal-interest comparisons. Use when comparing loans, calculating payments, evaluating prepayment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to calculate and compare mortgage repayment scenarios, evaluate prepayment outcomes, estimate affordability, and manage local mortgage-related notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store mortgage and financial notes in local plaintext logs and export them to stdout.

Mitigation: Avoid entering sensitive mortgage, income, account, or lender details unless plaintext local storage and export behavior are acceptable.

Risk: The remove command may not erase stored records.

Mitigation: Do not rely on the remove command for deletion until the implementation is fixed; inspect and manage the data files directly when erasure is required.

## Reference(s):

- [Mortgage Calculator on ClawHub](https://clawhub.ai/ckchzh/skills/mortgage-calculator)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and terminal text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local plaintext data logs under the configured mortgage-calculator data directory and export records to stdout.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

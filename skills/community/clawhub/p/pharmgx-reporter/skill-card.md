## Description:

Pharmacogenomic report from DTC genetic data (23andMe/AncestryDNA).

This skill is for research and development only.

## Publisher:

[manuelcorpas](https://clawhub.ai/user/manuelcorpas)

### License/Terms of Use:

MIT

## Use Case:

Researchers, developers, and precision-medicine reviewers can use this skill to generate educational pharmacogenomic Markdown reports from consumer genetic data files. The reports summarize detected pharmacogenomic variants, gene phenotypes, drug-response categories, and medication alerts for review by qualified professionals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill generates medication guidance from sensitive genetic data and may produce high-stakes recommendations.

Mitigation: Use reports only for education or research review, keep them private, and require clinician review before any medication decision.

Risk: Consumer genetic files may be incomplete for pharmacogenomic use.

Mitigation: Confirm clinically relevant findings with clinical-grade testing before acting on report outputs.

Risk: Report files contain genetic and medication-response information.

Mitigation: Store generated reports in access-controlled locations and avoid sharing them outside the intended review workflow.

## Reference(s):

- [ClawBio homepage](https://github.com/ClawBio/ClawBio)
- [PharmGx Reporter Skill Page](https://clawhub.ai/manuelcorpas/skills/pharmgx-reporter)
- [CPIC](https://cpicpgx.org/)
- [PharmGKB](https://www.pharmgkb.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports include an input checksum, detected format, gene profiles, drug recommendation tables, alerts, methods, reproducibility command, and clinical-use disclaimers.]

## Skill Version(s):

0.2.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

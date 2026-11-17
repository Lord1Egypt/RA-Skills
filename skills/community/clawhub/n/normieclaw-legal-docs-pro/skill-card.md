## Description:

Legal Docs Pro helps agents draft, review, explain, and export legal document templates for freelancers, solopreneurs, and small businesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as freelancers, solopreneurs, and small businesses use this skill to generate legal document drafts, review contracts for risky clauses or missing protections, and reuse stored business details. Its legal templates and analysis are informational and should be paired with attorney review for complex, high-value, or jurisdiction-specific matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious and warns that scripts can expose sensitive local files or run unintended code from crafted input.

Mitigation: Review or patch the release before installation, run scripts only from the intended skill directory, and avoid scanning untrusted files or arbitrary paths.

Risk: Business profiles, generated contracts, reviews, and dashboard records may contain sensitive business data, including EINs and contract terms.

Mitigation: Avoid entering sensitive identifiers unless required, restrict local file permissions, and treat all generated legal records as sensitive local files.

Risk: Contract text and generated legal content may enter the AI provider's conversation context.

Mitigation: Review the AI provider's data handling terms before processing confidential agreements, and avoid AI-assisted review for highly sensitive matters unless approved.

Risk: Generated legal templates and contract analysis may be incomplete, outdated, or unsuitable for a specific jurisdiction.

Mitigation: Use the output for informational drafting and review, and consult a licensed attorney for complex, high-value, employment, real estate, or jurisdiction-specific matters.

## Reference(s):

- [ClawHub listing for Legal Docs Pro](https://clawhub.ai/nollio/skills/normieclaw-legal-docs-pro)
- [NormieClaw](https://normieclaw.ai)
- [Pandoc installation documentation](https://pandoc.org/installing.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown legal drafts, contract review summaries, plain-English explanations, shell command snippets, and local configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local profile settings, save generated documents and reviews, and export markdown or PDF files when optional tools are installed.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Deep internationalization workflow: string extraction, ICU messages, formats, pseudolocale testing, and developer workflow for preparing software for translation before full localization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare applications for multilingual releases by scoping pilot locales, extracting user-visible strings, adopting ICU messages, applying locale-aware formatting, and adding pseudolocale or staging QA checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may lead to broad codebase changes, including string extraction, lint rule additions, and test updates.

Mitigation: Define product areas and pilot locales before use, then review generated code, configuration, and test changes through normal development review.

Risk: Incorrect locale formatting or message handling can change user-visible behavior across languages.

Mitigation: Confirm framework choices, ICU placeholder rules, and timezone policy before implementation, then use pseudolocale or staging locale checks for critical screens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codenova58/skills/i18n)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with checklists and implementation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose codebase changes such as string extraction, lint rules, formatting updates, and tests.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

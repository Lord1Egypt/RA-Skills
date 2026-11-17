## Description:

Pocketbook records, queries, completes, corrects, and undoes personal bookkeeping entries through short natural-language conversation, with local JSONL and Markdown persistence plus support for incomplete entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suru711](https://clawhub.ai/user/suru711)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Pocketbook to operate a personal ledger: capture expenses, income, refunds, and transfers; summarize spending or income; review recent entries; complete incomplete records; and correct or undo recent ledger events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive personal finance data in ordinary local files.

Mitigation: Use a private data directory with appropriate filesystem permissions and review where ledger, profile, and Markdown files are stored before use.

Risk: The Markdown renderer accepts an optional output path that can overwrite any writable file.

Mitigation: Avoid passing --output except for the intended Pocketbook Markdown file, and review the exact output path before rendering.

Risk: Implicit invocation could write ledger entries when the user's intent is ambiguous.

Mitigation: Require confirmation for medium-confidence transaction utterances or disable implicit invocation for deployments that need stricter write controls.

Risk: Default timezone and currency may not match the user's locale.

Mitigation: Configure timezone and currency before use if Asia/Shanghai and CNY are not intended.

## Reference(s):

- [Pocketbook ClawHub Skill Page](https://clawhub.ai/suru711/skills/pocket-book)
- [Pocketbook Project Homepage](https://github.com/SuRu711/pocketbook)
- [Pocketbook Schema](artifact/references/schema.md)
- [Trigger Examples](artifact/references/intent-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise natural-language ledger replies, structured JSON command payloads and results, and Markdown finance snapshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists ledger state locally as JSONL, renders a derived Markdown view, and can use profile defaults and aliases for currency, timezone, payment method, and account values.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

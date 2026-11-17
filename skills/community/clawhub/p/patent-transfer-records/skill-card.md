## Description:

Looks up disclosed patent assignment events for supplied patent numbers and creates a dated ownership-change timeline with source records and unresolved fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent owners and IP teams use this skill to review disclosed assignment events for supplied patent numbers and organize returned records into sourced timelines for internal tracking or preliminary transaction review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent identifiers and search queries are sent to PatentMax, and lookups may use paid balance.

Mitigation: Set a task budget, keep searches within the supplied scope, and avoid sending unpublished technical secrets.

Risk: The client can cache API credentials locally when the user chooses persistent storage.

Mitigation: Choose temporary use unless persistence is needed, and store a persistent key only in a private user location.

Risk: Database coverage and public disclosures may be incomplete, so missing events do not establish that no transfer occurred.

Mitigation: Describe results as records returned in the lookup and verify important ownership conclusions against official records.

## Reference(s):

- [API reference](artifact/references/api-reference.md)
- [Legal event review guidance](artifact/references/legal-event-review.md)
- [Key setup](artifact/references/key-setup.md)

## Skill Output:

**Output Type(s):** [Analysis, CSV files, Markdown, Source records]

**Output Format:** [CSV timeline with source JSON records and a concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves returned source fields and identifies missing or unresolved event details.]

## Skill Version(s):

1.0.2 (source: frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

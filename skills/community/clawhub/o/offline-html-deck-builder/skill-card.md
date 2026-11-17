## Description:

Builds proposal, report, retrospective, or product narrative materials into offline, single-file HTML slide decks for sharing without PDF lock-in, presentation software drift, or external resource dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT

## Use Case:

Employees, external collaborators, operators, product teams, and researchers can use this skill to turn source material into a clean local HTML presentation. It is suited to concise narrative decks that should open locally in a browser and avoid external web dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decks may accidentally include private customer names, account identifiers, internal IDs, or confidential screenshots.

Mitigation: Review generated deck content before sharing and remove sensitive details from templates, source notes, and screenshots.

Risk: Adding external fonts, CDNs, remote images, or online scripts can break the intended offline behavior.

Mitigation: Use the included offline checklist to verify that CSS is embedded and the final HTML opens correctly without network access.

## Reference(s):

- [Offline deck checklist](references/deck-checklist.md)
- [ClawHub skill page](https://clawhub.ai/shiyan521/skills/offline-html-deck-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Single-file HTML with embedded CSS, plus Markdown notes or review checklist when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline-oriented output; generated decks should avoid external fonts, CDNs, remote images, and online scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

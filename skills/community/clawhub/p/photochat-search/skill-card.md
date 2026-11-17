## Description:

Searches a user's PhotoCHAT library for photos using natural language queries through the PhotoCHAT CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[photochat](https://clawhub.ai/user/photochat)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find photos in a local PhotoCHAT library from natural language requests, then return parseable results with paths, match counts, filters, and scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic image-search requests could trigger searches over private local photos and expose absolute file paths.

Mitigation: Install only when PhotoCHAT should handle ordinary photo-finding requests, and review returned paths or images before sharing them.

Risk: Ambiguous dates can retrieve unintended photos.

Mitigation: Clarify ambiguous dates before searching and use the documented day-first parsing option when appropriate.

## Reference(s):

- [PhotoCHAT Search Examples](references/search-examples.txt)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with PowerShell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include absolute file paths, match counts, parsed filters, and optional similarity scores.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

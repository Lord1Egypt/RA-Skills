## Description:

Ask the user for their Google saved places list, look up each place with goplaces, and recommend the single best one to visit today based on their preferences and visit history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsq704252212](https://clawhub.ai/user/wsq704252212)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to choose one place to visit from their saved Google Places list. It imports saved places, maintains local visit history and notes, uses goplaces/Google Places lookups for current details, and ranks options against stated cuisine, location, and recency preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores saved places, notes, visit history, city classifications, and preferences locally, which can reveal sensitive location patterns.

Mitigation: Use it only with data the user agrees to store locally, restrict access to the state file, and clear or minimize saved history when it is no longer needed.

Risk: Lookup terms are sent through goplaces/Google Places and may expose saved place names or location preferences to external services.

Mitigation: Tell users before lookups are performed and avoid submitting sensitive private locations unless the user explicitly accepts that disclosure.

Risk: The skill shows shell-style goplaces commands that include user-controlled place names.

Mitigation: Invoke goplaces with shell execution disabled and literal argument arrays; do not execute untrusted pasted CSV content or place names through a shell.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wsq704252212/skills/goplaces-togo)
- [Google Takeout](https://takeout.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendation with a ranked table, inline shell command examples, and local JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists saved places, notes, city classifications, preferences, and visit history in a local JSON file]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

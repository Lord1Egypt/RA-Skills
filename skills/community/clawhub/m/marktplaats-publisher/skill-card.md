## Description:

Marktplaats-advertenties voorbereiden, plaatsen/bewerken, copy-QA, preflight, live-verificatie en register.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roelbroersma](https://clawhub.ai/user/roelbroersma)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare, check, place or update normal Marktplaats sale advertisements with script-gated copy QA, preflight checks, live verification and a local register.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use a local agent with the user's logged-in Safari Marktplaats session and write ad snapshots or registers.

Mitigation: Use only when comfortable with that local access pattern, keep snapshots private, and inspect logs or snapshots for sensitive data before sharing.

Risk: The probe workflow can read authenticated browser forms and may forward user-supplied cookies or headers if misused.

Mitigation: Do not pass cookies, cookie files, Authorization headers, or non-Marktplaats URLs to the probe tool.

## Reference(s):

- [Marktplaats Skill Page](https://clawhub.ai/roelbroersma/skills/marktplaats-publisher)
- [README](README.md)
- [Nederlandse handleiding](references/handleiding-nl.md)
- [English guide](references/guide-en.md)
- [Robust posting checklist](references/robust-posting-checklist.md)
- [Setup for small models](references/setup-small-model-nl.md)
- [Background Safari flow](references/background-safari-nl.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local JSON file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and may use a logged-in Safari Marktplaats session for authenticated checks.]

## Skill Version(s):

0.6.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

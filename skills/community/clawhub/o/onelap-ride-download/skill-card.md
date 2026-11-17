## Description:

Downloads Onelap cycling activity FIT files so users can back up and export ride records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckboss](https://clawhub.ai/user/ckboss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve personal Onelap ride FIT files for backup, import into third-party fitness platforms, or local activity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a logged-in Onelap browser session to locate and download personal activity files.

Mitigation: Install and run it only when the user explicitly authorizes access to that session and understands the account data being exposed.

Risk: FIT download URLs may include tokens and may use plain HTTP.

Mitigation: Avoid sharing full FIT URLs, prefer HTTPS-only links when available, and treat tokenized links as sensitive until they expire.

Risk: Downloaded FIT files can contain sensitive health and location data.

Mitigation: Store files only in a user-chosen location and handle exported ride records as private personal data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckboss/skills/onelap-ride-download)
- [Onelap activity analysis page](https://u.onelap.cn/analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces download commands and file organization guidance for FIT activity files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

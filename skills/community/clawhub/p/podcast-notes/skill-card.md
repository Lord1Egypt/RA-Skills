## Description:

Podcast Notes helps podcast producers draft outlines, show notes, intro scripts, guest questions, monetization ideas, distribution notes, and related episode content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External podcast creators and content teams use this skill to prepare, revise, organize, search, and export podcast production notes across episode planning, show notes, promotion, localization, and repurposing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Podcast content is stored in local plaintext logs and exports can include the full note history.

Mitigation: Avoid entering secrets, confidential sponsor details, or unpublished material unless plaintext local storage and full-history export are acceptable.

Risk: Search and export behavior has scanner-identified flaws around out-of-scope file reads and unsafe exported data.

Mitigation: Review before installing, fix grep option handling, and use proper JSON and CSV serializers before treating the skill as low risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/podcast-notes)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)
- [Publisher homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with command examples and local log/export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores timestamped entries in local plaintext logs and exports accumulated notes as JSON, CSV, or TXT files.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

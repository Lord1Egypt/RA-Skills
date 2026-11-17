## Description:

Uploads local IELTS reading review JSON files to www.liuxue.online, with token-based account sync and an anonymous fallback mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and agents use this skill to upload existing IELTS reading review JSON files, compare local and server records, and view synchronized review progress on www.liuxue.online.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads IELTS review data to www.liuxue.online and uses local account tokens for token mode.

Mitigation: Install and run it only after accepting that data flow, and review local token storage before using account sync.

Risk: Anonymous mode can send a persistent local identifier and OS username.

Mitigation: Prefer token mode for normal use, or set explicit anonymous identifiers only after deciding that disclosure is acceptable.

Risk: The publishing helper can modify local skill installations and is intended for maintainers.

Mitigation: Do not run publish-clawhub.sh unless maintaining the package and prepared for its local install changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dengjiawei1226/skills/ielts-tuyaya-upload)
- [www.liuxue.online IELTS dashboard](https://www.liuxue.online/ielts/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of local shell or Node.js upload commands that send JSON review data to www.liuxue.online.]

## Skill Version(s):

1.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

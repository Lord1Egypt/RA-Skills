## Description:

Search local documents and knowledge bases, retrieve cited answers, and manage notes and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmickel](https://clawhub.ai/user/gmickel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other knowledge workers use GNO to index and search local documents, notes, and agent-session archives, retrieve answers with citations, and manage selected notes or memory records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session archives can contain sensitive conversations.

Mitigation: Keep archives separate and local unless sharing is explicitly approved.

Risk: Writes, hooks, and schedules can change local files or automate actions.

Mitigation: Enable these capabilities only when wanted, and choose folders carefully.

Risk: Batch exports may overwrite earlier output files.

Mitigation: Use unique filenames and overwrite protection.

## Reference(s):

- [GNO on ClawHub](https://clawhub.ai/gmickel/skills/gno)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Plain-text or Markdown answers with local citations; optional JSON, CSV, or file-list results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers may include citations to local document URIs and line ranges.]

## Skill Version(s):

1.2.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

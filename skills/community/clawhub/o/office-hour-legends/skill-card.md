## Description:

Office Hour Legends runs YC-style office-hours sessions through selected partner or alumni personas, with optional Fathom transcript review for timestamped pitch, investor-call, or customer-conversation feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prodigalson](https://clawhub.ai/user/prodigalson)

### License/Terms of Use:

MIT-0

## Use Case:

External founders and builders use this skill to run simulated YC-style office hours, pressure-test startup ideas, and review pitch or customer-call transcripts with persona-guided feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process sensitive meeting transcripts and private forum content.

Mitigation: Use transcript review only for meetings the user is allowed to process, avoid committing or syncing saved session documents, and treat private-forum excerpts as sensitive.

Risk: Server security evidence reports a local code-injection issue in the Fathom recording-ID path.

Mitigation: Do not enable the Fathom transcript script with untrusted recording IDs until the path is fixed or constrained to trusted numeric IDs.

Risk: The optional Bookface integration depends on a third-party script that may handle YC credentials and cached sessions.

Mitigation: Review and pin the third-party script before use, and handle any YC credentials or cached sessions according to the user's access policy.

Risk: Persona-guided coaching can sound authoritative while still being simulated advice.

Mitigation: Do not present outputs as statements from the named people; review recommendations before using them for business decisions.

## Reference(s):

- [Office Hour Legends on ClawHub](https://clawhub.ai/prodigalson/skills/office-hour-legends)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Optional Bookface Integration](https://github.com/voska/bookface-search)
- [Optional Hacker News CLI Integration](https://github.com/voska/hn-cli)
- [Fathom](https://fathom.video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation output with optional saved Markdown session documents and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local persona files, use optional Fathom, Bookface, or Hacker News integrations, and write session documents in full mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

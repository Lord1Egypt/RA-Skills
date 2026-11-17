## Description:

My Diary helps users record, view, search, and delete personal diary entries stored in a local JSON file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nancyzhong2024](https://clawhub.ai/user/nancyzhong2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with an AI assistant to maintain a personal diary: writing timestamped entries, browsing summaries, reading entries, keyword searching, and deleting entries after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diary entries are sensitive personal content stored as plaintext JSON at the documented local path.

Mitigation: Use a private, access-restricted storage location and avoid shared machines or logged/shared assistant sessions.

Risk: View and search commands can reveal stored personal diary content.

Mitigation: Run the skill only in trusted sessions and review requests before displaying or searching diary entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nancyzhong2024/skills/my-diary)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Text responses and local JSON diary entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diary entries include id, content, and created_at fields; deletion requires confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

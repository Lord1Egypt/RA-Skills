## Description:

LetPub Skills helps agents query LetPub journal details, collect and analyze submission comments, and recommend journals for manuscript submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yon8](https://clawhub.ai/user/yon8)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, publication advisors, and writing-support agents use this skill to look up journal metadata, assess LetPub submission comments, and produce journal recommendations from a manuscript abstract and target constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a suspicious verdict because the skill handles LetPub login credentials and session cookies.

Mitigation: Install only when that handling is acceptable; keep credentials and cookies out of version control, logs, and backups, restrict access to the files, and rotate or revoke them if exposed.

Risk: Artifact behavior includes storing LetPub credentials in assets/credentials.json and cookies in assets/cookies.json, and login helper output can include sensitive response or cookie data.

Mitigation: Use a dedicated account where possible, avoid running login flows in shared terminals or CI logs, and scrub terminal output before sharing diagnostics.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yon8/skills/letpub-skills)
- [Search journal reference](artifact/references/search_journal.md)
- [Journal detail reference](artifact/references/get_journal_detail.md)
- [Journal comments reference](artifact/references/get_journal_comments.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include parsed journal data, comment analysis summaries, recommendation rationale, and credential or cookie setup guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

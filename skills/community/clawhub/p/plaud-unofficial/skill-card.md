## Description:

Use when accessing Plaud voice recorder data, including recordings, transcripts, and AI summaries, with credential setup guidance and patterns for plaud_client.py.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardsellem](https://clawhub.ai/user/leonardsellem)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to configure access to Plaud account data, list recordings, retrieve transcripts and AI summaries, and download audio through the included Python client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to extract and store a long-lived Plaud bearer token in plaintext.

Mitigation: Use only accounts you control, avoid command-line token arguments, store the .env file with owner-only permissions, keep it out of backups and version control, and rotate the token if exposure is suspected.

Risk: The included client can access sensitive Plaud recordings, transcripts, summaries, and downloaded audio.

Mitigation: Install and run the skill only when you are comfortable granting it access to the target Plaud account data, and review downloaded files before sharing them.

## Reference(s):

- [Plaud API Documentation](artifact/PLAUD_API.md)
- [Plaud Web App](https://web.plaud.ai)
- [ClawHub Skill Page](https://clawhub.ai/leonardsellem/skills/plaud-unofficial)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python client usage patterns, configuration examples, and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read Plaud account metadata, transcripts, summaries, and audio files when supplied with a valid bearer token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Check NZBGet download status and queue information. Use when the user asks about NZBGet downloads, wants to know how many things are downloading, check download speed, view the queue, or get a full status report of their Usenet downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aricus](https://clawhub.ai/user/aricus)

### License/Terms of Use:


## Use Case:

Users and operators with an NZBGet instance use this skill to check download counts, speed, queue contents, and concise status reports from their Usenet download queue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NZBGet credentials may be exposed because the helper constructs a plaintext HTTP URL containing the username and password.

Mitigation: Use the skill only with a trusted local NZBGet instance, or update the helper to use HTTPS and curl authentication options that keep credentials out of the URL.

Risk: Using the helper against a remote NZBGet host over an untrusted network could disclose credentials or status data.

Mitigation: Avoid remote untrusted network use and prefer a least-privileged NZBGet account when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aricus/skills/nzbget)
- [Publisher profile](https://clawhub.ai/user/aricus)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise text or Markdown summaries with optional shell command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queue listings are capped at 10 items in the bundled script.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

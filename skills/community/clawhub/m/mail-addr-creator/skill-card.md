## Description:

Creates one or many ordinary mailbox addresses in a Cloudflare temporary mail system through the /admin/new_address admin API and returns structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcwang502](https://clawhub.ai/user/jcwang502)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to create single or batch mailbox addresses in a Cloudflare temporary mail system through the backend admin API and receive structured JSON or CSV results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles admin credentials and returned mailbox secrets.

Mitigation: Use trusted environments, prefer environment variables over command-line secrets, and treat output files and transcripts as sensitive.

Risk: The API endpoint can be overridden with CLOUDFLARE_MAIL_API_URL.

Mitigation: Keep CLOUDFLARE_MAIL_API_URL unset unless intentionally using a trusted endpoint.

Risk: Generated JSON or CSV may include mailbox JWTs or passwords.

Mitigation: Store exports only in protected locations and avoid sharing logs or transcripts containing results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcwang502/skills/mail-addr-creator)
- [API Reference](artifact/references/api.md)
- [Example Prompts](artifact/references/examples.md)
- [Create Address API Endpoint](https://mail-api.suilong.online/admin/new_address)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON or CSV results, with Markdown summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include mailbox JWTs or passwords returned by the admin API; treat transcripts and output files as sensitive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

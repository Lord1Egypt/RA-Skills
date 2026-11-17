## Description:

Looper automates content creation, code improvement, and social media posting through scheduled Looper API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builder-nc](https://clawhub.ai/user/builder-nc)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use this skill to create and manage Looper workflows for scheduled blog generation, code review, content creation, and multi-platform social posting. Agents can configure loops, connect GitHub targets, trigger runs, and inspect tenant-scoped loop status through the Looper API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad authority to create accounts, store admin keys, and run persistent automations that may publish content or change repositories.

Mitigation: Use it only with accounts and repositories the operator is comfortable letting Looper manage, and confirm each GitHub connection and auto-publish loop before enabling scheduled runs.

Risk: Prompts or environment setup may expose API keys, inline passwords, or other credentials.

Mitigation: Store LOOPER_ADMIN_KEY and related service keys in a secret manager or protected environment variables, and avoid placing secrets directly in prompts or generated examples.

Risk: Changing LOOPER_API_URL can redirect authenticated requests to an untrusted destination.

Mitigation: Leave LOOPER_API_URL unset for the default Looper API unless the alternate endpoint is fully trusted.

## Reference(s):

- [Looper Skill Page](https://clawhub.ai/builder-nc/skills/looper)
- [Looper Homepage](https://looper.bot)
- [Looper API](https://api.looper.bot)
- [Looper API Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated actions require LOOPER_ADMIN_KEY; LOOPER_API_URL is optional and should only be set to a trusted Looper API endpoint.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

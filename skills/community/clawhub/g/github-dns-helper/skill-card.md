## Description:

GitHub DNS helper for diagnosing GitHub connectivity problems and applying hosts-file based DNS fixes when GitHub access, DNS resolution, or connections fail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thincher](https://clawhub.ai/user/thincher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to check GitHub connectivity and run a helper script that can update local hosts entries for GitHub-related domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can change system-wide DNS behavior by editing the hosts file.

Mitigation: Run it only after reviewing proposed hosts entries, keep a backup, and use operating-system default ownership and permissions for the hosts file.

Risk: Custom hosts URLs and unvalidated shell execution can expose users to unsafe commands or malicious DNS mappings.

Mitigation: Use trusted hosts sources, avoid custom URLs unless reviewed, and prefer an updated implementation that validates hostnames/IPs and avoids shell=True.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thincher/skills/github-dns-helper)
- [Default hosts source: raw.hellogithub.com](https://raw.hellogithub.com/hosts)
- [Default hosts source: jsDelivr mirror](https://fastly.jsdelivr.net/gh/AutismSuperman/github-dns/hosts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the user to run a local Python script that checks connectivity, edits the system hosts file, backs up prior hosts content, and flushes DNS caches.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

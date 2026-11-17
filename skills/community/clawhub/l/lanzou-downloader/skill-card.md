## Description:

Downloads individual files or selected items from Lanzou share links, including password-protected shares and batch lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwqww1](https://clawhub.ai/user/wwqww1)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents downloading files from Lanzou shares can list files, select specific items, and process multiple links from text, Markdown, or JSON lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JavaScript from remote pages can execute with the agent user's access.

Mitigation: Avoid broad deployment until this behavior is fixed; run only in a restricted environment if use is necessary.

Risk: The stated Lanzou domain boundary is not enforced, so untrusted links may reach unintended hosts.

Mitigation: Use only trusted Lanzou links and enforce an allowed-domain check before network requests.

## Reference(s):

- [Lanzou Downloader on ClawHub](https://clawhub.ai/wwqww1/skills/lanzou-downloader)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance, JSON file listings and manifests, and downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch downloads use title-based filenames with suffixes for duplicates.]

## Skill Version(s):

1.0.9 (source: server-resolved release and SKILL.md changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

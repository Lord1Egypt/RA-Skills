## Description:

GitHub Hosts CN helps users in China update system hosts entries for GitHub while preserving non-GitHub entries and supporting preview, backup, and restore workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n1e](https://clawhub.ai/user/n1e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to inspect and optionally update local GitHub-related hosts mappings when direct GitHub access is unreliable. It is intended for users who understand the effect of system-wide DNS overrides.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill writes externally supplied network-routing data into the privileged system hosts file.

Mitigation: Run only when intentionally changing GitHub DNS resolution and review the fetched mappings with --preview before applying them.

Risk: The security evidence reports weak safeguards and a likely broken restore path.

Mitigation: Avoid --yes, confirm each run interactively, and be prepared to manually edit or restore /etc/hosts if built-in restore fails.

Risk: Changing hosts entries can disrupt GitHub or broader network access.

Mitigation: Keep a known-good hosts backup available and validate connectivity after changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n1e/skills/github-hosts-cn-n1e)
- [HelloGitHub hosts source](https://raw.hellogithub.com/hosts)
- [GitLab ineo6 hosts source](https://gitlab.com/ineo6/hosts/-/raw/master/hosts)
- [Gitee hosts mirror](https://gitee.com/peng_zhihui/hosts/raw/master/hosts)
- [JSDelivr hosts mirror](https://cdn.jsdelivr.net/gh/ineo6/hosts@master/hosts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and terminal guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for running a Node.js hosts updater that may preview, update, back up, or restore system hosts entries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

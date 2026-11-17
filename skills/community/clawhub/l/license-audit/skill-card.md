## Description:

Multi-language license compliance audit powered by Trivy that detects GPL, AGPL, LGPL, MPL, BSL, and other risky licenses across Node.js, Python, Java, C#/.NET, Go, Rust, Ruby, PHP, and C/C++ projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theosunny](https://clawhub.ai/user/theosunny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering teams, and compliance reviewers use this skill to scan local projects or Git repositories for dependency license risk and produce reviewable reports for commercial open-source compliance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill can automatically run an unverified Trivy installer.

Mitigation: Install Trivy separately through a trusted, pinned method before invoking the skill, and avoid running it where installation to /usr/local/bin is allowed unintentionally.

Risk: The security review notes that private repository tokens can be exposed in logs if users place credentials in repository URLs.

Mitigation: Use SSH, a credential helper, or short-lived read-only credentials instead of embedding tokens in URLs, and avoid printing authenticated repository URLs.

Risk: Feishu output can upload dependency inventory to Feishu.

Mitigation: Use Feishu output only for intended internal sharing, preferably with a dedicated low-scope internal app and approved scopes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theosunny/skills/license-audit)
- [Trivy](https://github.com/aquasecurity/trivy)
- [Feishu developer console](https://open.feishu.cn)
- [Code Review Checklist](references/code-review-checklist.md)
- [Known License Table](references/known-licenses.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown, HTML, JSON, Feishu Doc, or Feishu Base report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize dependency license tiers as HIGH, MEDIUM, LOW, or UNKNOWN; file outputs can use generated timestamped filenames when no output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

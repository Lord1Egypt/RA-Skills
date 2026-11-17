## Description:

PIPL Audit helps agents run a Chinese Personal Information Protection Law compliance audit covering 32 checks across nine domains, with offline preview and optional CQDev cloud scoring at compliancehub.cn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preview or run a PIPL compliance audit for organizations processing personal information of natural persons in China. It collects yes/no/not-applicable answers, can submit scored runs to the CQDev cloud engine, and can generate local audit reports with risk levels and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored audits send yes/no audit answers plus either an API key or anonymous trial ID to compliancehub.cn.

Mitigation: Use the offline preview for no-network review, and run scored audits only when the user accepts sending those answers to the CQDev cloud engine.

Risk: Cloud-provided audit text is inserted into terminal prompts and HTML reports without escaping or browser protections.

Mitigation: Treat generated HTML reports as untrusted content, open them cautiously, and require escaping and browser hardening before broad deployment.

Risk: API keys may be stored in a local per-user file under ~/.config/compliancehub on shared machines.

Mitigation: Prefer COMPLIANCEHUB_API_KEY for ephemeral key use, and protect or remove local key files when using shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/pipl-audit)
- [CQDev compliance cloud endpoint](https://compliancehub.cn)
- [ComplianceHub API key page](https://compliancehub.cn/account.html?skill=pipl-audit)

## Skill Output:

**Output Type(s):** [text, JSON, HTML files, shell commands, configuration, guidance]

**Output Format:** [Terminal prompts, CLI text, JSON preview/scoring output, and optional local HTML audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline preview uses bundled checks; scored audits send answers to compliancehub.cn and may require COMPLIANCEHUB_API_KEY or an anonymous trial ID.]

## Skill Version(s):

2.0.2 (source: evidence.release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

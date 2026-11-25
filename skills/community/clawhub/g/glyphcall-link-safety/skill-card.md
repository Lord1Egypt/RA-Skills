## Description:

Decide whether a link is safe to open, click or pay before an agent follows it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutshell2000](https://clawhub.ai/user/nutshell2000)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to assess links from email, chat, scraped pages, or tool results before opening, clicking, or paying. It checks phishing blocklists, redirect hops, domain trust signals, HTTPS, security headers, and look-alike URL patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full URLs may contain private or sensitive information and are sent to an external provider.

Mitigation: Review URLs for sensitive data and redact it before submitting them for a check.

Risk: The security review flags the unpinned agentcash@latest package as a supply-chain concern.

Mitigation: Review the package source and pin a trusted version before running its CLI commands.

## Reference(s):

- [Glyphcall URL Safety API](https://api.glyphcall.com/pack/url-safety?url=<full-url>)
- [Glyphcall Phishing Check API](https://api.glyphcall.com/phishing/check?url=<full-url>)
- [ClawHub release page](https://clawhub.ai/nutshell2000/skills/glyphcall-link-safety)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, API Calls]

**Output Format:** [Structured URL risk assessment with supporting signals, summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an overall risk verdict and available redirect, host, and URL-pattern signals; failed checks should be treated as unknown rather than safe.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

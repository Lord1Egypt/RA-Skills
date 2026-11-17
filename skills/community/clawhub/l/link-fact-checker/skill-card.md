## Description:

Checks whether a supplied URL is reachable and returns a brief verification-style summary for link status and claimed facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wumingyu1688-sudo](https://clawhub.ai/user/wumingyu1688-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for preliminary checks of public links and lightweight review of online claims. It is best suited for link accessibility triage rather than authoritative fact-checking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate fact-checking capability because the security summary identifies it as a simple URL checker.

Mitigation: Use it for preliminary public URL checks only, and require independent source review before relying on factual conclusions.

Risk: The security guidance notes unrestricted network requests to user-supplied URLs.

Mitigation: Use only non-sensitive public URLs, and add URL allowlisting, private-network blocking, request timeouts, response-size limits, and privacy disclosure before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wumingyu1688-sudo/skills/link-fact-checker)
- [Publisher profile](https://clawhub.ai/user/wumingyu1688-sudo)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style verification summary or JSON result object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports URL accessibility, status code, page title when available, and pending cross-verification status for submitted facts.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
